from flask import Flask, request, jsonify

app = Flask(__name__)

books_db = {
    1: {"title": "1984", "author": "Orwell", "year": 1949},
    2: {"title": "1984", "author": "Orwell", "year": 1949},
    3: {"title": "1984", "author": "Orwell", "year": 1949}
}

next_book_id = 4

@app.route("/books", methods=['GET'])
def get_all_books():
    return jsonify({
        "success": True,
        "data": list(books_db.values()),
        "count": len(books_db)
    }), 200

@app.route("/books/<int:book_id>", methods=['GET'])
def get_book_by_id(book_id):
    if book_id not in books_db:
        return jsonify({
            "success": False,
            "error": f"User {book_id} not found"
        }), 404

    return jsonify({
        "success": True,
        "data": books_db[book_id]
    }), 200

@app.route("/books/", methods=['POST'])
def create_book():

    global next_book_id

    if not request.is_json:
        return jsonify({
            "success": False,
            "error": "Content-Type must be application/json"
        }), 400

    data = request.get_json()

    new_book = {
        "title": data['title'],
        "author": data['author'],
        "year": data['year']
    }
    books_db[next_book_id] = new_book
    next_book_id += 1

    return jsonify({
        "success": True,
        "message": "User created successfully",
        "data": new_book
    }), 201

if __name__ == "__main__":
    app.run(debug=True, port=5000)