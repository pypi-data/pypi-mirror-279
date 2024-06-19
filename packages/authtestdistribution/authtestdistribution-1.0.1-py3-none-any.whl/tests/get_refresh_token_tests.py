from Authentication.services.impl.sdk_authenticate_service_impl import User

client_instance = User()
username = "--username--"
password = "--password--"
refresh_token_response=client_instance.get_refresh_token('--refresh_token--')
print(refresh_token_response)

print("access token from refresh token",refresh_token_response.get('access_token'))