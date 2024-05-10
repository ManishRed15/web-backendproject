//Function to handle user registration
function registerUser() {
    var regUsername = document.getElementById('regUsername').value;
    var regPassword = document.getElementById('regPassword').value;

    fetch('http://127.0.0.1:5000/register?username=' + regUsername + '&password=' + regPassword, {
        method: 'GET'
    })
    .then(response => {
        if (response.ok) {
            document.getElementById('regMessage').innerText = 'User registered successfully';
        } else {
            throw new Error('Failed to register user');
        }
    })
    .catch(error => {
        console.error('Error:', error.message);
        document.getElementById('regMessage').innerText = 'Error: ' + error.message;
    });
}

// Function to handle user login
function loginUser() {
    var loginUsername = document.getElementById('loginUsername').value;
    var loginPassword = document.getElementById('loginPassword').value;

    fetch('http://127.0.0.1:5000/login', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            username: loginUsername,
            password: loginPassword
        })
    })
    .then(response => {
        if (response.ok) {
            return response.json();
        } else {
            throw new Error('Invalid username or password');
        }
    })
    .then(data => {
        console.log(data);
        // Clear input fields
        document.getElementById('loginUsername').value = '';
        document.getElementById('loginPassword').value = '';
        // Display welcome message and access token
        document.getElementById('loginMessage').innerText = 'Welcome ' + loginUsername; 
        document.getElementById('accessToken').innerText = 'Access token: ' + data.access_token;
    })
    .catch(error => {
        console.error('Error:', error.message);
        document.getElementById('loginMessage').innerText = 'Error: ' + error.message;
    });
}

// Function to handle file upload
function uploadFile() {
    var fileInput = document.getElementById('fileInput');
    var file = fileInput.files[0];
    var formData = new FormData();
    formData.append('file', file);

    fetch('http://127.0.0.1:5000/upload', {
        method: 'POST',
        body: formData
    })
    .then(response => {
        if (response.ok) {
            return response.json();
        } else {
            throw new Error('Failed to upload file');
        }
    })
    .then(data => {
        console.log(data);
        document.getElementById('uploadMessage').innerText = data.message;
    })
    .catch(error => {
        console.error('Error:', error.message);
        document.getElementById('uploadMessage').innerText = 'Error: ' + error.message;
    });
}

// Function to retrieve and display user data
function getUserData() {
    fetch('http://127.0.0.1:5000/users', {
        method: 'GET'
    })
    .then(response => {
        if (response.ok) {
            return response.json();
        } else {
            throw new Error('Failed to retrieve user data');
        }
    })
    .then(users => {
        console.log(users);
        var userList = document.getElementById('userList');
        userList.innerHTML = ''; // Clear existing user data

        users.forEach(user => {
            var userElement = document.createElement('div');
            userElement.textContent = 'Username: ' + user.username;
            userList.appendChild(userElement);
        });
    })
    .catch(error => {
        console.error('Error:', error.message);
        document.getElementById('message').innerText = 'Error: ' + error.message;
    });
}