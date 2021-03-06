[![Build Status](https://travis-ci.org/TDG-Platform/gbdx-auth.svg?branch=master)](https://travis-ci.org/TDG-Platform/gbdx-auth)
[![PyPI version](https://badge.fury.io/py/gbdx-auth.svg)](https://badge.fury.io/py/gbdx-auth)
[![Conda version](https://anaconda.org/digitalglobe/gbdx-auth/badges/version.svg)](https://anaconda.org/digitalglobe/gbdx-auth)
[![Updates](https://pyup.io/repos/github/TDG-Platform/gbdx-auth/shield.svg)](https://pyup.io/repos/github/TDG-Platform/gbdx-auth/)
[![Codecov.io](https://codecov.io/gh/TDG-Platform/gbdx-auth/branch/master/graph/badge.svg)](https://codecov.io/gh/TDG-Platform/gbdx-auth)

# GBDX Oauth2 Tool

This is a simple python abstraction layer accessing the GBDX API via Oauth2

Current version: 0.4.0

To install, run

```
pip install gbdx-auth
```


## Usage

Once installed, set your ini file and make requests against the GBDX REST APIs:

```python
from gbdx_auth import gbdx_auth

# Get the config.  If you pass a path to your ini file as an argument
# to get_session, it will use that to pull the config.  If you provide
# nothing, it will first try to pull the config from the environment
# variables GBDX_USERNAME and GBDX_PASSWORD.  If those don't exist, it will try to pull from
# an ini file at ~/.gbdx-config, if it exists.
#
# There are a couple other methods in gbdx_auth for getting a session.
#
# gbdx is an oauth2 enabled Session object like you find in the
# reqeusts package
# (http://docs.python-requests.org/en/latest/user/advanced/).
gbdx = gbdx_auth.get_session()

# GET the set of workflow tasks:
r = gbdx.get("https://geobigdata.io/workflows/v1/tasks")
task_list = r.json()
print task_list
```

You can also pass credentials explicitly if desired:

```python
gbdx = gbdx_auth.session_from_kwargs(username='<your-username>',
                                     password='<your-password>')
```

### ini File

Various credentials are needed to actually hit the GBDX API.  These are found in a ini file that you pass into `get_session`.  By default, it will first look for environment variables (GBDX_USERNAME, GBDX_PASSWORD) and then look for ~/.gbdx-config if you don't specify an explicit file to use.  The format should look like:

```
[gbdx]
user_name = your_user_name
user_password = your_password
```

Note that if you use `get_session`, the token that is fetched is cached in the ini file under  a `[gbdx_token]` section, unless the credentials were pulled from environment variables.  If this section isn't present, a new token is fetched using your credentials.  If it is present, we don't ask for a new one.  Auto refreshing of the token is enabled when using `get_session`, and it will update the cached token on refresh.


## Development

DigitalGlobe hosts a conda build for this package: https://anaconda.org/digitalglobe/gbdx-auth 

To produce this build:

1. conda build -c conda-forge -c digitalglobe .
2. anaconda upload --user digitalglobe {file from step1}

