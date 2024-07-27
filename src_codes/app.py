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
import uuid

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
        username = request.form.get('username')
        password = request.form.get('password')
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
        username = request.form.get('username')
        password = request.form.get('password')
        role = request.form.get('role')  # Retrieve the role from the form
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
    available_rooms = []
    room_type = None
    check_in_date = None
    check_out_date = None

    if request.method == 'POST':
        room_type = request.form.get('room_type')
        check_in_date = request.form.get('check_in')
        check_out_date = request.form.get('check_out')

        # Debug print statements
        print(f"Booking form data - room_type: {room_type}, check_in: {check_in_date}, check_out: {check_out_date}")

        if not all([room_type, check_in_date, check_out_date]):
            flash('Please fill out all required fields.')
            return redirect(url_for('booking'))

        available_rooms = check_room_availability(room_type, check_in_date, check_out_date)
        return render_template('booking.html', available_rooms=available_rooms, room_type=room_type, check_in_date=check_in_date, check_out_date=check_out_date)

    return render_template('booking.html', available_rooms=available_rooms, room_type=room_type, check_in_date=check_in_date, check_out_date=check_out_date)

@app.route('/select_room', methods=['POST'])
@login_required
def select_room():
    room_id = request.form.get('room_id')
    check_in_date = request.form.get('check_in_date')
    check_out_date = request.form.get('check_out_date')
    room_type = request.form.get('room_type')
    status = request.form.get('status', 'Pending')

    # Debug print statements
    print(f"Room selection data - room_id: {room_id}, check_in: {check_in_date}, check_out: {check_out_date}, room_type: {room_type}, status: {status}")

    if not all([room_id, check_in_date, check_out_date, room_type]):
        flash('Please provide all required fields.')
        return redirect(url_for('booking'))

    create_booking(db, current_user.id, room_id, check_in_date, check_out_date, status, room_type)
    flash(f'Room {room_id} has been booked successfully for check-in on {check_in_date} and check-out on {check_out_date}.')
    return redirect(url_for('booking'))

def check_room_availability(room_type, check_in_date, check_out_date):
    bookings = get_bookings(db)
    unavailable_rooms = set()

    # Define room numbers based on room type
    room_types = {
        'single': ["101", "102", "103", "104"],
        'double': ["201", "202", "203", "204"],
        'suite': ["301", "302", "303", "304"]
    }
    
    all_rooms = room_types.get(room_type, [])

    # Filter out rooms that are not available for the given date range
    for booking in bookings:
        if 'room_type' in booking and booking['room_type'] == room_type:
            if not (booking['check_out'] < check_in_date or booking['check_in'] > check_out_date):
                unavailable_rooms.add(booking['room_id'])

    # Get rooms that are not in the unavailable list
    available_rooms = [room for room in all_rooms if room not in unavailable_rooms]

    return available_rooms

@app.route('/checkin_checkout', methods=['GET', 'POST'])
@login_required
def checkin_checkout():
    if current_user.role not in ['Staff', 'Admin']:
        flash('You do not have permission to access this page.')
        return redirect(url_for('home'))
    if request.method == 'POST':
        # Implement check-in/check-out logic here
        flash("Check-In/Check-Out processed successfully")
        return redirect(url_for('checkin_checkout'))
    return render_template('checkin_checkout.html')

@app.route('/room_service', methods=['GET', 'POST'])
@login_required
def room_service():
    if current_user.role not in ['Staff', 'Admin']:
        flash('You do not have permission to access this page.')
        return redirect(url_for('home'))
    if request.method == 'POST':
        # Implement room service logic here
        flash("Room Service request processed successfully")
        return redirect(url_for('room_service'))
    return render_template('room_service.html')

@app.route('/fees_rules')
def fees_rules():
    return render_template('fees_rules.html')

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        subject = request.form.get('subject')
        message = request.form.get('message')
        # Add logic to process the contact form data
        flash('Your message has been sent successfully!')
        return redirect(url_for('contact'))
    return render_template('contact.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)