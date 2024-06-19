from Authentication.services.impl.sdk_authenticate_service_impl import User

client_instance = User()
username = "--username--"
password = "--password--"
token_response = client_instance.get_token("username", "password")
print(token_response)

print("access token",token_response.get('access_token'))