import os
from unittest import TestCase

import markdown

from markdown_include.include import MarkdownInclude


class TestInclude(TestCase):
    def setUp(self) -> None:
        self.maxDiff = None
        self.markdown_include = MarkdownInclude(
            configs={'base_path': os.path.dirname(os.path.realpath(__file__)), 'inheritHeadingDepth': True}
        )

    def test_single_include(self):
        source = "{!resources/simple.md!}"
        html = markdown.markdown(source, extensions=[self.markdown_include])

        self.assertEqual(html, '<p>This is a simple template</p>')

    def test_double_include(self):
        source = "{!resources/simple.md!} and {!resources/simple_2.md!}"
        html = markdown.markdown(source, extensions=[self.markdown_include])

        self.assertEqual(html, '<p>This is a simple template and This is another simple template</p>')

    def test_headers(self):
        source = "Source file\n" \
                 "# Heading Level 1 of main file\n" \
                 "{!resources/header.md!}\n" \
                 "## Heading Level 2 of main file\n" \
                 "{!resources/header.md!}"

        html = markdown.markdown(source, extensions=[self.markdown_include])

        self.assertEqual(html, "<p>Source file</p>\n"
                                "<h1>Heading Level 1 of main file</h1>\n"
                                "<h2>This heading will be one level deeper from the previous heading</h2>\n"
                                "<p>More included file content.</p>\n"
                                "<p>End of included content.</p>\n"
                                "<h2>Heading Level 2 of main file</h2>\n"
                                "<h3>This heading will be one level deeper from the previous heading</h3>\n"
                                "<p>More included file content.</p>\n"
                                "<p>End of included content.</p>")
