from flask import Blueprint, request, abort, Response, jsonify
from werkzeug.security import check_password_hash
from flask_login import login_user
from flask_jwt_extended import (
    jwt_required, create_access_token, get_jwt_identity
)
import src

login_bp = Blueprint("login_bp", __name__, url_prefix="/login")

@login_bp.route("/", methods=["POST"])
def login_user():
    user_data = request.get_json()
    if user_data is None:
        return abort(Response("incorrect data",400))
    
    email = user_data.get("email")
    user_present = src.models.User.query.filter_by(email = email).first()
    if user_present is None:
        return abort(Response("User not found", 403))
    if not user_present.confirmed:
        return abort(Response("User is not confirmed", 403)) 
    password = user_data.get("password")
    if check_password_hash(user_present.password, password) and user_present.confirmed:
        login_user(user_present)
        access_token = create_access_token(identity=email)
        return jsonify(token = access_token), 200
    else:
        return Response("Invalid authentication", 403)

