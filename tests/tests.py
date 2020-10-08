import unittest
import sys
from pypremiumsim import PremiumSimSession

sampledatadir = "./tests/sampledata/"


class TestLoginMethod(unittest.TestCase):

    def test_extract_csrf_gets_token(self):
        session = PremiumSimSession()

        with(open(sampledatadir + "login_page.html", "rb")) as f:
            login_page = f.read()

            csrf = session._PremiumSimSession__get_csrf_for_login(login_page)

            self.assertEqual(csrf, "dlGf6vnkuJo3PHony6q34k9pjvBACb9af0bLruyjxRw")

    def test_handle_login_response_good_response_returns_true(self):
        session = PremiumSimSession()

        with(open(sampledatadir + "start_page.html", "rb")) as f:
            good_login = f.read()

            loginOk = session._PremiumSimSession__handle_login_response(good_login)

            self.assertTrue(loginOk)

    def test_handle_login_response_wrong_credentials_throws(self):
        session = PremiumSimSession()

        with(open(sampledatadir + "login_failed_page.html", "rb")) as f:
            failed_login = f.read()

            with self.assertRaises(IOError) as context:
                session._PremiumSimSession__handle_login_response(failed_login)

            self.assertTrue('Your credentials are incorrect' in str(context.exception))

if __name__ == '__main__':
    unittest.main()
