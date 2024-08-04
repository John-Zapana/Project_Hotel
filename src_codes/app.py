# cd Project_Hotel
# cd src_codes
# python3 app.py

from flask import Flask, request, jsonify, render_template, redirect, url_for, flash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_bcrypt import Bcrypt
from mysql_operations import create_user, get_users, update_user, delete_user, get_user_by_id
from mongo_operations import create_booking, get_bookings, update_booking, delete_booking, create_mongo_connection
from database import create_connection
import uuid
from bson.objectid import ObjectId
from datetime import datetime
import logging
from decimal import Decimal

# Initialize Flask app
app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Replace with your actual secret key
bcrypt = Bcrypt(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Create database connections
db = create_mongo_connection()
connection = create_connection()

class User(UserMixin):
    def __init__(self, id, username, password_hash, role):
        self.id = id
        self.username = username
        self.password_hash = password_hash
        self.role = role

@login_manager.user_loader
def load_user(user_id):
    connection = create_connection()
    cursor = connection.cursor(dictionary=True)
    query = "SELECT user_id, username, password_hash, role FROM Users WHERE user_id = %s"
    cursor.execute(query, (user_id,))
    user = cursor.fetchone()
    cursor.close()
    connection.close()
    
    if user:
        return User(user['user_id'], user['username'], user['password_hash'], user['role'])
    return None

def convert_decimal_to_float(value):
    if isinstance(value, Decimal):
        return float(value)
    return value

def get_available_rooms(start_date, end_date):
    connection = create_connection()
    cursor = connection.cursor(dictionary=True)
    query = """
    SELECT room_id, room_type FROM Rooms
    WHERE room_id NOT IN (
        SELECT room_id FROM Bookings
        WHERE (check_in <= %s AND check_out >= %s)
    )
    """
    cursor.execute(query, (end_date, start_date))
    rooms = cursor.fetchall()
    cursor.close()
    connection.close()
    return rooms

def get_service_price(service_type):
    connection = create_connection()
    cursor = connection.cursor(dictionary=True)
    
    try:
        cursor.execute('SELECT fee FROM Services WHERE service_name = %s', (service_type,))
        result = cursor.fetchone()
        if result:
            return float(result['fee'])  # Convert Decimal to float if necessary
        return None
    except Exception as e:
        logging.error(f"Error retrieving service price: {e}")
        return None
    finally:
        cursor.close()
        connection.close()

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        # Fetch all users from the database
        users = get_users()
        
        # Find the user with the given username
        user = next((u for u in users if u['username'] == username), None)
        
        if user and bcrypt.check_password_hash(user['password_hash'], password):
            # Create a User object
            user_obj = User(user['user_id'], user['username'], user['password_hash'], user['role'])
            login_user(user_obj)
            
            # Redirect based on user role
            if user['role'] == 'Admin':
                return redirect(url_for('admin_dashboard'))
            else:
                return redirect(url_for('home'))
        else:
            flash('Invalid username or password')

    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        role = request.form.get('role')
        password_hash = bcrypt.generate_password_hash(password).decode('utf-8')
        create_user(username, password_hash, role)
        flash('Account created successfully! Please log in.')
        return redirect(url_for('login'))
    return render_template('signup.html')
    
@app.route('/admin_dashboard')
@login_required
def admin_dashboard():
    if current_user.role != 'Admin':
        flash('You do not have permission to access this page.')
        return redirect(url_for('home'))
    
    return render_template('admin_dashboard.html')
    
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
    if current_user.role == 'Customer':
        if request.method == 'POST':
            room_type = request.form.get('room_type')
            check_in_date = request.form.get('check_in')
            check_out_date = request.form.get('check_out')

            if not all([room_type, check_in_date, check_out_date]):
                flash('Please provide all required fields.')
                return redirect(url_for('booking'))

            available_rooms = []
            unavailable_rooms = set()  # Temporarily unavailable rooms

            connection = create_connection()
            if not connection:
                flash('Failed to connect to the database.')
                return redirect(url_for('booking'))

            try:
                cursor = connection.cursor()
                cursor.execute('SELECT room_id, price FROM Rooms WHERE room_type = %s', (room_type,))
                rooms = cursor.fetchall()

                for room in rooms:
                    try:
                        room_id = int(room[0])  # Access room_id using index 0
                        price = float(room[1])  # Access price using index 1
                    except ValueError:
                        print(f"Invalid value for room: {room}")
                        continue

                    # Check if the room is booked during the period
                    query = {
                        'room_id': room_id,
                        'check_in': {'$lte': check_out_date},
                        'check_out': {'$gte': check_in_date}
                    }

                    if db['Bookings'].find_one(query):
                        unavailable_rooms.add(room_id)
                    else:
                        available_rooms.append({
                            'room_id': room_id,
                            'price': price
                        })
            finally:
                cursor.close()  # Ensure cursor is closed
                connection.close()  # Ensure connection is closed

            if not available_rooms:
                flash('No rooms available for the selected criteria.')
                return redirect(url_for('booking'))

            return render_template('booking.html', available_rooms=available_rooms, check_in_date=check_in_date, check_out_date=check_out_date, room_type=room_type)

        return render_template('booking.html')

    elif current_user.role == 'Manager':
        if request.method == 'POST':
            booking_id = request.form.get('booking_id')
            action = request.form.get('action')  # 'approve' or 'reject'
            
            if action == 'approve':
                update_booking(db, booking_id, {'status': 'Approved'})
                flash('Booking approved successfully.')
            elif action == 'reject':
                update_booking(db, booking_id, {'status': 'Rejected'})
                flash('Booking rejected successfully.')
            else:
                flash('Invalid action.')

            return redirect(url_for('booking'))

        # Display bookings for manager
        all_bookings = get_bookings(db)
        
        # Filter bookings based on their status
        pending_bookings = [booking for booking in all_bookings if booking.get('status') == 'Pending']
        approved_bookings = [booking for booking in all_bookings if booking.get('status') == 'Approved']
        rejected_bookings = [booking for booking in all_bookings if booking.get('status') == 'Rejected']
        
        return render_template('booking.html', 
                               is_manager=True, 
                               pending_bookings=pending_bookings, 
                               approved_bookings=approved_bookings, 
                               rejected_bookings=rejected_bookings)

    flash('Unauthorized access')
    return redirect(url_for('home'))

@app.route('/confirm_booking', methods=['POST'])
@login_required
def confirm_booking():
    room_id = request.form.get('room_id')
    check_in_date = request.form.get('check_in_date')
    check_out_date = request.form.get('check_out_date')
    room_type = request.form.get('room_type')
    
    if not all([room_id, check_in_date, check_out_date, room_type]):
        flash('Please provide all required fields.')
        return redirect(url_for('booking'))
    
    current_time = datetime.utcnow()
    booking_id = str(current_time.timestamp())
    
    connection = create_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute('SELECT price FROM Rooms WHERE room_id = %s', (room_id,))
    price = cursor.fetchone()['price']
    cursor.close()
    connection.close()

    # Convert price to float if it's a Decimal
    price = convert_decimal_to_float(price)

    # Create booking record in MongoDB
    db['Bookings'].insert_one({
        'booking_id': booking_id,
        'user_id': current_user.id,
        'room_id': room_id,
        'check_in': check_in_date,
        'check_out': check_out_date,
        'status': 'Pending',
        'room_type': room_type,
        'price': price
    })

    flash(f'Room {room_id} has been booked successfully for check-in on {check_in_date} and check-out on {check_out_date}.')
    return redirect(url_for('booking'))

@app.route('/check_availability', methods=['POST'])
@login_required
def check_availability():
    start_date = request.form.get('start_date')
    end_date = request.form.get('end_date')

    if not all([start_date, end_date]):
        flash('Please provide both start and end dates.')
        return redirect(url_for('booking'))

    available_rooms = get_available_rooms(start_date, end_date)
    return render_template('availability.html', available_rooms=available_rooms)

@app.route('/room_service', methods=['GET', 'POST'])
@login_required
def room_service():
    if request.method == 'POST':
        service_type = request.form.get('service_type')

        if current_user.role == 'Customer':
            room_number = None
        else:
            room_number = request.form.get('room_number')

        service_price = get_service_price(service_type)
        if not service_price:
            flash('Invalid service type.')
            return redirect(url_for('room_service'))

        # Save service request to MySQL and cache in MongoDB
        connection = create_connection()
        cursor = connection.cursor()
        cursor.execute('INSERT INTO RoomServiceRequests (user_id, room_number, service_type, service_price, request_time) VALUES (%s, %s, %s, %s, %s)',
                       (current_user.id, room_number, service_type, service_price, datetime.utcnow()))
        connection.commit()
        cursor.close()
        connection.close()

        db['RoomServiceRequests'].insert_one({
            'user_id': current_user.id,
            'room_number': room_number,
            'service_type': service_type,
            'service_price': service_price,
            'request_time': datetime.utcnow()
        })

        flash(f'Service request for {service_type} has been submitted successfully.')
        return redirect(url_for('room_service'))

    service_types = ['Food', 'Beverage', 'Cleaning', 'Other']
    return render_template('room_service.html', service_types=service_types)

@app.route('/financial_reports')
@login_required
def financial_reports():
    if current_user.role != 'Manager':
        flash('You do not have permission to access this page.')
        return redirect(url_for('home'))

    # Fetch monthly and quarterly revenue from MongoDB
    monthly_revenue = db['MonthlyRevenue'].find()  # Adjust the collection name and query as needed
    quarterly_revenue = db['QuarterlyRevenue'].find()  # Adjust the collection name and query as needed

    # Convert data to list of dictionaries if necessary
    monthly_revenue_list = list(monthly_revenue)
    quarterly_revenue_list = list(quarterly_revenue)

    return render_template('financial_reports.html', 
                           monthly_revenue=monthly_revenue_list,
                           quarterly_revenue=quarterly_revenue_list)

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
        flash('Your message has been sent successfully!')
        return redirect(url_for('contact'))
    return render_template('contact.html')
    
@app.template_filter('format_currency')
def format_currency(value):
    return "${:,.2f}".format(value)


@app.route('/checkin_checkout', methods=['GET', 'POST'])
@login_required
def checkin_checkout():
    if request.method == 'POST':
        action = request.form.get('action')
        booking_id = request.form.get('booking_id')

        if not booking_id:
            flash('Booking ID is required.')
            return redirect(url_for('checkin_checkout'))

        booking = db['Bookings'].find_one({'_id': ObjectId(booking_id)})

        if not booking:
            flash('Booking not found.')
            return redirect(url_for('checkin_checkout'))

        if action == 'Check-In':
            db['Bookings'].update_one(
                {'_id': ObjectId(booking_id)},
                {'$set': {'availability': 'unavailable'}}
            )
            flash(f'Room {booking["room_id"]} checked in successfully.')

        elif action == 'Check-Out':
            db['Bookings'].update_one(
                {'_id': ObjectId(booking_id)},
                {'$set': {'availability': 'available', 'status': 'ReadyForBilling'}}
            )
            flash(f'Room {booking["room_id"]} checked out successfully.')

        return redirect(url_for('checkin_checkout'))

    if current_user.role == 'Staff':
        rooms = db['Bookings'].find({'status': 'Approved'})
        return render_template('checkin_checkout.html', rooms=rooms)

    flash('Unauthorized access')
    return redirect(url_for('home'))

@app.route('/view_availability', methods=['GET', 'POST'])
@login_required
def view_availability():
    if current_user.role != 'Manager':
        flash('Unauthorized access')
        return redirect(url_for('home'))

    if request.method == 'POST':
        start_date = request.form.get('start_date')
        end_date = request.form.get('end_date')

        if start_date and end_date:
            available_rooms = get_available_rooms(start_date, end_date)
            return render_template('view_availability.html', available_rooms=available_rooms)
        else:
            flash('Start date and end date are required.')
            return redirect(url_for('view_availability'))

    # For GET requests, just render the page with no rooms
    return render_template('view_availability.html')




 

@app.route('/manage_users')
@login_required
def manage_users():
    if current_user.role != 'Admin':
        flash('You do not have permission to access this page.')
        return redirect(url_for('home'))
    
    users = get_users()
    return render_template('manage_users.html', users=users)
    
@app.route('/view_bookings')
@login_required
def view_bookings():
    if current_user.role != 'Admin':
        flash('You do not have permission to access this page.')
        return redirect(url_for('home'))
    
    bookings = get_bookings(db)
    return render_template('view_bookings.html', bookings=bookings)
    
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
