from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/hello/english", methods=['GET'])
def hello_en():
    return "Hello!"

@app.route("/hello/french")
def hello_fr():
    return "Bonjour!"


if __name__ == "__main__":
    app.run(debug=True, port=5000)