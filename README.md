# Markdown-Include

This is an extension to [Python-Markdown](https://pythonhosted.org/Markdown/)
which provides an "include" function, similar to that found in
LaTeX (and also the C pre-processor and Fortran). I originally wrote it for my
[FORD](https://github.com/cmacmackin/ford) Fortran auto-documentation generator.


## Installation
This module can now be installed using ``pip``.

    pip install markdown-include


## Usage
This module can be used in a program in the following way:

```python
import markdown
html = markdown.markdown(source, extensions=['markdown_include.include'])
```

The syntax for use within your Markdown files is ``{!filename!}``. This
statement will be replaced by the contents of ``filename``. Markdown-Include
will work recursively, so any included files within ``filename`` will also be
included. This replacement is done prior to any other
Markdown processing, so any Markdown syntax that you want can be used within
your included files. Note that this is a change from the previous version.
It was felt that this syntax was less likely to conflict with any code
fragments present in the Markdown.

By default, all file-names are evaluated relative to the location from which
Markdown is being called. If you would like to change the directory relative to
which paths are evaluated, then this can be done by specifying the extension
setting ``base_path``.

If there are leading tabs and spaces before the include statement, 
all the lines of the included file get prepended the same number of tabs, 
so includes to indented sections get automatically indented.

## Configuration

The following settings can be specified when initialising the plugin.

- __base_path__: Default location from which to evaluate relative
  paths for the include statement. (Default: the run-directory.)
- __encoding__: Encoding of the files used by the include statement. (Default: utf-8.)
- __inheritHeadingDepth__ : If true, increases headings on include
  file by amount of previous heading. Combiens with headingOffset
  option, below. (Default: False.)
- __headingOffset__: Increases heading depth by a specific ammount, in
  addition to the inheritHeadingDepth Option. (Default: 0)
- __throwException__: When true, if the extension is unable to find an
  included file it will throw an exception which the user can
  catch. If false (default), a warning will be printed and Markdown
  will continue parsing the file.

## Examples

An example of setting the base path and file encoding is given below:
```python
import markdown
from markdown_include.include import MarkdownInclude

# Markdown Extensions
markdown_include = MarkdownInclude(
    configs={'base_path':'/srv/content/', 'encoding': 'iso-8859-1'}
)
html = markdown.markdown(source, extensions=[markdown_include])
```

Included files can inherit the heading depth of the location
``inheritHeadingDepth``, as well as receive a specific offset, ``headingOffset``
For example, consider the  files
```markdown
Source file
# Heading Level 1 of main file

{!included_file.md!}

## Heading Level 2 of main file

{!included_file.md!}
```

and included_file.md

```markdown
# This heading will be one level deeper from the previous heading
More included file content.
End of included content.
```
Then running the script
```python
import markdown
from markdown_include.include import MarkdownInclude

# Markdown Extensions
markdown_include = MarkdownInclude(
    configs={'inheritHeadingDepth':True}
)
html = markdown.markdown(source, extensions=[markdown_include])
```
produces
```html
<p>Source file</p>
<h1>Heading Level 1 of main file</h1>
<h2>This heading will be one level deeper from the previous heading</h2>
<p>More included file content.</p>
<p>End of included content.</p>
<h2>Heading Level 2 of main file</h2>
<h3>This heading will be one level deeper from the previous heading</h3>
<p>More included file content.</p>
<p>End of included content.</p>
```


## ChangeLog
### Version 0.7.0
Modified to work with Python-Markdown 3.4. This makes the plugin
incompatible with versions < 3.0.
### Version 0.6.0
- Added ability ot offset headers in the included file so they fall under the header level in which the include occurs
- Add option to throw exception when can't find an include file (instead of printing a warning)
- Fixed stripping of last character in file, so only occurs if it is a new-line
- Some behind-the-scenes improvement to code and documentation
### Version 0.5.1
Bugfix for a syntax error.
### Version 0.5
Corrected some errors in documentation and merged in commits of
[diegobz](https://github.com/diegobz) to add support for encoding and tidy up
the source code.
### Version 0.4
Fixed problem related to passing configurations to the extension.
### Version 0.3
Added support for Python 3.
### Version 0.2
Changed the API to be less likely to conflict with other syntax.
### Version 0.1
Initial release.
