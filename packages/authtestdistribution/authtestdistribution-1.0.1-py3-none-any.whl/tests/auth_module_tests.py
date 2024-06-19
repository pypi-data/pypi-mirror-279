import unittest
from Authentication.services.impl.sdk_authenticate_service_impl import User


class TestUserServiceIntegration(unittest.TestCase):

    def setUp(self):
        self.client_instance = User()
        self.username = "--username--"
        self.password = "--password--"

    def test_get_token(self):
        token_response = self.client_instance.get_token(self.username, self.password)

        self.assertIn('access_token', token_response, "Access token not found in the response")
        self.assertIsNotNone(token_response.get('access_token'), "Access token is None")
        print("Access Token:", token_response.get('access_token'))

    def test_get_refresh_token(self):
        token_response = self.client_instance.get_token(self.username, self.password)
        self.assertIn('refresh_token', token_response, "Refresh token not found in the initial response")
        refresh_token = token_response.get('refresh_token')

        refresh_token_response = self.client_instance.get_refresh_token(refresh_token)

        self.assertIn('access_token', refresh_token_response, "Access token not found in the refresh token response")
        self.assertIsNotNone(refresh_token_response.get('access_token'), "Access token is None after refresh")
        print("New Access Token Using Refresh Token:", refresh_token_response.get('access_token'))


if __name__ == '__main__':
    unittest.main()
