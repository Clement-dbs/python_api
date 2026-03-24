from flask import Flask, jsonify, request
from datetime import datetime
import re

EMAIL_PATTERN = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
USERNAME_PATTERN = r'^[a-zA-Z0-9_]{3,20}$'

app = Flask(__name__)

users_db = {}
next_user_id = 1

@app.route("/register", methods=["POST"])
def register():

    global next_user_id
    
   
  
    data = request.get_json()
    
   # Vérifier format username (2-20 caractères)
    if (len(data["username"]) < 2 or len(data["username"]) > 20):
        return jsonify({
            "success": False,
            "field": "username"
        }), 400

   # Vérifier format email (format valide)
    if not re.match(EMAIL_PATTERN, data["email"]):
        return jsonify({
            "success": False,
            "field": "email",
        }), 400

   # Vérifier mot de passe correct minimum 8 caractères
    if len(data["password"]) < 8:
        return jsonify({
            "success": False,
            "field": "password",
        }), 400
    
   # Vérifier age (18-100)
    if data["age"] < 18 or data["age"] > 100:
        return jsonify({
            "success": False,
            "field": "age"
        }), 400

    new_user = {
        "id": next_user_id,
        "username": data['username'],
        "email": data['email'],
        "password": f"hashed_{data['password']}", 
        "age": int(data['age']),
        "created_at": datetime.now().strftime("%Y-%m-%d")
    }

    users_db[next_user_id] = new_user
    next_user_id += 1

    return jsonify({
        "success": True,
        "message": "User registered successfully",
        "data": {
            "id": new_user['id'],
            "username": new_user['username'],
            "email": new_user['email'],
            "created_at": new_user['created_at']
        }
    }), 201

if __name__ == '__main__':
    app.run(debug=True, port=5000)