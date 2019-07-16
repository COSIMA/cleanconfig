[![Build Status](https://travis-ci.org/coecms/esm-pre-industrial.svg?branch=master)](https://travis-ci.org/coecms/esm-pre-industrial)

## Test Config

This is a small test suite to make sure `payu` configuration files are suitable for cloning and running for any user.

Specifically this was designed for published experiment configurations from [COSIMA](https://github.com/COSIMA?language=shell)

To use:

1. Add the following lines to a `.travis.yml` file for a configuration repository:

```yaml
language: python

python:
    - '3.6'

git:
    depth: 3
    quiet: true

install:
    - pip install pytest pyyaml

env:
  global:
    - CCONF_DIR=${TRAVIS_BUILD_DIR}

before_script:
    - git clone https://github.com/COSIMA/cleanconfig.git

script:
    - (cd cleanconfig && pytest test.py)
```

Or copy [directly from an example repository](https://github.com/COSIMA/1deg_jra55_iaf/blob/master/.travis.yml)

2. Turn on Travis CI for the configuration repository

3. Customise tests?

It is possible to customise which tests are run in your `.travis.yml` file. The details are in the
[pytest documentation](https://docs.pytest.org/en/latest/example/markers.html), but briefly tests
can specified using the `-k` option to `pytest`, e.g.
```yaml
script:
    - (cd cleanconfig && pytest -s -k abs test.py)
```
will run all tests with `abs` in the name, which is tests that enforce absolute paths

Tests that have a marker can be selected with the `-m` option:
```yaml
script:
    - (cd cleanconfig && pytest -s -m basic test.py)
```
will run all tests marked as `basic`.

There is another, rather specialised, test which will read all shell scripts (files ending in `.sh`)
and check that all paths defined in the script are deliberately bogus. This is defined by the path
beginning with `/ERROR/SET`. This is because scripts like this are generally for synching data to 
another location. So a user cannot accidentally overwrite existing data inadvertently if the paths
are not valid.

This test can be invoked by adding the line
````
    - pytest -s cleanconfig/test_shell_paths.py
````
to the `script` section of the `travis.yml` file
