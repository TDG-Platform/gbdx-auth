import os

from gbdx_auth import gbdx_auth

# Get the config (you can pass one in below if its not located at ~/.gbdx-config)
# session is an oauth2 enabled Session object like you find in the reqeusts package
gbdx = gbdx_auth.get_session()

# GET the catalog heartbeat:
r = gbdx.get("https://geobigdata.io/workflows/v1/tasks")
task_list = r.json()
print task_list