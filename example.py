import os

from gbdx_auth import gbdx_auth

# Get the config (you can pass one in below if its not located at ~/.gbdx-config)
# session is an oauth2 enabled Session object like you find in the reqeusts package
session = gbdx_auth.get_session()

# GET the catalog heartbeat:
results, stats, search_tag = query.run(session)

# List GBDX Tasks:
