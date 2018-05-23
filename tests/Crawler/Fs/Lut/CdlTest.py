import os
import unittest
from ....BaseTestCase import BaseTestCase
from ingestor.Crawler import Crawler
from ingestor.PathHolder import PathHolder
from ingestor.Crawler.Fs.Lut import Cdl

class CdlTest(BaseTestCase):
    """Test Cdl crawler."""

    __cdlFile = os.path.join(BaseTestCase.dataDirectory(), "test.cdl")
    # disable test for now until cdl crawler is fixed
    pass
    # def testCdlCrawler(self):
    #     """
    #     Test that the Cdl crawler test works properly.
    #     """
    #     crawler = Crawler.create(PathHolder(self.__cdlFile))
    #     self.assertIsInstance(crawler, Cdl)
    #
    # def testCdlVariables(self):
    #     """
    #     Test that variables are set properly.
    #     """
    #     crawler = Crawler.create(PathHolder(self.__cdlFile))
    #     self.assertEqual(crawler.var("type"), "cdl")
    #     self.assertEqual(crawler.var("category"), "lut")
    #     self.assertEqual(crawler.var("slope"), [1.1, 1.2, 1.3])
    #     self.assertEqual(crawler.var("offset"), [0.1, 0.2, 0.3])
    #     self.assertEqual(crawler.var("power"), [1.4, 1.5, 1.6])
    #     self.assertEqual(crawler.var("saturation"), 1.0)


if __name__ == "__main__":
    unittest.main()
