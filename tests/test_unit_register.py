import unittest
from . import User, Lender, Borrower, create_app, db


class RegisterBPTest(unittest.TestCase):

    def setUp(self):
        self.app = create_app()
        self.test_client = app.test_client()
        self.ctx = self.app.app_context()
        self.ctx.push()
        db.create_all()
        lender1 = Lender()
        user1 = User(name="Wycliffe", email="sikoli@gmail.com",
                 phone_number="0703680126", password="SaveTheWorld",
                 lender=lender1)
        borrower1 = Borrower()
        user2 = User(name="Kefa", email="mutu@yahoo.com",
                 phone_number="+254708456210",
                 password="AmKing", borrower=borrower1)
        db.session.add(user1)
        db.session.add(user2)
        db.session.commit()

        def test_no_body_sent(self):
            response = test_client.post('/register/lender/', json=None)
            self.assertEqual(response.status_code,400)

        def test_add_lender(test_client, mock_db):
            response = test_client.post('/register/lender/',json={"name": "Eric","email": "macha@gmail.com","phone_number": "0704900126","password": "qwerty"})
            assert response.status_code == 200
            assert b"Lender has been added" in response.data
        
        def test_duplicate_lender_sent(self):
            response = test_client.post('/register/lender/',
                                json={"name": "Wycliffe",
                                      "email": "sikoi@gmail.com",
                                      "phone_number": "0703680126",
                                      "password": "SaveTheWorld"})
            assert response.status_code == 409
            assert b"User in db" in response.data
        
        def test_duplicate_borrower_sent(self):
            response = test_client.post('/register/borrower/',
                                json={"name": "Kefa",
                                      "email": "mutu@yahoo.com",
                                      "phone_number": "+254708456210",
                                      "password": "AmKing"})
            assert response.status_code == 409
            assert b"User in db" in response.data

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.ctx.pop()