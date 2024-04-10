import requests

url = 'http://127.0.0.1:5000/register'  # Update the URL with your server's address

# Data to be sent in the POST request
user_list = [
   # {'username': 'Rahul', 'password': 'password1'},
   # {'username': 'John', 'password': 'password2'},
   # {'username': 'Alice', 'password': 'password3'},
   # {'username': 'Raol', 'password': 'password35'} , 
   {'username': 'Randy', 'password': 'password40'}, 
    
]

# Send the POST request for each username-password pair
for user_data in user_list:
    response = requests.post(url, data=user_data)
    print(f"Status code for {user_data['username']}: {response.status_code}")
    print(response.text)
    
# Print the response
print(response.status_code)


