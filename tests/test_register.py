# test for request method
def test_wrong_method(test_client):
    """GIVEN a flask app
    WHEN the '/register/*' requests are made with GET
    THEN check if wrong method status code is sent -> 405
    """
    lender_response = test_client.get('/register/lender/')
    borrower_response = test_client.get('/register/borrower/')
    assert lender_response.status_code == 405
    assert borrower_response.status_code == 405


# test for when no body is sent
def test_no_body_sent(test_client):
    """GIVEN a flask app
    WHEN no body is sent to '/register/*' url with POST
    THEN check if '400' is sent
    """
    response = test_client.post('/register/lender/', json=None)
    assert response.status_code == 400


def test_add_lender(test_client, mock_db):
    """GIVEN a flask app
    WHEN a user tries to register again
    THEN check if error is raised
    """
    response = test_client.post('/register/lender/', json={"name": "Eric", "email": "macha@gmail.com", "phone_number": "0704900126", "password": "qwerty"})
    assert response.status_code == 200
    assert b"Lender has been added" in response.data


def test_duplicate_lender_sent(test_client, mock_db):
    """GIVEN a flask app
    WHEN a user tries to register again
    THEN check if error is raised
    """
    response = test_client.post('/register/lender/', json={"name": "Wycliffe", "email": "sikoi@gmail.com", "phone_number": "0703680126", "password": "SaveTheWorld"})
    assert response.status_code == 409
    assert b"User in db" in response.data


def test_duplicate_borrower_sent(test_client, mock_db):
    """GIVEN a flask app
    WHEN a user tries to register again
    THEN check if error is raised
    """
    response = test_client.post('/register/borrower/', json={"name": "Kefa", "email": "mutu@yahoo.com", "phone_number": "+254708456210", "password": "AmKing"})
    assert response.status_code == 409
    assert b"User in db" in response.data


def test_malformed_data_sent(test_client):
    """GIVEN a flask app
    WHEN a user sends incomplete data
    THEN check if error is raised
    """
    response = test_client.post('/register/lender/', json={"name": "Wycliffe", "email": "sikoi@gmail.com", "password": "SaveTheWorld"})
    assert response.status_code == 400
    assert b"phone_number" in response.data
