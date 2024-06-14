"""
File cache.

Copies files from a remote filesystem (e.g. NFS)
to a local filesystem (e.g. /var/tmp) to speed up access.

See https://github.com/rwth-i6/returnn/issues/1519 for initial discussion.

Main class is :class:`FileCache`.
"""

from typing import Any, Collection, List, Tuple
import os
import time
import shutil
from dataclasses import dataclass
from collections import defaultdict
from contextlib import contextmanager
from threading import Thread, Event
from .basic import expand_env_vars, LockFile, human_bytes_size


__all__ = ["FileCache", "CachedFile"]


class FileCache:
    """
    File cache.

    Copies files from a remote filesystem (e.g. NFS)
    to a local filesystem (e.g. ``/var/tmp``) to speed up access.

    Some assumptions we depend on:

    - When a cached file is available, and its size matches the original file,
      we can use it.
      (We might want to extend this logic later, e.g. by storing and checking the original source mtime.
       But for simplicity, we don't do this for now.)
    - We will update the cached file mtime frequently (every second) via a background thread
      of used cached files, to mark that they are used.
      (We would maybe want to use atime, but we don't expect that atime can be relied on.)
      Note that updating mtime might influence the behavior of some external tools.
      (If this becomes a problem at some point, instead of abusing mtime this way,
       we might store the most recent usage time e.g. in a separate file.)
    - :func:`os.utime` will update mtime, and mtime is somewhat accurate (up to 10 secs maybe),
      mtime compares to time.time().
    - :func:`shutil.disk_usage` can be relied on.

    See https://github.com/rwth-i6/returnn/issues/1519 for initial discussion.
    """

    def __init__(
        self,
        *,
        cache_directory: str = "$TMPDIR/$USER/returnn/file_cache",
        cleanup_files_always_older_than_days: float = 31.0,
        cleanup_files_wanted_older_than_days: float = 7.0,
        cleanup_disk_usage_wanted_free_ratio: float = 0.2,  # try to free at least 20% disk space
    ):
        """
        :param cache_directory: directory where to cache files.
            Uses :func:`expand_env_vars` to expand environment variables.
        :param cleanup_files_always_older_than_days: always cleanup files older than this.
        :param cleanup_files_wanted_older_than_days: if cleanup_disk_usage_wanted_free_ratio not reached,
            cleanup files older than this.
        :param cleanup_disk_usage_wanted_free_ratio: try to free at least this ratio of disk space.
        """
        self.cache_directory = expand_env_vars(cache_directory)
        self._cleanup_files_always_older_than_days = cleanup_files_always_older_than_days
        self._cleanup_files_wanted_older_than_days = cleanup_files_wanted_older_than_days
        self._cleanup_disk_usage_wanted_free_ratio = cleanup_disk_usage_wanted_free_ratio
        self._touch_files_thread = _TouchFilesThread(cache_base_dir=self.cache_directory)
        self._touch_files_thread.start()
        self._recent_full_cleanup_time = float("-inf")

    # Note on lock_timeout: It will check whether a potentially existing lock file is older than this timeout,
    # and if so, then it would delete the existing lock file, assuming it is from a crashed previous run.
    # We are always keeping the lock file mtime updated via the _touch_files_thread (every second),
    # so it should never be older than this timeout.
    # If there is a Python exception anywhere here, we will always properly release the lock.
    # Only if the process dies (e.g. killed, segfault or so), the lock file might be left-over,
    # and another process might need to wait for this timeout.
    # We don't expect that this must be configured, so let's just use a reasonable default.
    # This should be more than the _touch_files_thread interval (1 sec).
    _lock_timeout = 20

    def __del__(self):
        self._touch_files_thread.stop.set()

    def get_file(self, src_filename: str) -> str:
        """
        Get cached file.
        This will copy the file to the cache directory if it is not already there.
        This will also make sure that the file is not removed from the cache directory
        via the _touch_files_thread
        until you call :func:`release_file`.

        :param src_filename: source file to copy (if it is not already in the cache).
        :return: cached file path (in the cache directory)
        """
        dst_filename = self._get_dst_filename(src_filename)
        self._copy_file_if_needed(src_filename, dst_filename)
        self._touch_files_thread.files_extend([dst_filename])
        return dst_filename

    def release_files(self, filenames: Collection[str]):
        """
        Release cached files.
        This just says that we are not using the files anymore for now.
        They will be kept in the cache directory for now,
        and might be removed when the cache directory is cleaned up.

        :param filenames: files to release (paths in the cache directory)
        """
        self._touch_files_thread.files_remove(filenames)

    def cleanup(self, *, need_at_least_free_space_size: int = 0):
        """
        Cleanup cache directory.
        """
        if not os.path.exists(self.cache_directory):
            return
        disk_usage = shutil.disk_usage(self.cache_directory)
        want_free_space_size = max(
            need_at_least_free_space_size, int(self._cleanup_disk_usage_wanted_free_ratio * disk_usage.total)
        )
        # If we have enough free space, and we did a full cleanup recently, we don't need to do anything.
        if want_free_space_size <= disk_usage.free and time.monotonic() - self._recent_full_cleanup_time < 60 * 10:
            return
        # Do a full cleanup, i.e. iterate through all files in cache directory and check their mtime.
        # Get current time now, so that cur_time - mtime is pessimistic,
        # and does not count the time for the cleanup itself.
        cur_time = time.time()
        all_files = []  # mtime, neg size (better for sorting), filename
        for root, dirs, files in os.walk(self.cache_directory):
            for rel_fn in files:
                fn = root + "/" + rel_fn
                try:
                    f_stat = os.stat(fn)
                except Exception as exc:
                    print(f"FileCache: Error while stat {fn}: {type(exc).__name__}: {exc}")
                    continue
                else:
                    all_files.append((f_stat.st_mtime, -f_stat.st_blocks * 512, fn))
        all_files.sort()
        cur_expected_free = disk_usage.free
        reached_more_recent_files = False
        cur_used_time_threshold = self._lock_timeout * 0.5  # Used files mtime should be updated every second.
        total_cache_files_size = sum(-neg_size for _, neg_size, _ in all_files)
        total_cur_used_cache_files_size = sum(
            -neg_size for mtime, neg_size, fn in all_files if cur_time - mtime <= cur_used_time_threshold
        )
        report_size_str = (
            f"Total size cached files: {human_bytes_size(total_cache_files_size)},"
            f" currently used: {human_bytes_size(total_cur_used_cache_files_size)}"
        )
        for mtime, neg_size, fn in all_files:
            size = -neg_size
            delete_reason = None
            if cur_time - mtime > self._cleanup_files_always_older_than_days * 60 * 60 * 24:
                delete_reason = f"File is {(cur_time - mtime) / 60 / 60 / 24} days old"
            else:
                reached_more_recent_files = True
            if not delete_reason and need_at_least_free_space_size > cur_expected_free:
                # Still must delete some files.
                if cur_time - mtime > cur_used_time_threshold:
                    delete_reason = f"Still need more space, file is {cur_time - mtime} secs old"
                else:
                    raise Exception(
                        f"We cannot free enough space on {self.cache_directory}.\n"
                        f"Needed: {human_bytes_size(need_at_least_free_space_size)},\n"
                        f"currently available: {human_bytes_size(cur_expected_free)},\n"
                        f"oldest file is still too recent: {fn}.\n"
                        f"{report_size_str}"
                    )
            if not delete_reason and want_free_space_size > cur_expected_free:
                if cur_time - mtime > self._cleanup_files_wanted_older_than_days * 60 * 60 * 24:
                    delete_reason = f"Still want more space, file is {(cur_time - mtime) / 60} min old"
                else:
                    # All further files are even more recent, so we would neither cleanup them,
                    # so we can also just stop now.
                    break

            if delete_reason:
                cur_expected_free += size
                print(
                    f"FileCache: Delete file {fn}, size {human_bytes_size(size)}. {delete_reason}."
                    f" After deletion, have {human_bytes_size(cur_expected_free)} free space."
                )
                try:
                    os.remove(fn)
                except Exception as exc:
                    print(f"FileCache: Error while removing {fn}: {type(exc).__name__}: {exc}")
                    cur_expected_free -= size

            if reached_more_recent_files and want_free_space_size <= cur_expected_free:
                # Have enough free space now.
                break

        if need_at_least_free_space_size > cur_expected_free:
            raise Exception(
                f"We cannot free enough space on {self.cache_directory}.\n"
                f"Needed: {human_bytes_size(need_at_least_free_space_size)},\n"
                f"currently available: {human_bytes_size(cur_expected_free)}.\n"
                f"{report_size_str}"
            )

        # Cleanup empty dirs.
        for root, dirs, files in os.walk(self.cache_directory, topdown=False):
            if files:
                continue
            try:
                if cur_time - os.stat(root).st_mtime <= cur_used_time_threshold:  # still in use?
                    continue
            except Exception as exc:
                print(f"FileCache: Error while stat dir {root}: {type(exc).__name__}: {exc}")
                continue
            try:
                # Recheck existence of dirs, because they might have been deleted by us.
                if any(os.path.exists(root + "/" + d) for d in dirs):
                    continue
            except Exception as exc:
                print(f"FileCache: Error while checking sub dirs in {root}: {type(exc).__name__}: {exc}")
                continue
            try:
                # We can delete this empty dir.
                print(f"FileCache: Remove empty dir {root}")
                os.rmdir(root)
            except Exception as exc:
                print(f"FileCache: Error while removing empty dir {root}: {type(exc).__name__}: {exc}")

        self._recent_full_cleanup_time = time.monotonic()

    def handle_cached_files_in_config(self, config: Any) -> Tuple[Any, List[str]]:
        """
        :param config: some config, e.g. dict, or any nested structure
        :return: modified config, where all :class:`CachedFile` instances are replaced by the cached file path,
            and the list of cached files which are used.
        """
        import tree

        res_files = []

        def _handle_value(value):
            if isinstance(value, CachedFile):
                res = self.get_file(value.filename)
                res_files.append(res)
                return res
            return value

        return tree.map_structure(_handle_value, config), res_files

    def _get_dst_filename(self, src_filename: str) -> str:
        """
        Get the destination filename in the cache directory.
        """
        assert src_filename.startswith("/")
        return self.cache_directory + src_filename

    def _copy_file_if_needed(self, src_filename: str, dst_filename: str):
        """
        Copy the file to the cache directory.
        """
        if self._check_existing_copied_file_maybe_cleanup(src_filename, dst_filename):
            os.utime(dst_filename, None)  # touch
            return

        # Make sure we have enough disk space.
        self.cleanup(need_at_least_free_space_size=os.stat(src_filename).st_size)

        print(f"FileCache: Copy file {src_filename} to cache")

        # Create dirs.
        dst_dir = os.path.dirname(dst_filename)
        os.makedirs(dst_dir, exist_ok=True)

        # Copy the file, while holding a lock. See comment on lock_timeout above.
        with LockFile(
            directory=dst_dir, name=os.path.basename(dst_filename) + ".lock", lock_timeout=self._lock_timeout
        ) as lock:
            # Maybe it was copied in the meantime, while waiting for the lock.
            if os.path.exists(dst_filename):
                return

            dst_tmp_filename = dst_filename + ".copy"
            if os.path.exists(dst_tmp_filename):
                # The minimum age should be at least the lock_timeout.
                # (But leave a bit of room for variance in timing in the sanity check below.)
                dst_tmp_file_age = time.time() - os.stat(dst_tmp_filename).st_mtime
                assert dst_tmp_file_age > self._lock_timeout * 0.8, (
                    f"FileCache: Expected left-over temp copy file {dst_tmp_filename}"
                    f" from crashed previous copy attempt"
                    f" to be older than {self._lock_timeout * 0.8}s but it is {dst_tmp_file_age} seconds old"
                )

            with self._touch_files_thread.files_added_context([dst_dir, lock.lockfile]):
                shutil.copyfile(src_filename, dst_tmp_filename)
                os.rename(dst_tmp_filename, dst_filename)

    @staticmethod
    def _check_existing_copied_file_maybe_cleanup(src_filename: str, dst_filename: str) -> bool:
        """
        Check if the file is in the cache directory.
        """
        if not os.path.exists(dst_filename):
            return False
        src_stat = os.stat(src_filename)
        dst_stat = os.stat(dst_filename)
        if src_stat.st_size != dst_stat.st_size:
            os.remove(dst_filename)
            return False
        return True


