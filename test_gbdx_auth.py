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