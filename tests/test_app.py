import unittest
from unittest.mock import patch, MagicMock
from app import app, mysql

class FlaskTestCase(unittest.TestCase):
    """Unit tests for Flask application."""
    
    def setUp(self):
        self.app = app
        self.app.config['TESTING'] = True
        self.client = self.app.test_client()
        self.mock_cursor = MagicMock()
        self.mock_connection = MagicMock()
        self.mock_connection.cursor.return_value = self.mock_cursor
        
        # Patch the mysql object in the app module
        self.patcher = patch('app.mysql', self.mock_connection)
        self.patcher.start()

    def tearDown(self):
        self.patcher.stop()

    def test_home(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Login', response.data)

    @patch('app.mysql.connection.cursor')
    def test_login_success(self, mock_cursor):
        mock_cursor.return_value = self.mock_cursor
        self.mock_cursor.fetchone.return_value = {'id': 1, 'username': 'db'}
        
        response = self.client.post('/login',
                       data={"username": "db", "password": "1234567"},
                       follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Logged in successfully!', response.data)

    @patch('app.mysql.connection.cursor')
    def test_login_failure(self, mock_cursor):
        mock_cursor.return_value = self.mock_cursor
        self.mock_cursor.fetchone.return_value = None
        
        response = self.client.post('/login',
                       data={"username": "wrong_user", "password": "wrong_password"},
                       follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Incorrect username / password!', response.data)

    @patch('app.mysql.connection.cursor')
    def test_register_success(self, mock_cursor):
        mock_cursor.return_value = self.mock_cursor
        self.mock_cursor.fetchone.return_value = None
        
        response = self.client.post('/register',
                       data={"username": "new_user", "password": "new_password", "email": "newuser@example.com"},
                       follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'You have successfully registered!', response.data)

    @patch('app.mysql.connection.cursor')
    def test_register_failure(self, mock_cursor):
        mock_cursor.return_value = self.mock_cursor
        self.mock_cursor.fetchone.return_value = {'username': 'existing_user'}
        
        response = self.client.post('/register',
                       data={"username": "existing_user", "password": "password", "email": "existing@example.com"},
                       follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Account already exists!', response.data)

    @patch('app.mysql.connection.cursor')
    def test_logout(self, mock_cursor):
        response = self.client.get('/logout', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        with self.client.session_transaction() as sess:
            self.assertNotIn('loggedin', sess)

if __name__ == '__main__':
    unittest.main()
