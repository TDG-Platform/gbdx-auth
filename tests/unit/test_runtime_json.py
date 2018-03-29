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


class runtime_file_tests(unittest.TestCase):

    def test_session_from_runtime_invalid_jwt(self):
        # override the default location of a possible runtime file:
        gbdx_auth.GBDX_RUNTIME_FILE = 'tests/unit/data/runtime1.json'
        with self.assertRaises(Exception) as e:
            gbdx = gbdx_auth.get_session()

        gbdx_auth.GBDX_RUNTIME_FILE = '/mnt/work/gbdx_runtime.json'
        self.assertEqual( str(e.exception), 'Supplied GBDX access token is not a valid JWT.  Check GBDX_ACCESS_TOKEN env var or runtime.json')

    def test_session_from_runtime(self):
        # override the default location of a possible runtime file:
        gbdx_auth.GBDX_RUNTIME_FILE = 'tests/unit/data/runtime2.json'
        gbdx = gbdx_auth.get_session()
        gbdx_auth.GBDX_RUNTIME_FILE = '/mnt/work/gbdx_runtime.json'
        self.assertEqual( 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJPbmxpbmUgSldUIEJ1aWxkZXIiLCJpYXQiOjE1MjIzNDUzMDMsImV4cCI6MTU1Mzg4MTMwMywiYXVkIjoid3d3LmV4YW1wbGUuY29tIiwic3ViIjoianJvY2tldEBleGFtcGxlLmNvbSIsIkdpdmVuTmFtZSI6IkpvaG5ueSIsIlN1cm5hbWUiOiJSb2NrZXQiLCJFbWFpbCI6Impyb2NrZXRAZXhhbXBsZS5jb20iLCJSb2xlIjpbIk1hbmFnZXIiLCJQcm9qZWN0IEFkbWluaXN0cmF0b3IiXX0.iTYhRVtOLExk3q1ScRs_98lH-QBpLzgdFkhGepQOvtg', gbdx.token['access_token'] )



    ## TODO: run tests with missing / invalid creds, check for good error messages
