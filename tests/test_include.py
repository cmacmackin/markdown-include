from markdown_include.include import IncludePreprocessor, MarkdownInclude

import markdown
import pathlib
from textwrap import dedent

import pytest

RESOURCE_DIR = pathlib.Path(__file__).parent.absolute() / "resources"


@pytest.fixture(scope="module")
def markdown_include():
    return MarkdownInclude(configs={"base_path": RESOURCE_DIR})


@pytest.fixture(scope="module")
def markdown_include_inherit_heading_depth():
    return MarkdownInclude(
        configs={"base_path": RESOURCE_DIR, "inheritHeadingDepth": True}
    )


def test_relative_path(markdown_include):
    source = "{!docs/template/template.md!}"
    html = markdown.markdown(source, extensions=[markdown_include])

    assert html == "<p><img alt=\"some_image.jpg\" src=\"docs/template/some_image.jpg\" /></p>"


def test_relative_path_parent(markdown_include):
    source = "{!docs/template/template_2.md!}"
    html = markdown.markdown(source, extensions=[markdown_include])

    assert html == "<p><img alt=\"some_image.jpg\" src=\"docs/template/../images/image1.jpg\" /></p>"


def test_relative_path_url_link(markdown_include):
    source = "{!with_link.md!}"
    html = markdown.markdown(source, extensions=[markdown_include])

    assert html == "<p><a href=\"https://google.com\">some link</a></p>"


def test_abs_url_link(markdown_include):
    source = "{!docs/template/template_abs_link.md!}"
    html = markdown.markdown(source, extensions=[markdown_include])

    assert html == "<p><a href=\"/template\">some link</a></p>"


def test_frag_url_link(markdown_include):
    source = "{!docs/template/template_frag_link.md!}"
    html = markdown.markdown(source, extensions=[markdown_include])

    assert html == "<p><a href=\"#template\">some link</a></p>"


def test_relative_path_img_url_link(markdown_include):
    source = "{!with_img_link.md!}"
    html = markdown.markdown(source, extensions=[markdown_include])

    assert html == "<p><img alt=\"some link\" src=\"https://google.com\" /></p>"


def test_single_include(markdown_include):
    source = "{!simple.md!}"
    html = markdown.markdown(source, extensions=[markdown_include])

    assert html == "<p>This is a simple template</p>"


def test_double_include(markdown_include):
    source = "{!simple.md!} and {!simple_2.md!}"
    html = markdown.markdown(source, extensions=[markdown_include])

    assert (
            html == "<p>This is a simple template and This is another simple template</p>"
    )


def test_headers(markdown_include):
    source = (
        "Source file\n"
        "# Heading Level 1 of main file\n"
        "{!header.md!}\n"
        "## Heading Level 2 of main file\n"
        "{!header.md!}"
    )

    html = markdown.markdown(source, extensions=[markdown_include])

    assert html == dedent(
        """\
        <p>Source file</p>
        <h1>Heading Level 1 of main file</h1>
        <h1>This heading will be one level deeper from the previous heading</h1>
        <p>More included file content.
        End of included content.</p>
        <h2>Heading Level 2 of main file</h2>
        <h1>This heading will be one level deeper from the previous heading</h1>
        <p>More included file content.
        End of included content.</p>"""
    )


def test_embedded_template(markdown_include):
    source = "{!template_inside.md!}"
    html = markdown.markdown(source, extensions=[markdown_include])

    assert (
            html
            == "<p>This is a simple template</p>\n<p>This is a template with a template.</p>"
    )


def test_single_include_inherit_heading_depth(markdown_include_inherit_heading_depth):
    source = "{!simple.md!}"
    html = markdown.markdown(
        source, extensions=[markdown_include_inherit_heading_depth]
    )

    assert html == "<p>This is a simple template</p>"


def test_double_include_inherit_heading_depth(markdown_include_inherit_heading_depth):
    source = "{!simple.md!} and {!simple_2.md!}"
    html = markdown.markdown(
        source, extensions=[markdown_include_inherit_heading_depth]
    )

    assert (
            html == "<p>This is a simple template and This is another simple template</p>"
    )


def test_headers_inherit_heading_depth(markdown_include_inherit_heading_depth):
    source = (
        "Source file\n"
        "# Heading Level 1 of main file\n"
        "{!header.md!}\n"
        "## Heading Level 2 of main file\n"
        "{!header.md!}"
    )

    html = markdown.markdown(
        source, extensions=[markdown_include_inherit_heading_depth]
    )

    assert html == dedent(
        """\
        <p>Source file</p>
        <h1>Heading Level 1 of main file</h1>
        <h2>This heading will be one level deeper from the previous heading</h2>
        <p>More included file content.
        End of included content.</p>
        <h2>Heading Level 2 of main file</h2>
        <h3>This heading will be one level deeper from the previous heading</h3>
        <p>More included file content.
        End of included content.</p>"""
    )


def test_processor_lines():
    processor = IncludePreprocessor(
        None,
        {
            "base_path": RESOURCE_DIR,
            "encoding": "utf-8",
            "inheritHeadingDepth": False,
            "headingOffset": 0,
            "throwException": False,
        },
    )

    source = [
        "Source file",
        "# Heading Level 1 of main file",
        "{!header.md!}",
        "## Heading Level 2 of main file",
        "{!header.md!}",
    ]
    result_lines = processor.run(source)

    assert len(result_lines) == 9


def test_include_lines(markdown_include):
    source = "{!longer.md!lines=1 3}"
    html = markdown.markdown(source, extensions=[markdown_include])

    assert html == dedent(
        """\
        <p>This is line 1
        This is line 3</p>"""
    )


def test_include_line_range(markdown_include):
    source = "{!longer.md!lines=3-5}"
    html = markdown.markdown(source, extensions=[markdown_include])

    assert html == dedent(
        """\
        <p>This is line 3
        This is line 4
        This is line 5</p>"""
    )


def test_include_lines_and_line_range(markdown_include):
    source = "{!longer.md!lines=1 3-5 8}"
    html = markdown.markdown(source, extensions=[markdown_include])

    assert html == dedent(
        """\
        <p>This is line 1
        This is line 3
        This is line 4
        This is line 5
        This is line 8</p>"""
    )


def test_include_lines_out_of_order(markdown_include):
    source = "{!longer.md!lines=3 1}"
    html = markdown.markdown(source, extensions=[markdown_include])

    assert html == dedent(
        """\
        <p>This is line 3
        This is line 1</p>"""
    )


def test_nested_table(markdown_include_inherit_heading_depth):
    source = "{!table_inner.md!}"
    html = markdown.markdown(
        source, extensions=[markdown_include_inherit_heading_depth, "tables"]
    )

    assert "<table>" in html
