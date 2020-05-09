from flask import Blueprint, request, abort, Response
from werkzeug.security import generate_password_hash
from . import db
from src.models import User, Borrower, Lender
register_bp = Blueprint("reg_bp", __name__, url_prefix="/register")


@register_bp.route("/lender/", methods=["POST"])
def reg_lender():
    """
    Lender registration endpoint
    """
    user_data = request.get_json()
    if user_data is None:
        abort(400)
    err = is_user_in_db_err(user_data)
    if err is LookupError:
        return Response("User in db", 409)
    elif err is KeyError:
        return Response(err)
    try:
        name = user_data["name"]
        email = user_data["email"]
        password = user_data["password"]
        phone_number = user_data["phone_number"]
        lender = Lender()
        user = User(name=name, email=email, password=generate_password_hash(password=password), phone_number=phone_number, lender=lender)
        db.session.add(user)
        db.session.commit()
    except KeyError as key:
        return Response("Check "+str(key),400)
    
    return Response("Lender has been added!", 200)


@register_bp.route("/borrower/", methods=["POST"])
def reg_borrower():
    """
    Borrower registration endpoint
    """
    user_data = request.get_json()
    if user_data is None:
        abort(400)
    if user_data is None:
        abort(400)
    err = is_user_in_db_err(user_data)
    if err is LookupError:
        return Response("User in db", 409)
    elif err is KeyError:
        return Response(err)
    try:
        name = user_data["name"]
        email = user_data["email"]
        password = user_data["password"]
        phone_number = user_data["phone_number"]
        borrower = Borrower()
        user = User(name=name, email=email, password=generate_password_hash(password=password), phone_number=phone_number, borrower=borrower)
        db.session.add(user)
        db.session.commit()
    except KeyError as key:
        return Response("Check "+str(key),400)
    return Response("Borrower has been added!", 200)


def is_user_in_db_err(user_info):
    """
    Check if user in the database
    """
    email_result = None
    phone_result = None
    err = None
    try:
        email = user_info["email"]
        email_result = User.query.filter_by(email=email).first()
        phone = user_info["phone_number"]
        phone_result = User.query.filter_by(phone_number=phone).first()
    except KeyError as key:
        return key
    if email_result is not None or phone_result is not None:
        return LookupError
    return None