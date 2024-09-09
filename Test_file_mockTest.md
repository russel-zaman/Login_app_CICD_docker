This file is created To keep a test file and mock test file 
And how to run test file 



----------------------Normal test_app.py file------------------------------------------
import unittest
from flask import session
from app import app


"""
This module contains unit tests for the Flask application.
"""
class FlaskTestCase(unittest.TestCase):
    """Unit tests for Flask application."""
    # Ensure that Flask was set up correctly
    def test_home(self):
        tester = app.test_client(self)
        response = tester.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Login', response.data)  # Check if 'Login' is in the HTML

    # Ensure login behaves correctly with correct credentials
    def test_login_success(self):
        tester = app.test_client(self)
        response = tester.post('/login',
                       data={"username": "db", "password": "1234567"},
                       follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Logged in successfully!', response.data)

    # Ensure login behaves correctly with incorrect credentials
    def test_login_failure(self):
        tester = app.test_client(self)
        response = tester.post('/login', data=dict(username="wrong_user", password="wrong_password"), follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Incorrect username / password!', response.data)

    # Ensure that registration works with valid details
    def test_register(self):
        tester = app.test_client(self)
        response = tester.post('/register', data=dict(username="new_user", password="new_password", email="newuser@example.com"), follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'You have successfully registered!', response.data)

    # Ensure logout works properly
    def test_logout(self):
        tester = app.test_client(self)
        tester.post('/login', data=dict(username="db", password="1234567"), follow_redirects=True)  # Correct credentials for login
        response = tester.get('/logout', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertNotIn('loggedin', session)  # Check if the user is logged out

if __name__ == '__main__':
    unittest.main()




-----------------------------End-----------------------------------------------









--------------------test_app.py file with mock test include ----------------------


import unittest
from unittest.mock import patch, MagicMock
from flask import session
from app import app

class FlaskTestCase(unittest.TestCase):
    """Unit tests for Flask application."""

    @patch('app.mysql.connection.cursor')
    def test_login_success(self, mock_cursor):
        # Mock the cursor and its methods
        mock_cursor.return_value = MagicMock()
        mock_cursor.return_value.fetchone.return_value = {
            'id': 1,
            'username': 'db',
            'password': '1234567'
        }

        tester = app.test_client(self)
        response = tester.post('/login',
                               data={"username": "db", "password": "1234567"},
                               follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Logged in successfully!', response.data)

    @patch('app.mysql.connection.cursor')
    def test_login_failure(self, mock_cursor):
        # Mock the cursor and its methods
        mock_cursor.return_value = MagicMock()
        mock_cursor.return_value.fetchone.return_value = None

        tester = app.test_client(self)
        response = tester.post('/login',
                               data={"username": "wrong_user", "password": "wrong_password"},
                               follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Incorrect username / password!', response.data)

    @patch('app.mysql.connection.cursor')
    def test_register_success(self, mock_cursor):
        # Mock the cursor and its methods
        mock_cursor.return_value = MagicMock()
        mock_cursor.return_value.fetchone.return_value = None

        tester = app.test_client(self)
        response = tester.post('/register',
                               data={"username": "new_user", "password": "new_password", "email": "newuser@example.com"},
                               follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'You have successfully registered!', response.data)

    @patch('app.mysql.connection.cursor')
    def test_register_failure(self, mock_cursor):
        # Mock the cursor and its methods
        mock_cursor.return_value = MagicMock()
        mock_cursor.return_value.fetchone.return_value = {'username': 'existing_user'}

        tester = app.test_client(self)
        response = tester.post('/register',
                               data={"username": "existing_user", "password": "some_password", "email": "existing@example.com"},
                               follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Account already exists!', response.data)

    @patch('app.mysql.connection.cursor')
    def test_logout(self, mock_cursor):
        # Mock the cursor and its methods
        mock_cursor.return_value = MagicMock()
        mock_cursor.return_value.fetchone.return_value = {
            'id': 1,
            'username': 'db',
            'password': '1234567'
        }

        tester = app.test_client(self)
        tester.post('/login', data={"username": "db", "password": "1234567"}, follow_redirects=True)
        response = tester.get('/logout', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertNotIn('loggedin', session)  # Check if the user is logged out

if __name__ == '__main__':
    unittest.main()



----------------------------End -----------------------------------------





Explanation:
@patch('app.mysql.connection.cursor'): This decorator is used to replace the cursor method on app.mysql.connection with a mock object during the test.

MagicMock(): This is used to create a mock object that can be configured to return specific values when methods are called.

mock_cursor.return_value.fetchone.return_value: Configures what the fetchone() method of the mocked cursor should return.

Test cases:
test_login_success: Tests successful login with correct credentials.
test_login_failure: Tests login failure with incorrect credentials.
test_register_success: Tests successful registration.
test_register_failure: Tests registration failure due to existing username.
test_logout: Tests logout functionality.


Running the Tests

To run your tests, execute the following command from the root directory of your project:

python -m unittest discover -s tests

or

pytest


This will execute all the test cases defined in test_app.py and provide you with the results.