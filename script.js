document.getElementById('loginForm').addEventListener('submit', function(event) {
    event.preventDefault();

    var username = document.getElementById('username').value;
    var password = document.getElementById('password').value;

    fetch('http://localhost:5000/login', {
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
        document.getElementById('message').innerText = 'Login successful. Access token: ' + data.access_token;
    })
    .catch(error => {
        console.error('Error:', error.message);
        document.getElementById('message').innerText = 'Error: ' + error.message;
    });
});
