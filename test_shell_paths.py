"""
Copyright 2019 ARC Centre of Excellence for Climate Systems Science
author: Aidan Heerdegen <aidan.heerdegen@anu.edu.au>
Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at
    http://www.apache.org/licenses/LICENSE-2.0
Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

import pytest
import sys, os, time, glob, re

bashvar = re.compile(r'\s*(\w+)=([\w|/]*)')
boguspathstart = '/ERROR/SET'

def find_and_test_paths(filepath):
    """
    Find all shell variable definitions that look like paths and check
    they are bogus
    """
    for line in open(filepath, 'r'):
        # Strip out all comments
        line = line.split('#')[0]
        m = bashvar.match(line)
        if m is not None:
            match = m.group(2)
            # Insist the match has at least one '/' character so we know
            # it is probably a path
            if '/' in match and not match.startswith(boguspathstart):
                msg = """Error in {file}.\nStart of shell path does not match {bogus}:\n{line}
                      """.format(file=filepath, bogus=boguspathstart, line=line)
                raise ValueError(msg) 
    
    return True
    
def test_all_shell_script_paths():

    print("")
    for filepath in glob.glob("*.sh"):
        print("Checking {}".format(filepath))
        assert(find_and_test_paths(filepath))
