import unittest
import os
from ...BaseTestCase import BaseTestCase
from ingestor.Task import Task
from ingestor.Crawler.Fs import FsPath

class RemoveTest(BaseTestCase):
    """Test Remove task."""

    __path = os.path.join(BaseTestCase.dataDirectory(), "toRemove.exr")

    @classmethod
    def setUpClass(cls):
        """
        Create a file to remove in the test.
        """
        open(cls.__path, 'w').close()

    def testRemove(self):
        """
        Test that the remove task works properly.
        """
        pathCrawler = FsPath.createFromPath(self.__path)
        removeTask = Task.create('remove')
        removeTask.add(pathCrawler, self.__path)
        result = removeTask.output()
        self.assertEqual(len(result), 1)
        crawler = result[0]
        self.assertFalse(os.path.isfile(crawler.var("filePath")))


if __name__ == "__main__":
    unittest.main()
