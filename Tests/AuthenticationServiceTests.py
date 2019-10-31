import unittest
from Services.AuthenticationService import Authentication


service = Authentication()

class TestAuthenticationService(unittest.TestCase):

    def test_validPassword(self):
        self.assertTrue(service.authenticate(""))