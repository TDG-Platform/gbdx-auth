# GBDX Oauth2 Tool

This is a simple python abstraction layer accessing the GBDX API via Oauth2

To install, run

```
git clone https://github.com/tdg-platform/authtool.git
cd TDGP-catalog-interface
python setup.py install
```

This will install the dependencies (requests and shapely) as well. You will want to have GEOS installed for shapely to be performant, it will look for a geos-config executable in your path when it is installed and link against it.

## Usage

Once installed, you can take it for a spin. The authentication is OAuth2 style. You will need a token from the TDGP Auth API.
See the file example_driver.py for a usage example, it'll look something like this:

```python
import os

from tdgp_catalog import config
from tdgp_catalog.query import Query

if __name__ == "__main__":

    # Build your query.
    query = Query("POLYGON ((-104 41, -103 41, -103 40, -104 40, -104 41))")
    query.add_filter("cloudCover < 10.0")
    query.add_filter("sensorPlatformName = 'WORLDVIEW02'")
    query.add_type("DigitalGlobeAcquisition")
    query.add_start_date('2014-01-01')
    query.add_end_date('2015-01-01')

    # Get the config (you can pass one in below if its not located at ~/.whackstack_config.ini)
	# session is an oauth2 enabled Session object like you find in the reqeusts package
    session = config.get_tdgp_session()

    # Run the query.
    results, stats, search_tag = query.run(session)
```

You should get back a dictionary packed full of fun stuff.

You can add filters and types to the query object via the `add_filter` and `add_type` methods.  To see options, install the Postman Chrome extension and import this guy:

https://www.getpostman.com/collections/f32a09a3a06e4433e635

You can restrict your search dates using the `add_start_date` and `add_end_date` methods.

### ini File

Various secrets are needed to actually hit the TDGP API.  These are found in a ini file that you pass into `get_tdgp_session`.  By default, it will look for ~/.whackstack_config.ini if you don't specify an explicit file to use.  The format should look like:

```
[tdgp]
auth_url = https://geobigdata.io/auth/v1/oauth/token/
client_id = your_client_id
client_secret = your_client_secret
user_name = your_user_name
user_password = your_password
```

You would be wise to make your ini file readable for you and only you!

You can add `catalog_url = https://geobigdata.io/catalog/v1/` if you need to change where the catalog lives (unlikely).  The config module has a method for fetching out that url, which you can pass to the `run` method on the query object.

Note that if you use `get_tdgp_session`, the token that is fetched is cached in the ini file under  a `[tdgp_token]` section.  If this section isn't present, a new token is fetched using your credentials.  If it is present, we don't ask for a new one.  Auto refreshing of the token should be enabled when using `get_tdgp_session`, and it will update the cached token on refresh.  

## Testing

You can run the tests using py.test from the package root directory via

```
py.test tests
```

Tests that query the actual platform will only run if you have a ~/.whackstack_config.ini file.  

Enjoy!
