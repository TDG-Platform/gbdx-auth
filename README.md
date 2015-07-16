# GBDX Oauth2 Tool

This is a simple python abstraction layer accessing the GBDX API via Oauth2

To install, run

```
pip install git+https://github.com/tdg-platform/authtool.git
```

## Usage

Once installed, set your ini file and make requests against the GBDX REST APIs:

```python
from gbdx_auth import gbdx_auth

# Get the config (you can pass one in below if its not located at ~/.gbdx-config)
# session is an oauth2 enabled Session object like you find in the reqeusts package
gbdx = gbdx_auth.get_session()

# GET the catalog heartbeat:
r = gbdx.get("https://geobigdata.io/workflows/v1/tasks")
task_list = r.json()
print task_list
```


### ini File

Various credentials are needed to actually hit the GBDX API.  These are found in a ini file that you pass into `get_session`.  By default, it will look for ~/.gbdx-config if you don't specify an explicit file to use.  The format should look like:

```
[gbdx]
auth_url = https://geobigdata.io/auth/v1/oauth/token/
client_id = your_client_id
client_secret = your_client_secret
user_name = your_user_name
user_password = your_password
```

Note that if you use `get_session`, the token that is fetched is cached in the ini file under  a `[gbdx_token]` section.  If this section isn't present, a new token is fetched using your credentials.  If it is present, we don't ask for a new one.  Auto refreshing of the token is enabled when using `get_session`, and it will update the cached token on refresh.  