from Authentication.constants.token_constants import USERNAME_OR_PASSWORD_MISSING


class InvalidCredentialsError(Exception):
        def __init__(self, message=USERNAME_OR_PASSWORD_MISSING, status_code=400):
            super().__init__(f"HTTP {status_code}: {message}")
            self.status_code = status_code



class TokenRequestError(Exception):
    def __init__(self, status_code, message):
        super().__init__(f"HTTP {status_code}: {message}")
        self.status_code = status_code


class DNSResolutionError(Exception):
    def __init__(self, host, original_exception):
        super().__init__(f"Failed to resolve DNS for host '{host}': {original_exception}")


class PropertyNotFoundError(Exception):
    pass
