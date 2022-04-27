from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os
import bcrypt

# Init app
app = Flask(__name__, template_folder="./public")
basedir = os.path.abspath(os.path.dirname(__file__))

# Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'db.sqlite') 
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Init db
db = SQLAlchemy(app)

# Init orm
ma = Marshmallow(app)

# User Model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    password = db.Column(db.String)

    def __init__(self, name, password):
        self.name = name
        self.password = password

# User Schema
class UserSchema(ma.Schema):
    class Meta:
        fields = ('id', 'firstname', 'name', 'email', 'password')

# Item Model
class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)

    def __init__(self, name):
        self.name = name

# Item Schema
class ItemSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name')

# Init User and Item schema
user_schema = UserSchema()
users_schema = UserSchema(many=True)
item_schema = ItemSchema()
items_schema = ItemSchema(many=True)

# Create a User
@app.route('/users', methods=['POST'])
def add_user():
        name = request.json['name']
        password = request.json['password'].encode("utf-8")

        hashed = bcrypt.hashpw(password, bcrypt.gensalt())

        new_user = User(name, hashed)

        db.session.add(new_user)
        db.session.commit()

        return jsonify('New User Created')

# Get all users
@app.route('/users', methods=['GET'])
def get_users():
    all_users = User.query.all()
    result = users_schema.dump(all_users)
    return jsonify(result)

# Get single User by id
@app.route('/users/<id>', methods=['GET'])
def get_user(id):
    user = User.query.get(id)
    result = user_schema.dumps(user)
    return jsonify(result)

# Delete user
@app.route('/users/<id>', methods=['DELETE'])
def delete_user(id):
    user = User.query.get(id)
    db.session.delete(user)
    db.session.commit()
    return jsonify('User Deleted')

# Get all items
@app.route('/items', methods=['GET'])
def get_items():
    all_items = Item.query.all()
    result = items_schema.dump(all_items)
    return jsonify(result)

# Run Server
if __name__ == '__main__':
    app.run(debug=True)