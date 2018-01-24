from pathlib import Path
import RfcPaths
import json


class ImageLib:
    def __init__(self):
        """
        Initialize
        """
        self.rpath = RfcPaths.RfcPaths()
        self.image_list = None

    def make_json(self):
        """
        Create image list json file from dictionary, indexed by filename, and include file metadata.
        :return: None
        """
        self.image_list = [x for x in self.rpath.imagepath.iterdir() if x.is_file() and x.name.endswith('.png')]
        stat_fields = ['st_mode', 'st_ino', 'st_dev', 'st_nlink', 'st_uid', 'st_gid', 'st_size', 'st_atime',
                       'st_mtime', 'st_ctime']

        image_dict = {}

        for image_file in self.image_list:
            stats = image_file.lstat()
            image_dict[image_file.name] = {}
            idx = image_dict[image_file.name]

            for n, field in enumerate(stat_fields):
                idx[field] = stats[n]

        with self.rpath.imagedict.open('w') as fo:
            json.dump(image_dict, fo)


def testit():
    """
    Test routine
    :return: None
    """
    il = ImageLib()
    il.make_json()

if __name__ == '__main__':
    testit()
