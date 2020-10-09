import unittest
from pypremiumsim import PremiumSimSession, DataVolume

sampledatadir = "./tests/sampledata/"


class TestLoginMethod(unittest.TestCase):

    def test_extract_csrf_gets_token(self):
        session = PremiumSimSession()

        with(open(sampledatadir + "login_page.html", "rb")) as f:
            login_page = f.read()

            csrf = session._PremiumSimSession__get_csrf_for_login(login_page)

            self.assertEqual(csrf, "TWtsHpuDAK6BCvFqQJhQNQtK_ffHfvwiVkkXeLmyvcg")

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

    def test_handle_data_usage_response_parses_content(self):
        session = PremiumSimSession()

        with(open(sampledatadir + "data_usage_page.html", "r")) as f:
            page = f.read()
            result = session._PremiumSimSession__handle_data_usage_response(page)

            expected = DataVolume(u"20,00 GB", u"749,04 MB", u"3,7 %")

            self.assertEqual(result.__dict__, expected.__dict__)

if __name__ == '__main__':
    unittest.main()
