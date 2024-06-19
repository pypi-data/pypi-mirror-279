import unittest
from Authentication.services.impl.sdk_authenticate_service_impl import User
from Authentication.exception.authenticate_exception import InvalidCredentialsError, TokenRequestError


class TestUserServiceIntegration(unittest.TestCase):

    def setUp(self):
        self.client_instance = User()
        self.invalid_username = "invalid_username"
        self.invalid_password = "invalid_password"

    def test_get_token_with_invalid_credentials(self):
        with self.assertRaises(TokenRequestError) as context:
            self.client_instance.get_token(self.invalid_username, self.invalid_password)

        self.assertEqual(context.exception.status_code, 401)
        print("Caught TokenRequestError with status code:", context.exception.status_code)

    def test_get_token_with_missing_credentials(self):
        with self.assertRaises(InvalidCredentialsError):
            self.client_instance.get_token(None, "")

        with self.assertRaises(InvalidCredentialsError):
            self.client_instance.get_token("", None)

        with self.assertRaises(InvalidCredentialsError):
            self.client_instance.get_token(None, None)

        with self.assertRaises(InvalidCredentialsError):
            self.client_instance.get_refresh_token("")

        with self.assertRaises(InvalidCredentialsError):
            self.client_instance.get_refresh_token(None)


if __name__ == '__main__':
    unittest.main()
