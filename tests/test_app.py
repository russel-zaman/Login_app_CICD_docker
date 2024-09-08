import unittest
from app import app
from flask import session

class FlaskTestCase(unittest.TestCase):

    # Ensure that Flask was set up correctly
    def test_home(self):
        tester = app.test_client(self)
        response = tester.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Login', response.data)  # Check if 'Login' is in the HTML

    # Ensure login behaves correctly with correct credentials
    def test_login_success(self):
        tester = app.test_client(self)
        response = tester.post('/login', data=dict(username="correct_user", password="correct_password"), follow_redirects=True)
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
        tester.post('/login', data=dict(username="correct_user", password="correct_password"), follow_redirects=True)
        response = tester.get('/logout', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertNotIn('loggedin', session)  # Check if the user is logged out

if __name__ == '__main__':
    unittest.main()
