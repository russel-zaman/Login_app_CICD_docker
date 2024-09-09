from flask import Flask
from flask_mysqldb import MySQL

app = Flask(__name__)
app.secret_key = 'secret'

# Configuration
app.config['MYSQL_HOST'] = "db"
app.config['MYSQL_USER'] = "flask"
app.config['MYSQL_PASSWORD'] = "1234567"
app.config['MYSQL_DATABASE'] = "geeklogin"
app.config['MYSQL_PORT'] = 3306

mysql = MySQL(app)

from app import routes  # Import routes after initializing the app and MySQL
