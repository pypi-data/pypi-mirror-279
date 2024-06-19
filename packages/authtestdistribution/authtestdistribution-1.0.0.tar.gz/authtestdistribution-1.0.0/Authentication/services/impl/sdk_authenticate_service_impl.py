import hashlib
import logging
import time

import requests
import urllib3

from Authentication.constants.caching_constants import EXPIRES_AT
from Authentication.constants.config_constants import REFRESH_TOKEN_ENDPOINT, TOKEN_ENDPOINT, BEARER_URL, SDK
from Authentication.constants.token_constants import TokenServiceConstants, RESPONSE, PASSWORD, USERNAME, \
    REFRESH_TOKEN
from Authentication.exception.authenticate_exception import TokenRequestError, \
    DNSResolutionError, InvalidCredentialsError
from Authentication.model.token_response import TokenResponse
from Authentication.services.sdk_authenticate_service import SDKAuthenticate
from Authentication.services.support.rest_gateway_support import create_rest_template
from Authentication.util.property_util import PropertyUtils

logger = logging.getLogger(__name__)


class User(SDKAuthenticate):

    def __init__(self):
        super().__init__()
        self._password = None
        self._username = None
        bearer_url = PropertyUtils.get_property(SDK, BEARER_URL)
        token_endpoint = PropertyUtils.get_property(SDK, TOKEN_ENDPOINT)
        refresh_token_endpoint = PropertyUtils.get_property(SDK, REFRESH_TOKEN_ENDPOINT)
        self._api_url = bearer_url + token_endpoint
        self._api_refresh_url = bearer_url + refresh_token_endpoint
        self._headers = TokenServiceConstants.HEADERS

    def get_token(self, username, password, proxy=None):

        cached_response = self.__validate(username, password)
        if cached_response:
            logger.info("Using cached token for %s", username)
            return cached_response[RESPONSE]

        self._username, self._password = username, password

        response = self.__request_token(username, password, proxy)
        return response

    def get_refresh_token(self, refresh_token, proxy=None):
        cached_response = self.__validate_refresh_token(refresh_token)
        if cached_response:
            logger.info("Using cached refresh token")
            return cached_response[RESPONSE]

        response = self.__request_refresh_token(refresh_token, proxy)
        return response

    def __validate(self, username, password):
        if not username or not password:
            raise InvalidCredentialsError()

        cache_key = self.__generate_cache_key(username, password)
        if cache_key in self._token_map:
            token_info = self._token_map[cache_key]
            if EXPIRES_AT in token_info and token_info[EXPIRES_AT] > time.time():
                return token_info
        return None

    def __validate_refresh_token(self, refresh_token):
        if not refresh_token:
            raise InvalidCredentialsError()

        if refresh_token in self._token_map:
            token_info = self._token_map[refresh_token]
            if EXPIRES_AT in token_info and token_info[EXPIRES_AT] > time.time():
                return token_info
        return None
    def __request_token(self, username, password, proxy=None):
        headers = TokenServiceConstants.HEADERS
        data = {
            USERNAME: username,
            PASSWORD: password
        }
        try:
            session = create_rest_template(proxy)
            response = session.post(self._api_url, headers=headers, data=data)
            if response.status_code == 200:
                return self.__process_token_response(response, username)
            else:
                response.raise_for_status()
        except requests.exceptions.HTTPError as e:
            error_msg = f"Exception in getting token details: {e.response.text}"
            logger.error(error_msg)
            raise TokenRequestError(e.response.status_code, error_msg)
        except (requests.exceptions.ConnectionError, urllib3.exceptions.MaxRetryError) as e:
            error_msg = f"Connection error occurred: {str(e)}"
            logger.error(error_msg)
            raise ConnectionError(f"Failed to establish connection to host '{self._api_url}': {str(e)}")
        except Exception as e:
            error_msg = f"An unexpected error occurred: {str(e)}"
            logger.error(error_msg)
            status_code = getattr(e, RESPONSE, None)
            if status_code:
                status_code = status_code.status_code
            raise TokenRequestError(status_code, error_msg)
    def __request_refresh_token(self, refresh_token, proxy=None):
        headers = TokenServiceConstants.HEADERS
        data = {
            REFRESH_TOKEN: refresh_token
        }

        try:
            session = create_rest_template(proxy)
            response = session.post(self._api_refresh_url, headers=headers, data=data)
            response.raise_for_status()
            if response.status_code == 200:
                return self.__process_refresh_token_response(response, refresh_token)
            else:
                response.raise_for_status()
        except requests.exceptions.HTTPError as e:
            error_msg = f"Exception in getting token details: {e.response.text}"
            logger.error(error_msg)
            raise TokenRequestError(e.response.status_code, error_msg)
        except (requests.exceptions.ConnectionError, urllib3.exceptions.MaxRetryError) as e:
            error_msg = f"Connection error occurred: {str(e)}"
            logger.error(error_msg)
            raise ConnectionError(f"Failed to establish connection to host '{self._api_url}': {str(e)}")
        except urllib3.exceptions.NameResolutionError as e:
            error_msg = f"DNS resolution error occurred: {e}"
            logger.error(error_msg)
            raise DNSResolutionError(self._api_url, e)
        except Exception as e:
            error_msg = f"An unexpected error occurred: {str(e)}"
            logger.error(error_msg)
            status_code = getattr(e, RESPONSE, None)
            if status_code:
                status_code = status_code.status_code
            raise TokenRequestError(status_code, error_msg)

    def __process_token_response(self, response, username):
        response_data = response.json()
        token_response = TokenResponse.from_json(response_data)
        if token_response.access_token:
            self.__cache_token_response(username, response_data)
            logger.info("Successfully retrieved new token response: %s", username)
            return response_data

    def __process_refresh_token_response(self, response, refresh_token):
        response_data = response.json()
        token_response = TokenResponse.from_json(response_data)
        if token_response.access_token:
            self.__cache_refresh_token_response(refresh_token, response_data)
            logger.info("Successfully retrieved token response using refresh token")
            return response_data

    def __cache_token_response(self, username, response_data):
        expires_in_seconds = int(response_data.get("expires_in_seconds", 0))
        expires_at = time.time() + expires_in_seconds
        cache_key = self.__generate_cache_key(username, self._password)
        self._token_map[cache_key] = {RESPONSE: response_data, EXPIRES_AT: expires_at}
        logger.info("Stored token response in cache map for user: %s", username)

    def __cache_refresh_token_response(self, refresh_token, response_data):
        expires_in_seconds = int(response_data.get("expires_in_seconds", 0))
        expires_at = time.time() + expires_in_seconds
        self._token_map[refresh_token] = {RESPONSE: response_data, EXPIRES_AT: expires_at}
        logger.info("Stored refresh token response in cache map")

    def __generate_cache_key(self, username, password):
        encrypted_password = self.__encrypt_password(password)
        return f"{username}:{encrypted_password}"

    def __encrypt_password(self, password):
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        return hashed_password
