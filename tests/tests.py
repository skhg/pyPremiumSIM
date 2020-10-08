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

if __name__ == '__main__':
    unittest.main()
