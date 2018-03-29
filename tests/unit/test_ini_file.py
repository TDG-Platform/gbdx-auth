from gbdx_auth import gbdx_auth
import vcr
import unittest
from mock import patch

"""
How to use vcr to create unit tests:
1. Add a new test that is dependent upon actually hitting GBDX APIs.
2. Decorate the test with @vcr appropriately, supply a yaml file path to gbdx-auth/tests/unit/cassettes
    note: a yaml file will be created after the test is run

3. Run the tests.  This will record a "cassette".
4. Edit the cassette to remove any possibly sensitive information (s3 creds for example)
"""


class ini_file_tests(unittest.TestCase):

    @patch.object(gbdx_auth, 'session_from_config')
    def test_session_from_existing_ini_file_token(self, mocked_session_from_config):
        inifile = 'tests/unit/data/config_ini_with_token.txt'
        gbdx = gbdx_auth.get_session(config_file=inifile)
        self.assertTrue(mocked_session_from_config.called)

    def test_session_from_existing_ini_file_token2(self):
        inifile = 'tests/unit/data/config_ini_with_token.txt'
        gbdx = gbdx_auth.get_session(config_file=inifile)
        self.assertEqual('super-dummy-access-token',gbdx.token['access_token'])

    @vcr.use_cassette('tests/unit/cassettes/test_session_from_existing_ini_file_user_pass.yaml', filter_headers=['authorization'])
    def test_session_from_existing_ini_file_user_pass(self):
        gbdx_auth.SAVE_TOKEN = False  # prevent the test config file from getting written to
        inifile = 'tests/unit/data/config_ini_with_user_pass.txt'
        gbdx = gbdx_auth.get_session(config_file=inifile)
        self.assertEqual('dumdumdum',gbdx.token['access_token'])
        gbdx_auth.SAVE_TOKEN = True

    @patch.object(gbdx_auth, 'session_from_config')
    def test_session_from_existing_ini_file_user_pass2(self, mocked_session_from_config):
        inifile = 'tests/unit/data/config_ini_with_user_pass.txt'
        gbdx = gbdx_auth.get_session(config_file=inifile)
        self.assertTrue(mocked_session_from_config.called)


    ## TODO: run tests with missing / invalid creds, check for good error messages
