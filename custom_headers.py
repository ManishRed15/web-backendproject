import requests

url = 'http://127.0.0.1:5000/example'  # Update the URL with your server's address

# Custom headers
headers = {
    'X-Custom-Header': 'MyCustomHeaderValue123',
}

# Send the GET request with custom headers
response = requests.get(url, headers=headers)

# Print the response
print(response.status_code)
print(response.text)


'''from flask import Flask, request, jsonify, redirect, url_for, Response

app = Flask(__name__)

# Your existing routes and configuration...

@app.route('/example', methods=['GET'])
def example_route():
    # Access custom headers
    custom_header_value = request.headers.get('X-Custom-Header')

    if custom_header_value:
        # Manipulate the header value if needed
        custom_header_value += " Modified"

        # Create a custom response with the manipulated header
        response = Response("Custom header value: {}".format(custom_header_value), status=200)
        response.headers['X-Custom-Header'] = custom_header_value

        return response
    else:
        return "No custom header found", 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
'''