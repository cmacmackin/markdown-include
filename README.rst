Markdown-Include
================

This is an extension to
`Python-Markdown <https://pythonhosted.org/Markdown/>`__ which provides
an "include" function, similar to that found in LaTeX (and also the C
pre-processor and Fortran). I originally wrote it for my
`FORD <https://pypi.python.org/pypi/FORD>`__ Fortran auto-documentation
generator.

Installation
------------

This module can now be installed using ``pip``.

::

    pip install markdown-include

Usage
-----

This module can be used in a program in the following way:

::

    import markdown
    html = markdown.markdown(source, extensions=[markdown_include.include'])

The syntax for use within your Markdown files is ``{!filename!}``. This
statement will be replaced by the contents of ``filename``.
Markdown-Include will work recursively, so any included files within
``filename`` wil also be included. This replacement is done prior to any
other Markdown processing, so any Markdown syntax that you want can be used
within your included files. Note that this is a change from the previous 
version. It was felt that this syntax was less likely to conflict with any code
fragments present in the Markdown.

By default, all file-names are evaluated relative to the location from
which Markdown is being called. If you would like to change the
directory relative to which paths are evaluated, then this can be done
by specifying the extension setting ``base_path``.

::

    import markdown
    from markdown_include.include import MarkdownInclude

    # Markdown Extensions
    markdown_include = MarkdownInclude(
        configs={'base_path':'/srv/content/', 'encoding': 'iso-8859-1'}
    )
    html = markdown.markdown(source, extensions=[markdown_include])

