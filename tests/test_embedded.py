import os
from unittest import TestCase

import markdown

from markdown_include.include import IncludePreprocessor, MarkdownInclude


class TestEmbedded(TestCase):
    def setUp(self) -> None:
        self.maxDiff = None
        self.markdown_include = MarkdownInclude(
            configs={'base_path': os.path.dirname(os.path.realpath(__file__))}
        )

    def test_embedded_template(self):
        source = "{!resources/template_inside.md!}"
        html = markdown.markdown(source, extensions=[self.markdown_include])

        self.assertEqual(html, "<p>This is a simple template</p>\n<p>This is a template with a template.</p>")
