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
fms = False

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

    global model_config, fms

    if verbose: print ("setup_module      module:%s" % module.__name__)
    if verbose: print ("Python version: {}".format(sys.version))

    confdir = os.environ.get('CCONF_DIR', '.')

    confpath = os.path.join(confdir,'config.yaml')

    model_config = readconfig(confpath)

    print('Reading config file: {}'.format(confpath))

    if verbose: print(model_config)
 
    fms_models = {'access', 'access-om2', 'access-esm', 'mom', 'mom6'}
    fms = model_config['model'].lower() not in fms_models;

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
    """ Input directories must be absolute, and pointing some shared space"""
    for dir in insist_array(model_config.get('input', [])):
        if not os.path.isabs(dir):
            pytest.fail("input should be absolute: \ninput: {}".format(dir))

def test_submodel_absinputs():
    """ Input directories must be absolute, and pointing some shared space"""
    for model in model_config.get('submodels',[]):
        for dir in insist_array(model.get('input', [])):
            if not os.path.isabs(dir):
                pytest.fail("input for submodel {} should be absolute: \ninput: {}".format(model['name'], dir))

def test_submodel_executable_abspaths():
    """Model executables should always be absolute paths for published configs"""
    if 'exe' in model_config and not os.path.isabs(model_config['exe']):
        pytest.fail("executable for model should be absolute: \nexe: {}".format(model_config['exe']))
    for model in model_config.get('submodels',[]):
        if 'exe' not in model or not os.path.isabs(model['exe']):
            pytest.fail("executable for submodel {} should be absolute: \nexe: {}".format(model['name'], model['exe']))

def test_collate_dict():
    """Enforce the new dictionary mehod for defining collate options""" 
    cconf = model_config.get('collate',None)
    if cconf is not None and type(cconf) is bool:
        pytest.fail("Collate config should be updated to a dictionary")

def test_collate_executable_abspath():
    """Collate executable should be defined and an absolute path as new users will not have
       this in their path. Should check for model type """

    # Would like to use a decorator for this, but skipif can't be dynamically set
    if fms: pytest.skip('Not a valid test for non FMS models')

    cconf = model_config.get('collate',None)
    if cconf is None or 'exe' not in cconf:
        pytest.fail("Collate executable must be defined")
    if not os.path.isabs(cconf['exe']):
        pytest.fail("Collate executable must be an absolute path")

def test_collate_flags():
    """Best practice is to use default settings for collate flags"""
    cconf = model_config.get('collate',None)
    if cconf is not None and 'flags' in cconf:
        pytest.fail("Custom collate flags should not be defined")







