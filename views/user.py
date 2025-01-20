
from flask import jsonify, request, Blueprint
from models import db, User
from werkzeug.security import generate_password_hash

user_bp = Blueprint("user_bp", __name__)


# User
@user_bp.route("/users")
def fetch_users():
    users = User.query.all()

    user_list = []
    for user in users:
        user_list.append({
            'id':user.id,
            'email':user.email,
            'is_approved': user.is_approved,
            'is_admin': user.is_admin,
            'username':user.username,
        })

    # user_list = [{
    #         'id':user.id,
    #         'email':user.email,
    #         'is_approved': user.is_approved,
    #         'username':user.username
    #     } for user in Users]

    return jsonify(user_list)

@user_bp.route("/users", methods=["POST"])
def add_users():
    data = request.get_json()
    username = data['username']
    email = data['email']
    password = generate_password_hash(data['password'])

    check_username = User.query.filter_by(username=username).first()
    check_email = User.query.filter_by(email=email).first()

    print("Email ",check_email)
    print("Username",check_username)
    if check_username or check_email:
        return jsonify({"error":"Username/email exists"}),406

    else:
        new_user = User(username=username, email=email, password=password)
        db.session.add(new_user)
        db.session.commit()
        return jsonify({"success":"Added successfully"}), 201
    
# Update
@user_bp.route("/users/<int:user_id>", methods=["PATCH"])
def update_users(user_id):
    user = User.query.get(user_id)

    if user:
        data = request.get_json()
        username = data.get('username', user.username)
        email = data.get('email', user.email)
        password = data.get('password', user.password)

        check_username = User.query.filter_by(username=username and id!=user.id).first()
        check_email = User.query.filter_by(email=email and id!=user.id).first()

    
        if check_username or check_email:
            return jsonify({"error":"Username/email exists"}),406

        else:
            user.username=username
            user.email=email
            user.password=password
          
            db.session.commit()
            return jsonify({"success":"Updated successfully"}), 201

    else:
        return jsonify({"error":"User doesn't exist!"}),406
    

# Delete
@user_bp.route("/users/<int:user_id>", methods=["DELETE"])
def delete_users(user_id):
    user = User.query.get(user_id)

    if user:
        db.session.delete(user)
        db.session.commit()
        return jsonify({"success":"Deleted successfully"}), 200

    else:
        return jsonify({"error":"User your are trying to delete doesn't exist!"}),406