import os
from unittest import TestCase

import markdown

from markdown_include.include import IncludePreprocessor, MarkdownInclude


class TestInclude(TestCase):
    def setUp(self) -> None:
        self.maxDiff = None
        self.markdown_include = MarkdownInclude(
            configs={'base_path': os.path.dirname(os.path.realpath(__file__))}
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
                                "<h1>This heading will be one level deeper from the previous heading</h1>\n"
                                "<p>More included file content.\n"
                                "End of included content.</p>\n"
                                "<h2>Heading Level 2 of main file</h2>\n"
                                "<h1>This heading will be one level deeper from the previous heading</h1>\n"
                                "<p>More included file content.\n"
                                "End of included content.</p>")


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


class TestIncludeInheritHeaderDepth(TestCase):
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
