from flask import Blueprint, request, abort, Response
from werkzeug.security import generate_password_hash
from src.models import db
from src.models import User, Borrower, Lender
register_bp = Blueprint("reg_bp", __name__, url_prefix="/register")


@register_bp.route("/lender/", methods=["POST"])
def reg_lender():
    """Lender registration endpoint.

    Handles lender registration and adds to db if successful
    METHODS: POST
    """
    user_data = request.get_json()
    check_user_data(user_data)
    try:
        lender = Lender()
        name = user_data["name"]
        email = user_data["email"]
        password = user_data["password"]
        phone_number = user_data["phone_number"]
        user = User(name=name, email=email, password=generate_password_hash(password=password), phone_number=phone_number, lender=lender)
        db.session.add(user)
        db.session.commit()
    except KeyError as key:
        return Response("Check "+str(key), 400)
    else:
        return Response("Lender has been added!", 200)


@register_bp.route("/borrower/", methods=["POST"])
def reg_borrower():
    """Borrower registration endpoint.

    Handles the borrower registration and adds to db if sucessful
    METHODS: POST
    """
    user_data = request.get_json()
    check_user_data(user_data)
    try:
        borrower = Borrower()
        name = user_data["name"]
        email = user_data["email"]
        password = user_data["password"]
        phone_number = user_data["phone_number"]
        user = User(name=name, email=email, password=generate_password_hash(password=password), phone_number=phone_number, borrower=borrower)
        db.session.add(user)
        db.session.commit()
    except KeyError as key:
        return Response("Check "+str(key), 400)
    return Response("Borrower has been added!", 200)


def check_user_data(user_info):
    """Check if user in the database.
    
    It generates errors if use in the db
    Args:
        user_info: user data in key:value pairs format
    Returns:
        Throws and aborts if user is present or None if not not present
    """
    email_result = None
    phone_result = None
    if user_info is None:
        abort(Response("Body cannnot be empty"), 400)
    try:
        email = user_info["email"]
        email_result = User.query.filter_by(email=email).first()
        phone = user_info["phone_number"]
        phone_result = User.query.filter_by(phone_number=phone).first()
    except KeyError as key:
        abort(Response(str(key)+"is missing", 400))
    except Exception as err:
        abort(Response("Check your request "+str(err), 400))
    if email_result is not None or phone_result is not None:
        abort(Response("User in db", 409))
