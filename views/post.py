from flask import jsonify, request, Blueprint
from models import db, User,Post
from flask_jwt_extended import jwt_required, get_jwt_identity

post_bp= Blueprint("post_bp", __name__)

@post_bp.route("/post/add", methods=["POST"])
@jwt_required()
def add_post():
    data = request.get_json()
    current_user_id = get_jwt_identity()

    title = data['title']
    content = data['content']
    post_id = data['post_id']

    check_post_id =Post.query.get(post_id)

    if not check_post_id:
        return jsonify({"error":"Post/user doesn't exists"}),406

    else:
        new_post = Post(title=title, content=content,user_id=current_user_id, post_id=post_id, )
        db.session.add(new_post)
        db.session.commit()
        return jsonify({"success":"post added successfully"}), 201

@post_bp.route("/posts", methods=["GET"])
@jwt_required()
def get_posts():
    current_user_id = get_jwt_identity()

    posts = Post.query.filter_by(user_id = current_user_id)

    post_list = [
        {
            "id": post.id,
            "title": post.title,
            "post": post.post,
            "user_id": post.user_id,
            "is_complete": post.is_complete,
            "user": {"id":post.user.id, "username": post.user.username, "email": post.user.email},
        } for post in posts
    ]    

    return jsonify(post_list), 200


@post_bp_bp.route("/post_bp/<int:post_bp_id>", methods=["GET"])
@jwt_required()
def get_post_bp(post_bp_id):
    current_user_id = get_jwt_identity()

    post_bp = post_bp.query.filter_by(id=post_bp_id, user_id=current_user_id).first()
    if post_bp:
        post_bp_details = {
            "id": post_bp.id,
            "title": post_bp.title,
            "content": post_bp.content,
            "user_id": post_bp.user_id,
        }
        return jsonify(post_bp_details), 200
    
    else:
        return jsonify({"error": "post_bp not found"}), 406



# UPDATE
@post_bp.route("/post/<int:post_id>", methods=["PUT"])
@jwt_required()
def update_post(post_id):
    current_user_id = get_jwt_identity()

    data = request.get_json()
    post = Post.query.get(post_id)

    if post and post.user_id==current_user_id:

        title = data.get('title', post.title)
        content = data.get('content', post.content)
        is_complete=data.get('is_complete', post.is_complete)

        check_tag_id =User.query.get(post_id)

    
        if not check_tag_id :
            return jsonify({"error":"Tag/user doesn't exists"}),406


        else:
            # Apply updates
            post.title = title
            post.content = content
            post.is_complete = is_complete

            db.session.commit()
            return jsonify({"success": "post updated successfully"}), 200

    else:
        return jsonify({"error": "post not found/Unauthorized"}), 406
    
# DELETE
@post_bp_bp.route("/post_bp/<int:post_bp_id>", methods=["DELETE"])
@jwt_required()
def delete_post_bp(post_bp_id):
    current_user_id = get_jwt_identity()

    post_bp = post_bp.query.filter_by(id=post_bp_id, user_id=current_user_id).first()

    if not post_bp:
        return jsonify({"error": "Post_bp not found/Unauthorized"}), 406


    db.session.delete(post_bp)
    db.session.commit()
    return jsonify({"success": "Post_bp deleted successfully"}), 200
