from setuptools import setup, find_packages
from codecs import open  # To use a consistent encoding
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the relevant file
with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
  name = 'markdown-include',
  packages = find_packages(),
  version = '0.5.0',
  description = 'This is an extension to Python-Markdown which provides an "include" function, similar to that found in LaTeX (and also the C pre-processor and Fortran). I originally wrote it for my FORD Fortran auto-documentation generator.',
  long_description = long_description,
  author = 'Chris MacMackin',
  author_email = 'cmacmackin@gmail.com',
  url = 'https://github.com/cmacmackin/markdown-include/', 
  download_url = 'https://github.com/cmacmackin/markdown-include/tarball/v0.5.0',
  keywords = ['Markdown', 'typesetting', 'include', 'plugin', 'extension'],
  classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 5 - Production/Stable',

        # Indicate who your project is intended for
        'Intended Audience :: Developers',
        'Topic :: Internet :: WWW/HTTP :: Site Management',
        'Topic :: Software Development :: Documentation',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Text Processing :: Filters',
        'Topic :: Text Processing :: Markup :: HTML',

        # Pick your license as you wish (should match "license" above)
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
    ],
  install_requires = ['markdown']
)