@dataclass
class CachedFile:
    """
    Represents some file to be cached in a user config.
    See :func:`FileCache.handle_cached_files_in_config`.
    """

    filename: str  # original filename


class _TouchFilesThread(Thread):
    def __init__(self, *, interval: float = 1.0, cache_base_dir: str):
        super().__init__(daemon=True)
        self.stop = Event()
        self.files = defaultdict(int)  # usage counter
        self.interval = interval
        self.cache_base_dir = cache_base_dir

    def run(self):
        """thread main loop"""
        while True:
            all_files = {}  # dict to have order deterministic
            for filename in self.files:
                all_files[filename] = True
                all_files.update({k: True for k in _all_parent_dirs(filename, base_dir=self.cache_base_dir)})
            for filename in all_files:
                os.utime(filename, None)
            if self.stop.wait(self.interval):
                return

    def files_extend(self, files: Collection[str]):
        """append"""
        assert isinstance(files, (list, set, tuple))
        for file in files:
            self.files[file] += 1

    def files_remove(self, files: Collection[str]):
        """remove"""
        if isinstance(files, str):
            files = [files]
        assert isinstance(files, (list, set, tuple))
        for filename in files:
            self.files[filename] -= 1
            if self.files[filename] <= 0:
                del self.files[filename]

    @contextmanager
    def files_added_context(self, files: Collection[str]):
        """temporarily add files, and remove them afterwards again."""
        self.files_extend(files)
        try:
            yield
        finally:
            self.files_remove(files)


def _all_parent_dirs(filename: str, *, base_dir: str) -> List[str]:
    assert filename.startswith(base_dir + "/")
    dirs = []
    while True:
        filename = os.path.dirname(filename)
        if filename == base_dir:
            break
        dirs.append(filename)
    return dirs
