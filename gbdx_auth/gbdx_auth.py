"""Some functions for interacting with GBDX end points."""
from future import standard_library
standard_library.install_aliases()
import os
import base64
import json
from configparser import ConfigParser
from datetime import datetime
import jwt
from jwt.api_jwt import DecodeError
import sys

from oauthlib.oauth2 import LegacyApplicationClient
from requests_oauthlib import OAuth2Session

GBDX_RUNTIME_FILE='/mnt/work/gbdx_runtime.json'
SAVE_TOKEN = True # if false, never save the token back to the file

def session_from_existing_token(access_token, refresh_token="no_refresh_token", auth_url='https://geobigdata.io/auth/v1/oauth/token/'):
    """Returns a session with the GBDX authorization token baked in based on
    existing access_token and refresh_token.

    access_token - A GBDX access_token

    refresh_token - A GBDX refresh_token
    """
    def save_token(token):
        s.token = token

    # refresh_token is required parameter for OAuth2Session. Default
    #   refresh_token to "no_refresh_token" if none is provided. This allows
    #   session to be created with just an access token. Currently gbdx_runtime.json
    #   only provides an access token. In the future hopefully it will always
    #   provide both refresh_token and access_token
    #   TODO when gdbx does provide refresh token in gbdx_runtime, remove this
    #   default and require refresh_token as parameter to this function
    token = {"token_type": "Bearer", "refresh_token": refresh_token, "access_token": access_token, "scope": ["read", "write"], "expires_in": 604800, "expires_at": 0}

    # grab the expiration from the jwt access_token. Don't verify because
    # we dont care about source of token. GBDX auth endpoint will handle that.
    try:
        t = jwt.decode(access_token, verify=False)
    except DecodeError:
        raise Exception('Supplied GBDX access token is not a valid JWT.  Check GBDX_ACCESS_TOKEN env var or runtime.json')
    token['expires_at'] = t['exp']

    s = OAuth2Session(
            token=token,
            auto_refresh_url=auth_url,
            token_updater=save_token,
            )
    return s

def session_from_envvars(auth_url='https://geobigdata.io/auth/v1/oauth/token/',
                         environ_template=(('username', 'GBDX_USERNAME'),
                                           ('password', 'GBDX_PASSWORD'),
                                           ('client_id', 'GBDX_CLIENT_ID'),
                                           ('client_secret', 'GBDX_CLIENT_SECRET'))):
    """Returns a session with the GBDX authorization token baked in,
    pulling the credentials from environment variables.

    environ_template - An iterable of key, value pairs. The key should
                      be the variables used in the oauth workflow, and
                      the values being the environment variables to
                      pull the configuration from.  Change the
                      template values if your envvars differ from the
                      default, but make sure the keys remain the same.
    """
    def save_token(token):
        s.token = token

    environ = {var:os.environ[envvar] for var, envvar in environ_template}
    s = OAuth2Session(client=LegacyApplicationClient(environ['client_id']),
                      auto_refresh_url=auth_url,
                      auto_refresh_kwargs={'client_id':environ['client_id'],
                                           'client_secret':environ['client_secret']},
                      token_updater=save_token)

    s.fetch_token(auth_url, **environ)

    return s

def session_from_kwargs(**kwargs):
    def save_token(token):
        s.token = token
    auth_url='https://geobigdata.io/auth/v1/oauth/token/'
    s = OAuth2Session(client=LegacyApplicationClient(kwargs.get('client_id')),
                      auto_refresh_url=auth_url,
                      auto_refresh_kwargs={'client_id':kwargs.get('client_id'),
                                           'client_secret':kwargs.get('client_secret')},
                      token_updater=save_token)

    s.fetch_token(auth_url,
                  username=kwargs.get('username'),
                  password=kwargs.get('password'),
                  client_id=kwargs.get('client_id'),
                  client_secret=kwargs.get('client_secret'))
    return s


