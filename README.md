## Test Config

This is a small test suite to make sure `payu` configuration files are suitable for cloning and running for any user.

Specifically this was designed for published experiment configurations from [COSIMA](https://github.com/COSIMA?language=shell)

To use:

1. Add the following lines to a `.travis.yaml` file for a configuration repository:

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