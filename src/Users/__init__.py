"""User module, handles user routes e.g. Registration, Login and Logout."""
from .register import register_bp
from .login import login_bp


def print_modules():
    print(register_bp)
