from crypt import methods
from flask import Flask, jsonify
app = Flask(__name__)

data = [
        {
            "id":1,
            "image":"urllink",
            "LicenseNum":"result",
        },
        {
            "id":2,
            "image":"urllink",
            "LicenseNum":"result",
        }
]

@app.route('/')
def home():
    return "Hello My First Flask Project"

@app.route('/apitest', methods=['GET'])
def get_api():
    return jsonify(data)


if __name__ == '__main__':
    app.run(debug=True)