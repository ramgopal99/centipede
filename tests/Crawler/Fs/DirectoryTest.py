import os
import unittest
from ...BaseTestCase import BaseTestCase
from centipede.Crawler import Crawler
from centipede.PathHolder import PathHolder
from centipede.Crawler.Fs import Directory

class DirectoryTest(BaseTestCase):
    """Test Directory crawler."""

    __dir = os.path.join(BaseTestCase.dataDirectory(), "640x480")

    def testDirectoryCrawler(self):
        """
        Test that the Directory crawler test works properly.
        """
        crawler = Crawler.create(PathHolder(self.__dir))
        self.assertIsInstance(crawler, Directory)

    def testDirectoryVariables(self):
        """
        Test that the variables are set properly.
        """
        crawler = Crawler.create(PathHolder(self.__dir))
        self.assertEqual(crawler.var("width"), 640)
        self.assertEqual(crawler.var("height"), 480)

    def testIsLeaf(self):
        """
        Test to show directory crawler is not a leaf.
        """
        crawler = Crawler.create(PathHolder(self.__dir))
        self.assertFalse(crawler.isLeaf())

    def testBadFile(self):
        """
        Test to show that file names with illegal characters are skipped.
        """
        crawler = Crawler.create(PathHolder(self.dataDirectory()))
        crawlerPaths = map(lambda x: x.var("filePath"), crawler.children())
        self.assertNotIn(os.path.join(self.__dir, "bad file.txt"), crawlerPaths)


if __name__ == "__main__":
    unittest.main()
