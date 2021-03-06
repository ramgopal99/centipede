import os
import unittest
from ....BaseTestCase import BaseTestCase
from centipede.Crawler import Crawler
from centipede.PathHolder import PathHolder
from centipede.Crawler.Fs.Ascii import Txt

class TxtTest(BaseTestCase):
    """Test Txt crawler."""

    __txtFile = os.path.join(BaseTestCase.dataDirectory(), "test.txt")

    def testTxtCrawler(self):
        """
        Test that the Txt crawler test works properly.
        """
        crawler = Crawler.create(PathHolder(self.__txtFile))
        self.assertIsInstance(crawler, Txt)

    def testTxtVariables(self):
        """
        Test that variables are set properly.
        """
        crawler = Crawler.create(PathHolder(self.__txtFile))
        self.assertEqual(crawler.var("type"), "txt")
        self.assertEqual(crawler.var("category"), "ascii")

    def testTxtContents(self):
        """
        Test that txt files are parsed properly.
        """
        crawler = Crawler.create(PathHolder(self.__txtFile))
        testData = "testing txt file\nwith random data\n\n1 2 3\n"
        self.assertEqual(crawler.contents(), testData)


if __name__ == "__main__":
    unittest.main()
