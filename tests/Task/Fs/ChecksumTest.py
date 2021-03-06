import unittest
import os
import shutil
from ...BaseTestCase import BaseTestCase
from centipede.Task import Task
from centipede.Crawler.Fs import FsPath
from centipede.Task.Fs.Checksum import ChecksumMatchError

class ChecksumTest(BaseTestCase):
    """Test Checksum task."""

    __sourcePath = os.path.join(BaseTestCase.dataDirectory(), "test.exr")
    __targetPath = os.path.join(BaseTestCase.dataDirectory(), "testCopy.exr")
    __otherPath = os.path.join(BaseTestCase.dataDirectory(), "RND_ass_lookdev_default_beauty_tt.1001.exr")

    @classmethod
    def setUpClass(cls):
        """
        Create copy of the source file.
        """
        shutil.copy2(
            cls.__sourcePath,
            cls.__targetPath
        )

    def testChecksum(self):
        """
        Test that the checksum task works properly.
        """
        crawler = FsPath.createFromPath(self.__sourcePath)
        checksumTask = Task.create('checksum')
        checksumTask.add(crawler, self.__targetPath)
        result = checksumTask.output()
        self.assertEqual(len(result), 1)
        checksumTask = Task.create('checksum')
        checksumTask.add(crawler, self.__otherPath)
        self.assertRaises(ChecksumMatchError, checksumTask.output)

    @classmethod
    def tearDownClass(cls):
        """
        Remove the file that was copied.
        """
        os.remove(cls.__targetPath)


if __name__ == "__main__":
    unittest.main()
