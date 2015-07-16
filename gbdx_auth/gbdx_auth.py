"""Some functions for interacting with GBDX end points."""
import os
import base64
import json
from ConfigParser import ConfigParser

from oauthlib.oauth2 import LegacyApplicationClient
from requests_oauthlib import OAuth2Session

def get_session(config_file=None):
    """Returns a requests session object with oauth enabled for
    interacting with GBDX end points."""
    
    def save_token(token_to_save):
        """Save off the token back to the config file."""
        if not 'gbdx_token' in set(cfg.sections()):
            cfg.add_section('gbdx_token')
        cfg.set('gbdx_token', 'json', json.dumps(token_to_save))
        with open(config_file, 'w') as sink:
            cfg.write(sink)

    # Read the config file (ini format).
    cfg = ConfigParser()
    if not config_file:
        config_file = os.path.expanduser('~/.gbdx-config')
    if not cfg.read(config_file):
        raise RuntimeError('No ini file found at {} to parse.'.format(config_file))

    client_id = cfg.get('gbdx', 'client_id')    
    client_secret = cfg.get('gbdx', 'client_secret')

    # See if we have a token stored in the config, and if not, get one.
    if 'gbdx_token' in set(cfg.sections()):
        # Parse the token from the config.
        token = json.loads(cfg.get('gbdx_token','json'))

        # Note that to use a token from the config, we have to set it
        # on the client and the session!
        s = OAuth2Session(client_id, client=LegacyApplicationClient(client_id, token=token),
                          auto_refresh_url=cfg.get('gbdx','auth_url'),
                          auto_refresh_kwargs={'client_id':client_id,
                                               'client_secret':client_secret},
                          token_updater=save_token)
        s.token = token
    else:
        # No pre-existing token, so we request one from the API.
        s = OAuth2Session(client_id, client=LegacyApplicationClient(client_id),
                          auto_refresh_url=cfg.get('gbdx','auth_url'),
                          auto_refresh_kwargs={'client_id':client_id,
                                               'client_secret':client_secret},
                          token_updater=save_token)

        # Get the token and save it to the config.
        headers = {"Authorization": "Basic "  + base64.b64encode(client_id + ':' + client_secret),
                   "Content-Type": "application/x-www-form-urlencoded"}
        token = s.fetch_token(cfg.get('gbdx','auth_url'), 
                              username=cfg.get('gbdx','user_name'),
                              password=cfg.get('gbdx','user_password'),
                              headers=headers)
        save_token(token)

    return s