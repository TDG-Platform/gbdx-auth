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

    def test_session_from_existing_env_var_token2(self):
        # this is a dummy jwt that decodes successfully
        token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJPbmxpbmUgSldUIEJ1aWxkZXIiLCJpYXQiOjE1MjIzNDUzMDMsImV4cCI6MTU1Mzg4MTMwMywiYXVkIjoid3d3LmV4YW1wbGUuY29tIiwic3ViIjoianJvY2tldEBleGFtcGxlLmNvbSIsIkdpdmVuTmFtZSI6IkpvaG5ueSIsIlN1cm5hbWUiOiJSb2NrZXQiLCJFbWFpbCI6Impyb2NrZXRAZXhhbXBsZS5jb20iLCJSb2xlIjpbIk1hbmFnZXIiLCJQcm9qZWN0IEFkbWluaXN0cmF0b3IiXX0.iTYhRVtOLExk3q1ScRs_98lH-QBpLzgdFkhGepQOvtg'
        os.environ['GBDX_ACCESS_TOKEN'] = token
        os.environ['GBDX_REFRESH_TOKEN'] = 'dummy-refresh-token'
        gbdx = gbdx_auth.get_session()
        os.environ.pop('GBDX_ACCESS_TOKEN') 
        os.environ.pop('GBDX_REFRESH_TOKEN')

        self.assertEqual( token, gbdx.token['access_token'] )

    def test_session_from_existing_env_var_token_invalid_jwt(self):
        os.environ['GBDX_ACCESS_TOKEN'] = 'dummy-access-token-not-jwt'
        os.environ['GBDX_REFRESH_TOKEN'] = 'dummy-refresh-token'
        with self.assertRaises(Exception) as e:
            gbdx = gbdx_auth.get_session()

        self.assertEqual( str(e.exception), 'Supplied GBDX access token is not a valid JWT.  Check GBDX_ACCESS_TOKEN env var or runtime.json')

        os.environ.pop('GBDX_ACCESS_TOKEN') 
        os.environ.pop('GBDX_REFRESH_TOKEN')


    ## TODO: run tests with missing / invalid creds, check for good error messages
