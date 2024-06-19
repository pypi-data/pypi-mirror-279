# Authentication Module

The Authentication Module is a Python library that handles user authentication and token management. It supports obtaining and refreshing access tokens, and handling various exceptions that might occur during the authentication process.

## Features

- Obtain access tokens using username and password
- Methods exposed get_token() and get_refresh_token()
- Refresh access tokens using a refresh token.
- Handle errors such as invalid credentials, token request errors, and DNS resolution errors.
- Supports Proxy Functionality

## Installation

You can install the package using pip. Ensure you have Python 3.12+ installed.

```sh
! pip install authtestpkg1.0.0==1.0.2
```
# Usage
## 1.get_token Usage
Here's a brief example of how to use this get_token from this package:
```sh
from Authentication.services.impl.sdk_authenticate_service_impl import User

# Create a User instance
user = User()

# Get an access token using username and password
username = "your_username"
password = "your_password"
token_response = user.get_token(username, password)

print(token_response) # whole JSON response

#For getting access token from token_response
print(token_response.get("access_token"))
```
## 2.get_refresh_token Usage
```sh
from Authentication.services.impl.sdk_authenticate_service_impl import User

user = User()
refresh_token = "your_refresh_token"
new_token_response = user.get_refresh_token(refresh_token)

#For getting access token from new_token_response
print(new_token_response.get("access_token"))

print(new_token_response)
```

## Using a Proxy
If you need to use a proxy server for your authentication requests, you can pass an SDKProxy instance to the get_token or get_refresh_token methods.
```sh
from Authentication.services.impl.sdk_authenticate_service_impl import User
from Authentication.model.sdk_proxy import SDKProxy as AuthSDKProxy

# Create a User instance
user = User()

# Initialize proxy settings (if needed) 
auth_sdk_proxy = AuthSDKProxy( proxy_username="", proxy_password="", proxy_host=None, proxy_port=None, proxy_domain="" )

# Get an access token using username, password, and proxy
username = "your_username"
password = "your_password"
token_response = user.get_token(username, password, auth_sdk_proxy)
print(token_response)

#For getting access token from token_response
print(token_response.get("access_token"))

refresh_token_response=user.get_refresh_token("your_refresh_token",auth_sdk_proxy)
print(refresh_token_response)

#For getting access token from refresh_token_response
print(token_response.get("access_token"))

```

# Configuration
By default, the config is set to Prod URL's. To give preference, supports the custom-properties file. For that, Should create a properties file with Naming of "config/custom-authenticate-config.properties".
```sh
config/sdk_application.properties
```