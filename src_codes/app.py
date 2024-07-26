# pip install flask-login
# pip install flask-bcrypt

# cd Project_Hotel
# cd src_codes
# python3 app.py

from flask import Flask, request, jsonify, render_template, redirect, url_for, flash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_bcrypt import Bcrypt
from mysql_operations import create_user, get_users, update_user, delete_user
from mongo_operations import create_booking, get_bookings, update_booking, delete_booking, create_mongo_connection

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Replace with your actual secret key
bcrypt = Bcrypt(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

db = create_mongo_connection()

class User(UserMixin):
    def __init__(self, id, username, password_hash, role):
        self.id = id
        self.username = username
        self.password_hash = password_hash
        self.role = role

@login_manager.user_loader
def load_user(user_id):
    users = get_users()
    for user in users:
        if user['user_id'] == int(user_id):
            return User(user['user_id'], user['username'], user['password_hash'], user['role'])
    return None

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        users = get_users()
        for user in users:
            if user['username'] == username and bcrypt.check_password_hash(user['password_hash'], password):
                user_obj = User(user['user_id'], user['username'], user['password_hash'], user['role'])
                login_user(user_obj)
                return redirect(url_for('home'))
        flash('Invalid username or password')
    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        role = request.form['role']  # Retrieve the role from the form
        password_hash = bcrypt.generate_password_hash(password).decode('utf-8')
        create_user(username, password_hash, role)
        flash('Account created successfully! Please log in.')
        return redirect(url_for('login'))
    return render_template('signup.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/booking', methods=['GET', 'POST'])
@login_required
def booking():
    if request.method == 'POST':
        data = request.form
        if current_user.role == 'Customer':
            # Handle booking without status
            create_booking(db, data['booking_id'], data['user_id'], data['room_id'], data['check_in'], data['check_out'])
        else:
            # Handle booking with status
            status = data.get('status')  # Use .get() to avoid KeyError
            create_booking(db, data['booking_id'], data['user_id'], data['room_id'], data['check_in'], data['check_out'], status)
        
        flash("Booking created successfully")
        return redirect(url_for('booking'))
    return render_template('booking.html')

@app.route('/checkin_checkout', methods=['GET', 'POST'])
@login_required
def checkin_checkout():
    if current_user.role not in ['Staff', 'Admin']:
        flash('You do not have permission to access this page.')
        return redirect(url_for('home'))
    if request.method == 'POST':
        # Implement check-in/check-out logic here
        return jsonify({"message": "Check-In/Check-Out processed successfully"}), 201
    return render_template('checkin_checkout.html')

@app.route('/room_service', methods=['GET', 'POST'])
@login_required
def room_service():
    if current_user.role not in ['Staff', 'Admin']:
        flash('You do not have permission to access this page.')
        return redirect(url_for('home'))
    if request.method == 'POST':
        # Implement room service logic here
        return jsonify({"message": "Room Service request processed successfully"}), 201
    return render_template('room_service.html')

@app.route('/fees_rules')
def fees_rules():
    return render_template('fees_rules.html')

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        subject = request.form['subject']
        message = request.form['message']
        # Add logic to process the contact form data
        flash('Your message has been sent successfully!')
        return redirect(url_for('contact'))
    return render_template('contact.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
