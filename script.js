document.getElementById('loginForm').addEventListener('submit', function(event) {
    event.preventDefault();

    var username = document.getElementById('username').value;
    var password = document.getElementById('password').value;

    fetch('http://127.0.0.1:5000/login', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            username: username,
            password: password
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
        document.getElementById('loginForm').style.display = 'none'; // Hide the login form
        document.getElementById('message').innerText = 'Welcome ' + username; // Display welcome message
        document.getElementById('accessToken').innerText = 'Access token: ' + data.access_token; // Display access token
    })
    .catch(error => {
        console.error('Error:', error.message);
        document.getElementById('message').innerText = 'Error: ' + error.message;
    });
});
