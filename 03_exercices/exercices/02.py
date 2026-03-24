from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/convert/temp", methods=['GET'])
def convert_temp():
    try:
        value = int(request.args.get('value', 20))
        unit = str(request.args.get('unit', 'c2f'))
    except ValueError:
        return jsonify({
            "success": False,
            "error": "value must be integers, unit must be str"
        }), 400

    if unit == 'c2f':
        convertion = (value * 9/5) + 32
        return jsonify({
        "success": True,
        "celsius": convertion,
        "fahrenheit": value,
    }), 200

    else: 
        convertion = (value - 32) * 5/9
        return jsonify({
            "success": True,
            "fahrenheit": convertion,
            "celsius": value,
        }), 200


if __name__ == "__main__":
    app.run(debug=True, port=5000)