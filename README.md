#Markdown-Include

This is an extension to [Python-Markdown](https://pythonhosted.org/Markdown/)
which provides an "include" function, similar to that found in
LaTeX (and also the C pre-processor and Fortran). I originally wrote it for my
[FORD](https://github.com/cmacmackin/ford) Fortran auto-documentation generator.


##Installation
Place the ``markdown_include`` directory somewhere in your PYTHONPATH.
Hopefully in the near future this module will be available on PyPI and can be
installed using pip.


##Usage
This module can be used in a program in the following way:

	:::python
    import markdown
	html = markdown.markdown(source, extensions=[markdown_include.include'])

The syntax for use within your Markdown files is ``{{filename}}``. This
statement will be replaced by the contents of ``filename``. Markdown-Include
will work recursively, so any included files within ``filename`` wil also be
included. This replacement is done prior to any other
Markdown processing, so any Markdown syntax that you want can be used within
your included files.

By default, all file-names are evaluated relative to the location from which
Markdown is being called. If you would like to change the directory relative to
which paths are evaluated, then this can be done by specifying the extension
setting ``base_dir``. 

