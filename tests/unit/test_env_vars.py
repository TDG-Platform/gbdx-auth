from gbdx_auth import gbdx_auth
import vcr
import unittest
from mock import patch
import os
from jwt.api_jwt import DecodeError

"""
How to use vcr to create unit tests:
1. Add a new test that is dependent upon actually hitting GBDX APIs.
2. Decorate the test with @vcr appropriately, supply a yaml file path to gbdx-auth/tests/unit/cassettes
    note: a yaml file will be created after the test is run

3. Run the tests.  This will record a "cassette".
4. Edit the cassette to remove any possibly sensitive information (s3 creds for example)
"""


class env_var_tests(unittest.TestCase):

    @patch.object(gbdx_auth, 'session_from_existing_token')
    def test_session_from_existing_env_var_token(self, mocked_session_from_existing_token):
        os.environ['GBDX_ACCESS_TOKEN'] = 'dummy-access-token-not-jwt'
        os.environ['GBDX_REFRESH_TOKEN'] = 'dummy-refresh-token'
        gbdx = gbdx_auth.get_session()
        self.assertTrue(mocked_session_from_existing_token.called)

        os.environ.pop('GBDX_ACCESS_TOKEN') 
        os.environ.pop('GBDX_REFRESH_TOKEN')

    def test_session_from_existing_env_var_token_invalid_jwt(self):
        os.environ['GBDX_ACCESS_TOKEN'] = 'dummy-access-token-not-jwt'
        os.environ['GBDX_REFRESH_TOKEN'] = 'dummy-refresh-token'
        with self.assertRaises(Exception) as e:
            gbdx = gbdx_auth.get_session()

        self.assertEqual( e.exception.message, 'Supplied GBDX access token is not a valid JWT.  Check GBDX_ACCESS_TOKEN env var or runtime.json')

        os.environ.pop('GBDX_ACCESS_TOKEN') 
        os.environ.pop('GBDX_REFRESH_TOKEN')

    # def test_session_from_existing_ini_file_token2(self):
    #     inifile = 'tests/unit/data/config_ini_with_token.txt'
    #     gbdx = gbdx_auth.get_session(config_file=inifile)
    #     self.assertEqual('super-dummy-access-token',gbdx.token['access_token'])

    # @vcr.use_cassette('tests/unit/cassettes/test_session_from_existing_ini_file_user_pass.yaml', filter_headers=['authorization'])
    # def test_session_from_existing_ini_file_user_pass(self):
    #     gbdx_auth.SAVE_TOKEN = False
    #     inifile = 'tests/unit/data/config_ini_with_user_pass.txt'
    #     gbdx = gbdx_auth.get_session(config_file=inifile)
    #     self.assertEqual('dumdumdum',gbdx.token['access_token'])
    #     gbdx_auth.SAVE_TOKEN = True

    # @patch.object(gbdx_auth, 'session_from_config')
    # def test_session_from_existing_ini_file_user_pass2(self, mocked_session_from_config):
    #     inifile = 'tests/unit/data/config_ini_with_user_pass.txt'
    #     gbdx = gbdx_auth.get_session(config_file=inifile)
    #     self.assertTrue(mocked_session_from_config.called)


    ## TODO: run tests with missing / invalid creds, check for good error messages
