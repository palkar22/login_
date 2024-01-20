#C:\flask_dev\flaskreact\app.py
from flask import Flask, request, jsonify, session
from flask_bcrypt import Bcrypt #pip install Flask-Bcrypt = https://pypi.org/project/Flask-Bcrypt/
from flask_cors import CORS, cross_origin #ModuleNotFoundError: No module named 'flask_cors' = pip install Flask-Cors
from models import db, User
from flask_cors import CORS


app = Flask(__name__)
CORS(app, supports_credentials=True) 
app.config['SECRET_KEY'] = 'cairocoders-ednalan'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///jokers.db'
 
SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_ECHO = True
  
bcrypt = Bcrypt(app) 
CORS(app, supports_credentials=True)
db.init_app(app)
  
with app.app_context():
    db.create_all()
 
@app.route("/")
def hello_world():
    return "Hello, World!"
 
@app.route("/Register", methods=["POST"])
def register():
    username = request.json["username"]
    password = request.json["password"]
 
    user_exists = User.query.filter_by(username=username).first() is not None
 
    if user_exists:
        return jsonify({"error": "username already exists"}), 409
     
    hashed_password = bcrypt.generate_password_hash(password)
    new_user = User(username=username, password=password)
    db.session.add(new_user)
    db.session.commit()
 
    session["user_id"] = new_user.id
 
    return jsonify({
        "id": new_user.id,
        "username": new_user.username
    })
 
@app.route("/Login", methods=["POST"])
def login():
    username = request.json["username"]
    password = request.json["password"]
  
    user = User.query.filter_by(username=username).first()
  
    if user is None:
        return jsonify({"error": "Unauthorized Access"}), 401
  
    if not bcrypt.check_password_hash(user.password, password):
        return jsonify({"error": "Unauthorized"}), 401
      
    session["user_id"] = user.id
  
    return jsonify({
        "id": user.id,
        "username": user.username
    })
@app.route("/get_users", methods=["GET"])
def get_users():
    users = User.query.all()
    user_data = [{"id": user.id, "username": user.username} for user in users]
    return jsonify({"users": user_data})
@app.route("/modify_user/<user_id>", methods=["PUT"])
def modify_user(user_id):
    try:
        new_password = request.json.get("new_password")

        if not new_password:
            return jsonify({"error": "New password is required"}), 400

        user = User.query.filter_by(id=user_id).first()

        if user is None:
            return jsonify({"User password modified successfully"})

        # Modify the user's password
        hashed_password = bcrypt.generate_password_hash(new_password)
        user.password = hashed_password

        db.session.commit()

        return jsonify({"message": "User password modified successfully"})

    except Exception as e:
        return jsonify({"error": str(e)}), 500
if __name__ == "__main__":
    app.run(debug=True)