def expire_token(token_to_expire, config_file):
    """
    We want to expire tokens that return 401's under new auth, then re-try the original request which will trigger a new
    token
    :param token_to_expire:
    :param config_file
    :return:
    """
    if config_file:
        config_file = os.path.expanduser(config_file)
    else:
        config_file = os.path.expanduser('~/.gbdx-config')

    # Read the config file (ini format).
    cfg = ConfigParser()
    if not cfg.read(config_file):
        raise RuntimeError('No ini file found at {} to parse.'.format(config_file))

    if 'gbdx_token' not in set(cfg.sections()):
        cfg.add_section('gbdx_token')

    # reset expiration to force a new token request
    token_to_expire.update({"expires_at": 1})

    cfg.set('gbdx_token', 'json', json.dumps(token_to_expire))

    # write back token with expired token
    with open(config_file, 'w') as sink:
        cfg.write(sink)


def session_from_config(config_file):
    """Returns a requests session object with oauth enabled for
    interacting with GBDX end points."""

    def save_token(token_to_save):
        """Save off the token back to the config file."""
        if not SAVE_TOKEN:
            return
        if not 'gbdx_token' in set(cfg.sections()):
            cfg.add_section('gbdx_token')
        cfg.set('gbdx_token', 'json', json.dumps(token_to_save))
        with open(config_file, 'w') as sink:
            cfg.write(sink)

    # Read the config file (ini format).
    cfg = ConfigParser()
    if not cfg.read(config_file):
        raise RuntimeError('No ini file found at {} to parse.'.format(config_file))

    client_id = 'dummy_client_id(not-required)'
    client_secret = 'dummy_client_secret(not-required)'

    # See if we have a token stored in the config, and if not, get one.
    if 'gbdx_token' in set(cfg.sections()):
        # Parse the token from the config.
        token = json.loads(cfg.get('gbdx_token','json'))

        # Update the token experation with a little buffer room.
        token['expires_in'] = (datetime.utcfromtimestamp(token['expires_at']) -
                               datetime.utcnow()).total_seconds() - 600

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
        token = s.fetch_token(cfg.get('gbdx','auth_url'),
                              username=cfg.get('gbdx','user_name'),
                              password=cfg.get('gbdx','user_password'),
                              client_id=client_id,
                              client_secret=client_secret)
        save_token(token)

    return s

def get_session(config_file=None):
    """Returns a requests session with gbdx oauth2 baked in.

    If you provide GBDX_ACCESS_TOKEN and GBDX_REFRESH_TOKEN via env vars it will
    use those credentials. If GBDX_RUNTIME_FILE is defined with user_token in
    json object it will use those credentials. If you provide a path to a config
    file, it will look there for the credentials. If you don't it will try to
    pull the credentials from environment variables (GBDX_USERNAME, GBDX_PASSWORD,
    GBDX_CLIENT_ID, GBDX_CLIENT_SECRET).  If that fails and you have a
    '~/.gbdx-config' ini file, it will read from that.
    """

    if os.environ.get("GBDX_ACCESS_TOKEN", None):
        return session_from_existing_token(access_token=os.environ.get("GBDX_ACCESS_TOKEN", None), refresh_token=os.environ.get("GBDX_REFRESH_TOKEN", None))

    if os.path.isfile(GBDX_RUNTIME_FILE):
        with open(GBDX_RUNTIME_FILE) as f:
            runtime_json = json.loads(f.read())

        if runtime_json.get('user_token', None):
            return session_from_existing_token(access_token=runtime_json['user_token'])

    # If not config file, try using environment variables.  If that
    # fails and there is a config in the default location, use that.
    if not config_file:
        try:
            return session_from_envvars()
        except Exception as e:
            config_file = os.path.expanduser('~/.gbdx-config')

    error_output = """[gbdx]
auth_url = https://geobigdata.io/auth/v1/oauth/token/
client_id = your_client_id
client_secret = your_client_secret
user_name = your_user_name
user_password = your_password"""

    if not os.path.isfile(config_file):
        raise Exception("Please create a GBDX credential file at ~/.gbdx-config with these contents:\n%s" % error_output)

    try:
      session = session_from_config(config_file)
    except:
      raise Exception("Invalid credentials or incorrectly formated config file at ~/.gbdx-config")

    return session
