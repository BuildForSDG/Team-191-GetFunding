import unittest
import src


class RegisterBPTest(unittest.TestCase):

    def setUp(self):
        self.app = src.create_app()
        self.test_client = self.app.test_client()
        self.ctx = self.app.app_context()
        self.ctx.push()
        src.db.create_all()
        lender1 = src.models.Lender()
        user1 = src.models.User(name="Wycliffe", email="sikoli@gmail.com",
                 phone_number="0703680126", password="SaveTheWorld",
                 lender=lender1)
        borrower1 = src.models.Borrower()
        user2 = src.models.User(name="Kefa", email="mutu@yahoo.com",
                 phone_number="+254708456210",
                 password="AmKing", borrower=borrower1)
        src.db.session.add(user1)
        src.db.session.add(user2)
        src.db.session.commit()

    def test_no_body_sent(self):
        response = self.test_client.post('/register/lender/', json=None)
        self.assertEqual(response.status_code, 400)

    def test_add_lender(self):
        response = self.test_client.post('/register/lender/', json={"name": "Eric", "email": "macha@gmail.com", "phone_number": "0704900126", "password": "qwerty"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, b"Lender has been added!")

    def test_duplicate_lender_sent(self):
        response = self.test_client.post('/register/lender/',
                            json={"name": "Wycliffe",
                                    "email": "sikoi@gmail.com",
                                    "phone_number": "0703680126",
                                    "password": "SaveTheWorld"})
        self.assertEqual(response.status_code, 409)
        self.assertEqual(response.data, b"User in db")

    def test_duplicate_borrower_sent(self):
        response = self.test_client.post('/register/borrower/',
                            json={"name": "Kefa",
                                    "email": "mutu@yahoo.com",
                                    "phone_number": "+254708456210",
                                    "password": "AmKing"})
        self.assertEqual(response.status_code, 409)
        self.assertEqual(response.data, b"User in db")

    def tearDown(self):
        src.db.session.remove()
        src.db.drop_all()
        self.ctx.pop()


if __name__ == "__main__":
    unittest.main()
