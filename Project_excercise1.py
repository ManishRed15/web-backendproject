from flask import Flask, request, jsonify, redirect, url_for, make_response
from flask_mysqldb import MySQL
from flask_cors import CORS
from flask_pymongo import PyMongo 
from bson import ObjectId
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity 
import os
from werkzeug.security import generate_password_hash, check_password_hash


app = Flask(__name__) #An instance of the Flask application is created
cors = CORS(app) #CORS is enabled here

app.config['MONGO_URI'] = 'mongodb://localhost:27017/Myfirstdatabase'
mongo = PyMongo(app)

secret_key = os.urandom(32)

app.config['JWT_SECRET_KEY'] = secret_key  # Change this to a secret key of your choice
jwt = JWTManager(app)

# Define the path to the upload folder
app.config['UPLOAD_FOLDER'] = r'C:\Users\manish.reddy\Desktop\upload_folder'

# Define a route to handle file uploads
@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    # Save the file to the upload folder
    file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))

    return jsonify({'message': 'File uploaded successfully'}), 200


@app.route('/')
def index():
    return "Welcome to the Home Page and users table is created"

@app.route('/register', methods=['GET'])
def register():
    username = request.args.get('username')
    password = request.args.get('password')

    users_collection = mongo.db.users
    user_data = {
        'username': username,
        'password': password
    }
    users_collection.insert_one(user_data)

    return "User registered successfully", 201

@app.route('/users', methods=['GET'])
def get_users():
    users_collection = mongo.db.users
    users = list(users_collection.find({}, {'_id': 0}))  # Exclude '_id' field from the response
    return jsonify(users), 200

# Create a route to retrieve user information based on username
@app.route('/users/<username>', methods=['GET'])
def get_user_by_username(username):
    users_collection = mongo.db.users
    user = users_collection.find_one({'username': username}, {'_id': 0})
    if user:
        return jsonify(user), 200
    else:
        return "User not found", 404

@app.route('/users/id/<user_id>', methods=['GET'])
def get_user_by_id(user_id):
    try:
        # Convert user_id string to ObjectId
        user_id_obj = ObjectId(user_id)

        # Query the MongoDB collection
        users_collection = mongo.db.users
        user = users_collection.find_one({'_id': user_id_obj}, {'_id': 0})

        if user:
            return jsonify(user), 200
        else:
            return "User not found", 404
    except Exception as e:
        return str(e), 400  # Return status code 400 Bad Request if there's an error
    

@app.route('/login', methods=['POST'])
def login():
    username = request.json.get('username')
    password = request.json.get('password')

    print("Received username:", username)
    print("Received password:", password)

    # Verify user credentials
    if username == 'mark' and password == 'password567':
        access_token = create_access_token(identity=username)
        return jsonify(access_token=access_token), 200
    else:
        return jsonify({"msg": "Invalid username or password"}), 401
    
@app.route('/protected', methods=['GET'])
@jwt_required()
def protected():
    current_user = get_jwt_identity()
    return jsonify(logged_in_as=current_user), 200

@app.route('/set-cookie', methods=['GET'])
def set_cookie():
    resp = make_response("Cookie set successfully")
    resp.set_cookie('username', 'example_username')
    return resp

@app.route('/get-cookie', methods=['GET'])
def get_cookie():
    username = request.cookies.get('username')
    return f"Username from cookie: {username}"

# Update user route
@app.route('/users/<username>', methods=['PUT'])
def update_user(username):
    users_collection = mongo.db.users
    user_data = request.json  # Data to update
    result = users_collection.update_one({'username': username}, {'$set': user_data})
    if result.modified_count:
        return jsonify({'message': 'User updated successfully'}), 200
    else:
        return jsonify({'error': 'User not found'}), 404

# Delete user route
@app.route('/users/<username>', methods=['DELETE'])
def delete_user(username):
    users_collection = mongo.db.users
    result = users_collection.delete_one({'username': username})
    if result.deleted_count:
        return jsonify({'message': 'User deleted successfully'}), 200
    else:
        return jsonify({'error': 'User not found'}), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)