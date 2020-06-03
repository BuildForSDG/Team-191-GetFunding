from flask import Flask, Blueprint, request, Response
from flask_login import logout_user, login_required
from flask_jwt_extended import jwt_required
logout_bp = Blueprint("logout_bp", __name__, url_prefix="/logout")

@logout_bp.route("/")
@jwt_required
@login_required
def logout_user():
    user_data = request.get_json()
    email = user_data.get("email")
    logout_user()
    return Response("Logged out successfully", 200)
