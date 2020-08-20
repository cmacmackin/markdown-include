#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  include.py
#
#  Copyright 2015 Christopher MacMackin <cmacmackin@gmail.com>
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#
#

from __future__ import print_function
import re
import os.path
from codecs import open
from markdown.extensions import Extension
from markdown.preprocessors import Preprocessor

INC_SYNTAX = re.compile(r'\{!\s*(.+?)\s*!\}')
HEADING_SYNTAX = re.compile( '^#+' )


class MarkdownInclude(Extension):
    def __init__(self, configs={}):
        self.config = {
            'base_path': ['.', 'Default location from which to evaluate ' \
                'relative paths for the include statement.'],
            'encoding': ['utf-8', 'Encoding of the files used by the include ' \
                'statement.'],
            'inheritHeadingDepth': [False, 'Increases headings on included ' \
                'file by amount of previous heading (combines with '\
                'headingOffset option).'],
            'headingOffset': [0, 'Increases heading depth by a specific ' \
                'amount (and the inheritHeadingDepth option).  Defaults to 0.'],
            'throwException': [False, 'When true, if the extension is unable '\
                                'to find an included file it will throw an '\
                                'exception which the user can catch. If false '\
                                '(default), a warning will be printed and '\
                                'Markdown will continue parsing the file.']
        }
        for key, value in configs.items():
            self.setConfig(key, value)

    def extendMarkdown(self, md, md_globals):
        md.preprocessors.register(IncludePreprocessor(md,self.getConfigs()), 'include', 101)


class IncludePreprocessor(Preprocessor):
    '''
    This provides an "include" function for Markdown, similar to that found in
    LaTeX (also the C pre-processor and Fortran). The syntax is {!filename!},
    which will be replaced by the contents of filename. Any such statements in
    filename will also be replaced. This replacement is done prior to any other
    Markdown processing. All file-names are evaluated relative to the location
    from which Markdown is being called.
    '''
    def __init__(self, md, config):
        super(IncludePreprocessor, self).__init__(md)
        self.base_path = config['base_path']
        self.encoding = config['encoding']
        self.inheritHeadingDepth = config['inheritHeadingDepth']
        self.headingOffset = config['headingOffset']
        self.throwException = config['throwException']

    def run(self, lines):
        done = False
        bonusHeading = ''
        while not done:
            for loc, line in enumerate(lines):
                m = INC_SYNTAX.search(line)

                if m:
                    filename = m.group(1)
                    filename = os.path.expanduser(filename)
                    if not os.path.isabs(filename):
                        filename = os.path.normpath(
                            os.path.join(self.base_path,filename)
                        )
                    try:
                        with open(filename, 'r', encoding=self.encoding) as r:
                            text = r.readlines()
                            
                    except Exception as e:
                        if not self.throwException:
                            print('Warning: could not find file {}. Ignoring '
                                  'include statement. Error: {}'.format(filename, e))
                            lines[loc] = INC_SYNTAX.sub('',line)
                            break
                        else:
                            raise e

                    line_split = INC_SYNTAX.split(line)
                    if len(text) == 0:
                        text.append('')
                    for i in range(len(text)):
                        # Strip the newline, and optionally increase header depth
                        if self.inheritHeadingDepth or self.headingOffset:
                            if HEADING_SYNTAX.search(text[i]):
                                text[i] = text[i].rstrip('\r\n')
                                if self.inheritHeadingDepth:
                                    text[i] = bonusHeading + text[i]
                                if self.headingOffset:
                                    text[i] = '#' * self.headingOffset + text[i]
                        else:
                            text[i] = text[i].rstrip('\r\n')
                            
                    text[0] = line_split[0] + text[0]
                    text[-1] = text[-1] + line_split[2]
                    lines = lines[:loc] + text + lines[loc+1:]
                    break
                    
                else:
                    h = HEADING_SYNTAX.search(line)
                    if h:
                        headingDepth = len(h.group(0))
                        bonusHeading = '#' * headingDepth
                
            else:
                done = True
        return lines


def makeExtension(*args,**kwargs):
    return MarkdownInclude(kwargs)
