from flask import Blueprint, request, jsonify, render_template
from helpers import token_required
from models import db, User, Book, book_schema, books_schema

api = Blueprint('api', __name__, url_prefix='/api')

@api.route('/getdata')
def getdata():
    return {'get': 'money'}

# Create book
@api.route('/books', methods = ['POST'])
@token_required
def create_book(current_user_token):
    title = request.json['title']
    author = request.json['author']
    isbn = request.json['isbn']
    print_length = request.json['print_length']
    release_date = request.json['release_date']
    edition = request.json['edition']
    format = request.json['format']
    user_token = current_user_token.token

    print(f'BIG TESTER: {current_user_token.token}')

    book = Book(title, author, isbn, print_length, release_date, edition, format, user_token = user_token)

    db.session.add(book)
    db.session.commit()

    response = book_schema.dump(book)
    return jsonify(response)

# Get books
@api.route('/books', methods = ['GET'])
@token_required
def get_book(current_user_token):
    a_user = current_user_token.token
    books = Book.query.filter_by(user_token = a_user).all()
    response = books_schema.dump(books)
    return jsonify(response)

# Get single book
@api.route('/books/<id>', methods = ['GET'])
@token_required
def get_single_book(current_user_token, id):
    book = Book.query.get(id)
    response = book_schema.dump(book)
    return jsonify(response)


# Update book
@api.route('/books/<id>', methods = ['POST', 'PUT'])
@token_required
def update_book(current_user_token, id):
    book = Book.query.get(id)
    book.title = request.json['title']
    book.author = request.json['author']
    book.isbn = request.json['isbn']
    book.print_length = request.json['print_length']
    book.release_date = request.json['release_date']
    book.edition = request.json['edition']
    book.format = request.json['format']
    book.user_token = current_user_token.token

    db.session.commit()
    response = book_schema.dump(book)
    return jsonify(response)

# Deleting book
@api.route('/books/<id>', methods = ['DELETE'])
@token_required
def delete_book(current_user_token, id):
    book = Book.query.get(id)
    db.session.delete(book)
    db.session.commit()
    response = book_schema.dump(book)
    return jsonify(response)