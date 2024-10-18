from flask import Flask, request, render_template
from flask import Flask, render_template, request, redirect, url_for

import mysql.connector
from mysql.connector import Error

app = Flask(__name__)

#Setting a secret key



# Database connection
def create_connection():
    try:
        connection = mysql.connector.connect(
            host='localhost',  # Change to your MySQL server address
            database='marketplace',  # Your database name
            user='root',  # Your MySQL username
            password='Draughtsman78'  # Your MySQL password
        )
        if connection.is_connected():
            print("Connected to MySQL database")
        return connection
    except Error as e:
        print(f"Error connecting to MySQL: {e}")
        return None

# Render the login and sign-up forms
@app.route('/')
def home():
    return render_template('home.html')

# Route for login sign up page
@app.route('/sign')
def signin():
    return render_template('sign.html')

#Route for forgot password
@app.route('/forgot')
def forgot():
    return render_template('forgot.html')

#Route for log
@app.route('/log')
def log():
    return render_template('log.html')

#Route for dashboard
@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

# Handle user login
@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']

    # Connect to the database and validate user credentials
    connection = create_connection()
    if connection is None:
        return "Error connecting to the database"

    cursor = connection.cursor(dictionary=True)
    query = "SELECT * FROM user_login WHERE username = %s AND password = %s"
    cursor.execute(query, (username, password))
    result = cursor.fetchone()

    cursor.close()
    connection.close()

    if result:
        return render_template('dashboard.html')
    else:
        return "Login failed. Incorrect username or password."


# Handle user sign-up and add the new user to the database
@app.route('/signup', methods=['POST'])
def signup():
    new_username = request.form['new_username']
    new_password = request.form['new_password']

    # Connect to the database
    connection = create_connection()
    if connection is None:
        return "Error connecting to the database"

    cursor = connection.cursor()

    # Check if the username already exists
    check_query = "SELECT * FROM user_login WHERE username = %s"
    cursor.execute(check_query, (new_username,))
    existing_user = cursor.fetchone()

    if existing_user:
        cursor.close()
        connection.close()
        return "Username already exists. Please choose a different username."

    # Insert new user into the database
    insert_query = "INSERT INTO user_login (username, password) VALUES (%s, %s)"
    cursor.execute(insert_query, (new_username, new_password))
    connection.commit()

    cursor.close()
    connection.close()

    return f"User {new_username} registered successfully!"

#--------Create Sellers Dashboard-------------

# Sample data for demonstration
products = [
    {'id': 1, 'name': 'Product 1', 'price': 10.00, 'quantity': 5},
    {'id': 2, 'name': 'Product 2', 'price': 15.00, 'quantity': 2},
]

orders = [
    {'order_id': 1, 'product_name': 'Product 1', 'quantity': 1, 'total': 10.00},
    {'order_id': 2, 'product_name': 'Product 2', 'quantity': 1, 'total': 15.00},
]

@app.route('/')
def another_dashboard():
    return render_template('dashboard.html', products=products, orders=orders)

@app.route('/add_product')
def add_product():
    return render_template('add_product.html')
    
if __name__ == '__main__':
    app.run(debug=True)
