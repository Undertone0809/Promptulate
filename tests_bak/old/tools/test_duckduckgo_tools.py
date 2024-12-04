from unittest import TestCase
from unittest.mock import patch

from promptulate.tools.duckduckgo.api_wrapper import DuckDuckGoSearchAPIWrapper
from promptulate.tools.duckduckgo.tools import DuckDuckGoReferenceTool, DuckDuckGoTool
from promptulate.utils.logger import logger


class TestDuckDuckGoSearchAPIWrapper(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.api_wrapper = DuckDuckGoSearchAPIWrapper()

    def test_search_by_keyword(self):
        result = self.api_wrapper.query("LLM")
        for item in result:
            logger.info(item)
        self.assertIsNotNone(result)

    def test_get_formatted_result(self):
        results = self.api_wrapper.query_by_formatted_results("LLM", 5)
        for result in results:
            logger.info(result)
        self.assertIsNotNone(results[0]["snippet"])
        self.assertIsNotNone(results[0]["title"])
        self.assertIsNotNone(results[0]["link"])


class TestDuckDuckGoSearchTool(TestCase):
    def test_query(self):
        tool = DuckDuckGoTool()
        query = "What is promptulate?"
        result = tool.run(query)
        logger.info(result)


class TestDuckDuckGoReferenceTool(TestCase):
    def test_query(self):
        tool = DuckDuckGoReferenceTool()
        result = tool.run("LLM", num_results=1)
        logger.info(result)
        self.assertTrue("snippet" in result)
        self.assertTrue("title" in result)
        self.assertTrue("link" in result)

    def test_query_by_json(self):
        tool = DuckDuckGoReferenceTool()
        results = tool.run("LLM", num_results=6, return_type="original")
        logger.info(results)
        self.assertIsNotNone(results[0]["snippet"])
        self.assertIsNotNone(results[0]["title"])
        self.assertIsNotNone(results[0]["link"])
        self.assertEqual(6, len(results))
