import time
from unittest import TestCase

from promptulate import enable_log
from promptulate.tools import sleep_tool

enable_log()


class TestSleepTool(TestCase):
    def test_run(self):
        seconds = "1s"
        start_time = time.time()
        sleep_tool(seconds)
        duration = time.time() - start_time
        self.assertAlmostEqual(1, duration, delta=0.1)
