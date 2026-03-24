from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/calculate", methods=["GET"])
def calculate():
    
    operation = ["add", "substract", "multiply", "divide"]
    operation_arg = request.args.get("operation", "+")

    if operation_arg not in operation:
        return jsonify({
            "success": False,
            "field": "operation invalide"
        }), 400

    a = int(request.args.get("a", 0))
    b = int(request.args.get("b", 0))
    result = 0

    match(operation_arg):
        case "add":
            result = a + b
        case "substract":
            result = a - b
        case "multiply":
            result = a * b
        case "divide":
            result = a / b
        case _:
            result = ""

    return jsonify({
            "success": True,
            "result": result
        }), 200


if __name__ == "__main__":
    app.run(debug=True, port=5000)