import pytest
from src import create_app, db
from src.models import User

# create a test client for testing methods, requests and responses
@pytest.fixture(scope="module")
def test_client():
    app = create_app()
    client = app.test_client()
    return client

# Create new user on the User db
@pytest.fixture(scope="module")
def new_user():
    user = User(name="Flask", email="poocoo@flask.org",)
    return user
