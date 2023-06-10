import requests
import login_reqs

access_token = login_reqs.jwt_token['token']

# create_one_user
# user = {'name': 'Hassan', 'role': 'user', 'email': 'new_email3@a.b', 'password': 'new_password', 'phone_number': '123456789', 'city': 'Urmia'}
# print(requests.post('http://127.0.0.1:8000/users', json=user).json())

# get_one_user
print(requests.get('http://127.0.0.1:8000/users/1',  headers={'Authorization': f"Bearer {access_token}"}).json())
