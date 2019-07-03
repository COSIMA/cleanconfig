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

from __future__ import print_function

import pytest
import sys, os, time, glob
import shutil

import yaml

verbose = False
model_config = {}

def insist_array(str_or_array):
    if type(str_or_array) == str:
        str_or_array = [ str_or_array, ]
    return str_or_array

def readconfig(config_fname):
    """Parse input configuration file and return a config dict."""

    with open(config_fname, 'r') as config_file:
        config = yaml.safe_load(config_file)

    return config

def setup_module(module):

    global model_config

    if verbose: print ("setup_module      module:%s" % module.__name__)
    if verbose: print ("Python version: {}".format(sys.version))

    confdir = os.environ.get('CCONF_DIR', '.')

    confpath = os.path.join(confdir,'config.yaml')

    model_config = readconfig(confpath)

    print('Reading config file: {}'.format(confpath))

    if verbose: print(model_config)
 
@pytest.mark.basic
def test_project():

    if 'project' in model_config:
        pytest.fail("project should not be defined: \nproject: {}".format(model_config['project']))

@pytest.mark.basic
def test_shortpath():

    if 'shortpath' in model_config:
        pytest.fail("shortpath should not be defined: \nshortpath: {}".format(model_config['shortpath']))

@pytest.mark.basic
def test_postscript():

    if 'postscript' in model_config:
        pytest.fail("postscript should not be defined: \npostscript: {}".format(model_config['postscript']))

def test_rellab():

    if 'laboratory' in model_config:
        if os.path.isabs(model_config['laboratory']):
            pytest.fail("laboratory should not be absolute: \nlaboratory: {}".format(model_config['laboratory']))

def test_absinputs():

    # Input directories must be absolute, and pointing some shared space
    for dir in insist_array(model_config.get('input', [])):
        if not os.path.isabs(dir):
            pytest.fail("input should be absolute: \ninput: {}".format(dir))


def test_submodel_absinputs():

    for model in model_config.get('submodels',[]):
        # Input directories must be absolute, and pointing some shared space
        for dir in insist_array(model.get('input', [])):
            if not os.path.isabs(dir):
                pytest.fail("input for submodel {} should be absolute: \ninput: {}".format(model['name'], dir))

def test_submodel_executable_abspaths():

    for model in model_config.get('submodels',[]):
        if not os.path.isabs(model['exe']):
            pytest.fail("executable for submodel {} should be absolute: \nexe: {}".format(model['name'], model['exe']))

def test_collate_options():

    cconf = model_config.get('collate','')

    if type(cconf) is bool:
        pytest.fail("Collate config should be updated to a dictionary")




