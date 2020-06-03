from flask import Blueprint, request, abort, Response, url_for, render_template
from werkzeug.security import generate_password_hash
from src.token import generate_confirmation_token, confirm_token
from src.email import send_email
from flask_login import login_required, login_user
import src
register_bp = Blueprint("reg_bp", __name__, url_prefix="/register", template_folder="templates")


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
        passw = user_data["password"]
        phone_number = user_data["phone_number"]
        user = src.models.User(name=name, email=email,
                               password=generate_password_hash(password=passw),
                               phone_number=phone_number, lender=lender)
        src.db.session.add(user)
        src.db.session.commit()
        token = generate_confirmation_token(user.email)
        confirm_url = url_for("reg_bp.confirm_user", token=token, _external=True)
        html = str(render_template("activatemail.html", confirm_url = confirm_url))
        print(html)
        subject = "Confirmation of your email"
        send_email(user.email, subject, html)
        login_user(user)
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
        passw = user_data["password"]
        phone_number = user_data["phone_number"]
        user = src.models.User(name=name, email=email,
                               password=generate_password_hash(password=passw),
                               phone_number=phone_number, borrower=borrower)
        src.db.session.add(user)
        src.db.session.commit()
        token = generate_confirmation_token(user.email)
        confirm_url = url_for("src.confirm_user", token=token, _external=True)
        html = render_template("activatemail.html", confirm_url = confirm_url)
        subject = "Confirmation of your email"
        send_email(user.email, subject, html)
        login_user(user)
    except KeyError as key:
        return Response("Check your request", 400)
    return Response("Borrower has been added!", 200)

@register_bp.route("/confirm/<token>/")
def confirm_user(token):
    try:
        email = confirm_token(token)
    except:
        return Response("Link is invalid", 404)
    user = src.models.User.query.filter_by(email = email).first_or_404()
    if user.confirmed:
        return Response("<b>Already confirmed</b>",200)
    else:
        user.confirmed = True
        src.db.session.add(user)
        src.db.session.commit()
    return Response("<b>You are confirmed!<b>", 200)


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
        phone_result = (src.models.User.query.filter_by(phone_number=phone).first())
    except KeyError as key:
        abort(Response("Check your request", 400))
    except Exception as err:
        abort(Response(err, 500))
    if email_result is not None or phone_result is not None:
        abort(Response("User in db", 409))
