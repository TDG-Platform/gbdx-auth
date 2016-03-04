# GBDX Oauth2 Tool

This is a simple python abstraction layer accessing the GBDX API via Oauth2

Current version: 0.1.0

To install, run

```
pip install git+https://github.com/tdg-platform/gbdx-auth.git
```

Or if you are inside the DG Network:
```
pip install git+https://github.digitalglobe.com/gbdx/gbdx-auth.git
```

## Usage

Once installed, set your ini file and make requests against the GBDX REST APIs:

```python
from gbdx_auth import gbdx_auth

# Get the config.  If you pass a path to your ini file as an argument
# to get_session, it will use that to pull the config.  If you provide
# nothing, it will first try to pull the config from the environment
# variables GBDX_USERNAME, GBDX_PASSWORD, GBDX_CLIENT_ID, and
# GBDX_CLIENT_SECRET.  If those don't exist, it will try to pull from
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

### ini File

Various credentials are needed to actually hit the GBDX API.  These are found in a ini file that you pass into `get_session`.  By default, it will first look for environment variables (GBDX_USERNAME, GBDX_PASSWORD, GBDX_CLIENT_ID, and GBDX_CLIENT_SECRET) and then look for ~/.gbdx-config if you don't specify an explicit file to use.  The format should look like:

```
[gbdx]
auth_url = https://geobigdata.io/auth/v1/oauth/token/
client_id = your_client_id
client_secret = your_client_secret
user_name = your_user_name
user_password = your_password
```

Note that if you use `get_session`, the token that is fetched is cached in the ini file under  a `[gbdx_token]` section, unless the credentials were pulled from environment variables.  If this section isn't present, a new token is fetched using your credentials.  If it is present, we don't ask for a new one.  Auto refreshing of the token is enabled when using `get_session`, and it will update the cached token on refresh.  
