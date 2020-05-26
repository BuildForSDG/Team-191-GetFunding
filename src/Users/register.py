from flask import Blueprint, request, abort, Response
from werkzeug.security import generate_password_hash
import src
register_bp = Blueprint("reg_bp", __name__, url_prefix="/register")


@register_bp.route("/lender/", methods=["POST"])
def reg_lender():
    """
    Lender registration endpoint.
    Handles lender registration and adds to db if successful
    METHODS: POST
    """
    user_data = request.get_json()
    check_user_data(user_data)
    try:
        lender = src.models.Lender()
        name = user_data["name"]
        email = user_data["email"]
        password = user_data["password"]
        phone_number = user_data["phone_number"]
        user = src.models.User(name=name, email=email,
                    password=generate_password_hash(password=password),
                    phone_number=phone_number, lender=lender)
        src.db.session.add(user)
        src.db.session.commit()
    except KeyError as key:
        return Response("Check your request", 400)
    else:
        return Response("Lender has been added!", 200)


@register_bp.route("/borrower/", methods=["POST"])
def reg_borrower():
    """
    Borrower registration endpoint.
    Handles the borrower registration and adds to db if sucessful
    METHODS: POST
    """
    user_data = request.get_json()
    check_user_data(user_data)
    try:
        borrower = src.models.Borrower()
        name = user_data["name"]
        email = user_data["email"]
        password = user_data["password"]
        phone_number = user_data["phone_number"]
        user = src.models.User(name=name, email=email,
                    password=generate_password_hash(password=password),
                    phone_number=phone_number, borrower=borrower)
        src.db.session.add(user)
        src.db.session.commit()
    except KeyError as key:
        return Response("Check your request", 400)
    return Response("Borrower has been added!", 200)


def check_user_data(user_info):
    """
    Check if user in the database.
    It generates errors if use in the db
    Args:
        user_info: user data in key:value pairs format
    Returns:
        Throws and aborts if user is present or None if not not present
    """
    if user_info is None:
        abort(Response("Body cannnot be empty", 400))
    try:
        email = user_info["email"]
        email_result = src.models.User.query.filter_by(email=email).first()
        phone = user_info["phone_number"]
        phone_result = src.models.User.query.filter_by(phone_number=phone).first()
    except KeyError as key:
        abort(Response("Check your request", 400))
    except Exception as err:
        abort(Response("Server Error ", 500))
    if email_result is not None or phone_result is not None:
        abort(Response("User in db", 409))
