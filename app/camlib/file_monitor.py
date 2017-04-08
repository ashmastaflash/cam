import os


class FileMonitor(object):
    """Monitor a directory for files of a certain suffix.

    Args:
        drop_dir (str): Directory to monitor.
        target_suffix (str): File suffix to monitor.
    """

    def __init__(self, drop_dir, target_suffix):
        self.drop_dir = drop_dir
        self.target_suffix = target_suffix

    def get_one_file(self):
        """Return the full path of one file matching the target suffix"""
        files = [os.path.join(self.drop_dir, x) for x in
                 os.listdir(self.drop_dir) if
                 os.path.isfile(os.path.join(self.drop_dir, x)) and
                 x.endswith(self.target_suffix)]
        target = None
        for tgt in files:
            try:
                fobj = open(tgt, 'a', 8)
                if fobj:
                    print("%s is finished andready to ship..." % tgt)
                    target = tgt
                    break
            except IOError:
                pass
        return target
