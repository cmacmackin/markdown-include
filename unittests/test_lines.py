import os
from unittest import TestCase

from markdown_include.include import IncludePreprocessor


class TestProcessor(TestCase):
    def setUp(self) -> None:
        self.maxDiff = None
        self.processor = IncludePreprocessor(None, {
            "base_path": os.path.dirname(os.path.realpath(__file__)),
            "encoding": "utf-8",
            "inheritHeadingDepth": False,
            "headingOffset": 0,
            "throwException": False,
        })

    def test_lines(self):
        source = ["Source file",
                  "# Heading Level 1 of main file",
                  "{!resources/header.md!}",
                  "## Heading Level 2 of main file",
                  "{!resources/header.md!}"]
        result_lines = self.processor.run(source)

        self.assertEqual(9, len(result_lines))
