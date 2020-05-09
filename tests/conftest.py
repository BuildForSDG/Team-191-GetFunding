import pytest
from . import User, Lender, Borrower, create_app, db

# create a test client for testing methods, requests and responses
@pytest.fixture(scope="module")
def test_client():
    app = create_app()
    client = app.test_client()
    ctx = app.app_context()
    ctx.push()
    yield client
    ctx.pop()


# Create new user on the User db
@pytest.fixture(scope="module")
def new_user():
    user = User(name="Flask", email="poocoo@flask.org",)
    return user


@pytest.fixture(scope="module")
def mock_db():
    db.create_all()
    lender1 = Lender()
    user1 = User(name="Wycliffe", email="sikoli@gmail.com", phone_number="0703680126", password="SaveTheWorld", lender=lender1)
    borrower1 = Borrower()
    user2 = User(name="Kefa", email="mutu@yahoo.com", phone_number="+254708456210", password="AmKing", borrower=borrower1)
    db.session.add(user1)
    db.session.add(user2)
    db.session.commit()
    yield db
    db.drop_all()