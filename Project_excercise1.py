from flask import Flask, request, jsonify, redirect, url_for
from flask_mysqldb import MySQL
from flask_cors import CORS
'''These imports are essential for building a web application with Flask and integrating MySQL database 
and Cross-Origin Resource Sharing (CORS) functionality.'''

app = Flask(__name__) #An instance of the Flask application is created
cors = CORS(app) #CORS is enabled here

# MySQL configuration
app.config['MYSQL_USER'] = 'sql5693004'
app.config['MYSQL_PASSWORD'] = 'ruStJABw4n'
app.config['MYSQL_HOST'] = 'sql5.freemysqlhosting.net'
app.config['MYSQL_DB'] = 'sql5693004'


mysql = MySQL(app) # An instance of the MySQL extension is created and initialized with the Flask application using MySQL(app)


@app.route('/')
def index():
    cur = mysql.connection.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INT AUTO_INCREMENT PRIMARY KEY,
            username VARCHAR(50) UNIQUE NOT NULL,
            password VARCHAR(255) NOT NULL,
            email VARCHAR(100) UNIQUE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    mysql.connection.commit()
    cur.close()
    return "Welcome to the Home Page and users table is created"

@app.route('/register', methods=['POST'])
def register():
    username = request.form.get('username')
    password = request.form.get('password')

    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, password))
    mysql.connection.commit()
    cur.close()

    # Redirect to the home page after registration
    #return redirect(url_for('index'))


    return "User registered successfully", 201  # Return status code 201 Created

@app.route('/users', methods=['GET'])
def get_users():
    try: #Error codes are specified according to data sent and operations performed
        cur = mysql.connection.cursor()
        #Get query parameters
        '''This code checks if JSON data is provided using request.is_json. 
        If JSON data is provided, it extracts the query parameters from the JSON payload. 
        If not, it gets the query parameters from the URL as before. Then, it executes the SQL query accordingly. 
        If no users are found, it returns a 404 error.'''
        if request.is_json:  # Check if JSON data is provided
            data = request.json
            username_filter = data.get('username')
        else:  # If not JSON data, get query parameters from URL
            username_filter = request.args.get('username') # Get the value of 'username' query parameter
        # Build SQL query based on query parameters
        if username_filter:
            cur.execute("SELECT * FROM users WHERE username = %s", (username_filter,))
        else:
            cur.execute("SELECT * FROM users")

        users = cur.fetchall()
        cur.close()

        user_list = []
        for user in users:
            user_list.append({
                'id': user[0],
                'username': user[1],
                'password': user[2]
            })

        if not user_list: # Check if user_list is empty
            return "No such user exists", 404

        return jsonify(user_list), 200 # Return status code 200 OK
        # Redirect to the home page after fetching the list of users. Uncomment this to url_for execution 
        #return redirect(url_for('index')) 
    except Exception as e:
        print("An error occurred:", e)
        return "An error occurred while processing your request", 500 # Return status code 500 Internal Server Error


'''Open your browser.
Construct the URL for the /users endpoint with the desired query parameters. For example:
If you want to filter users by username, you can append ?username=desired_username to the endpoint URL.
Replace desired_username with the username you want to filter by.
The final URL might look like this: http://127.0.0.1:5000/users?username=desired_username.'''

# Create a route to retrieve user information based on username
@app.route('/users/<username>', methods=['GET'])
def get_user_by_username(username):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM users WHERE username = %s", (username,))
    user = cur.fetchone()
    cur.close()

    if user:
        user_info = {
            'id': user[0],
            'username': user[1],
            'password': user[2]
            # Add more fields as needed
        }
        return jsonify(user_info), 200  # Return user information with status code 200 OK
    else:
        return "User not found", 404  # Return 404 Not Found if user not found

# Create a route to retrieve user information based on user ID
@app.route('/users/id/<int:user_id>', methods=['GET'])
def get_user_by_id(user_id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM users WHERE id = %s", (user_id,))
    user = cur.fetchone()
    cur.close()

    if user:
        user_info = {
            'id': user[0],
            'username': user[1],
            'password': user[2]
            # Add more fields as needed
        }
        return jsonify(user_info), 200  # Return user information with status code 200 OK
    else:
        return "User not found", 404  # Return 404 Not Found if user not found\
    

@app.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    try:
        username = request.json.get('username')
        password = request.json.get('password')

        cur = mysql.connection.cursor()
        cur.execute("UPDATE users SET username = %s, password = %s WHERE id = %s", (username, password, user_id))
        mysql.connection.commit()
        cur.close()

        return "User updated successfully", 200  # Return status code 200 OK
    except Exception as e:
        return str(e), 400  # Return status code 400 Bad Request if there's an error


@app.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    try:
        cur = mysql.connection.cursor()
        cur.execute("DELETE FROM users WHERE id = %s", (user_id,))
        mysql.connection.commit()
        cur.close()

        return "User deleted successfully", 200  # Return status code 200 OK
    except Exception as e:
        return str(e), 500  # Return status code 500 Internal Server Error if there's an error

    

@app.route('/example', methods=['GET'])
def example_route():
    # Access custom headers
    custom_header_value = request.headers.get('X-Custom-Header')

    if custom_header_value:
        return f"Custom header value: {custom_header_value}"
    else:
        return "No custom header found"


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
    