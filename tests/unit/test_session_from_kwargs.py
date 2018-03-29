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


class session_from_kwargs_tests(unittest.TestCase):

    # @patch.object(gbdx_auth, 'session_from_existing_token')
    # def test_session_from_existing_env_var_token(self, mocked_session_from_existing_token):
    #     os.environ['GBDX_ACCESS_TOKEN'] = 'dummy-access-token-not-jwt'
    #     os.environ['GBDX_REFRESH_TOKEN'] = 'dummy-refresh-token'
    #     gbdx = gbdx_auth.get_session()
    #     self.assertTrue(mocked_session_from_existing_token.called)

    #     os.environ.pop('GBDX_ACCESS_TOKEN') 
    #     os.environ.pop('GBDX_REFRESH_TOKEN')

    # def test_session_from_existing_env_var_token2(self):
    #     # this is a dummy jwt that decodes successfully
    #     token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJPbmxpbmUgSldUIEJ1aWxkZXIiLCJpYXQiOjE1MjIzNDUzMDMsImV4cCI6MTU1Mzg4MTMwMywiYXVkIjoid3d3LmV4YW1wbGUuY29tIiwic3ViIjoianJvY2tldEBleGFtcGxlLmNvbSIsIkdpdmVuTmFtZSI6IkpvaG5ueSIsIlN1cm5hbWUiOiJSb2NrZXQiLCJFbWFpbCI6Impyb2NrZXRAZXhhbXBsZS5jb20iLCJSb2xlIjpbIk1hbmFnZXIiLCJQcm9qZWN0IEFkbWluaXN0cmF0b3IiXX0.iTYhRVtOLExk3q1ScRs_98lH-QBpLzgdFkhGepQOvtg'
    #     os.environ['GBDX_ACCESS_TOKEN'] = token
    #     os.environ['GBDX_REFRESH_TOKEN'] = 'dummy-refresh-token'
    #     gbdx = gbdx_auth.get_session()
    #     os.environ.pop('GBDX_ACCESS_TOKEN') 
    #     os.environ.pop('GBDX_REFRESH_TOKEN')

    #     self.assertEqual( token, gbdx.token['access_token'] )

    # def test_session_from_existing_env_var_token_invalid_jwt(self):
    #     os.environ['GBDX_ACCESS_TOKEN'] = 'dummy-access-token-not-jwt'
    #     os.environ['GBDX_REFRESH_TOKEN'] = 'dummy-refresh-token'
    #     with self.assertRaises(Exception) as e:
    #         gbdx = gbdx_auth.get_session()

    #     self.assertEqual( str(e.exception), 'Supplied GBDX access token is not a valid JWT.  Check GBDX_ACCESS_TOKEN env var or runtime.json')

    #     os.environ.pop('GBDX_ACCESS_TOKEN') 
    #     os.environ.pop('GBDX_REFRESH_TOKEN')

    # @patch.object(gbdx_auth, 'session_from_envvars')
    # @patch.object(gbdx_auth, 'session_from_config')  # need to mock this because it is a fallback, don't want to call it
    # def test_session_from_existing_env_var_user_pass_id_secret(self, mocked_session_from_config, mocked_session_from_envvars):
    #     os.environ['GBDX_USERNAME'] = 'dummy-username@digitalglobe.com'
    #     os.environ['GBDX_PASSWORD'] = 'dummy-password'
    #     os.environ['GBDX_CLIENT_ID'] = 'dummy-client_id'
    #     os.environ['GBDX_CLIENT_SECRET'] = 'dummy-secret'
    #     gbdx = gbdx_auth.get_session()
    #     self.assertTrue(mocked_session_from_envvars.called)

    #     os.environ.pop('GBDX_USERNAME') 
    #     os.environ.pop('GBDX_PASSWORD')
    #     os.environ.pop('GBDX_CLIENT_ID')
    #     os.environ.pop('GBDX_CLIENT_SECRET')

    # @vcr.use_cassette('tests/unit/cassettes/test_session_from_existing_env_var_user_pass_id_secret2.yaml')
    # def test_session_from_existing_env_var_user_pass_id_secret2(self):
    #     os.environ['GBDX_USERNAME'] = 'dummy-username@digitalglobe.com'
    #     os.environ['GBDX_PASSWORD'] = 'dummy-password'
    #     os.environ['GBDX_CLIENT_ID'] = 'dummy-client_id'
    #     os.environ['GBDX_CLIENT_SECRET'] = 'dummy-secret'
    #     with self.assertRaises(Exception) as e:
    #         gbdx = gbdx_auth.get_session()

    #     os.environ.pop('GBDX_USERNAME') 
    #     os.environ.pop('GBDX_PASSWORD')
    #     os.environ.pop('GBDX_CLIENT_ID')
    #     os.environ.pop('GBDX_CLIENT_SECRET')

    #     self.assertEqual( str(e.exception), 'Invalid GBDX credentials given in environment variables.')

    @vcr.use_cassette('tests/unit/cassettes/test_session_from_kwargs.yaml')
    def test_session_from_kwargs(self):
        username = 'asdf@digitalglobe.com'
        password = 'fdsa'
        client_id = 'dummy-client_id'
        client_secret = 'dummy-secret'
        gbdx = gbdx_auth.session_from_kwargs(username=username,
                                             password=password,
                                             client_id=client_id,
                                             client_secret=client_secret)

        token = 'dumdumdum'
        self.assertEqual( token, gbdx.token['access_token'] )

    @vcr.use_cassette('tests/unit/cassettes/test_session_from_kwargs_invalid_user_pass.yaml')
    def test_session_from_kwargs_invalid_user_pass(self):
        username = 'asdf@digitalglobe.com'
        password = 'fdsa'
        client_id = 'dummy-client_id'
        client_secret = 'dummy-secret'
        with self.assertRaises(Exception) as e:
            gbdx = gbdx_auth.session_from_kwargs(username=username,
                                             password=password,
                                             client_id=client_id,
                                             client_secret=client_secret)

        self.assertEqual( str(e.exception), 'Invalid credentials passed into session_from_kwargs()')

    @vcr.use_cassette('tests/unit/cassettes/test_session_from_kwargs_without_client_creds.yaml')
    def test_session_from_kwargs_without_client_creds(self):
        username = 'asdf@digitalglobe.com'
        password = 'fdsa'
        gbdx = gbdx_auth.session_from_kwargs(username=username,
                                             password=password)

        token = 'dumdumdum'
        self.assertEqual( token, gbdx.token['access_token'] )

    @vcr.use_cassette('tests/unit/cassettes/test_session_from_kwargs_invalid_user_pass_without_client_creds.yaml')
    def test_session_from_kwargs_invalid_user_pass_without_client_creds(self):
        username = 'asdf@digitalglobe.com'
        password = 'fdsa'
        with self.assertRaises(Exception) as e:
            gbdx = gbdx_auth.session_from_kwargs(username=username,
                                             password=password)

        self.assertEqual( str(e.exception), 'Invalid credentials passed into session_from_kwargs()')


    # @vcr.use_cassette('tests/unit/cassettes/test_session_from_existing_env_var_without_client_creds.yaml')
    # def test_session_from_existing_env_var_without_client_creds(self):
    #     os.environ['GBDX_USERNAME'] = 'asdf@digitalglobe.com'
    #     os.environ['GBDX_PASSWORD'] = 'fdsa'
    #     gbdx = gbdx_auth.get_session()

    #     os.environ.pop('GBDX_USERNAME') 
    #     os.environ.pop('GBDX_PASSWORD')
    #     token = 'dumdumdum'
    #     self.assertEqual( token, gbdx.token['access_token'] )

    # ## TODO: run tests with missing / invalid creds, check for good error messages
