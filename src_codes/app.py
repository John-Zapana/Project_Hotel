# cd Project_Hotel
# cd src_codes
# python3 app.py

from flask import Flask, request, jsonify, render_template
from mysql_operations import create_user, get_users, update_user, delete_user
from mongo_operations import create_booking, get_bookings, update_booking, delete_booking, create_mongo_connection

app = Flask(__name__)
db = create_mongo_connection()

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/booking', methods=['GET', 'POST'])
def booking():
    if request.method == 'POST':
        data = request.json
        create_booking(db, data['booking_id'], data['user_id'], data['room_id'], data['check_in'], data['check_out'], data['status'])
        return jsonify({"message": "Booking created successfully"}), 201
    return render_template('booking.html')

@app.route('/checkin_checkout', methods=['GET', 'POST'])
def checkin_checkout():
    if request.method == 'POST':
        # Implement check-in/check-out logic here
        return jsonify({"message": "Check-In/Check-Out processed successfully"}), 201
    return render_template('checkin_checkout.html')

@app.route('/room_service', methods=['GET', 'POST'])
def room_service():
    if request.method == 'POST':
        # Implement room service logic here
        return jsonify({"message": "Room Service request processed successfully"}), 201
    return render_template('room_service.html')

@app.route('/fees_rules')
def fees_rules():
    return render_template('fees_rules.html')
    
@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/users', methods=['GET'])
def get_all_users():
    users = get_users()
    return jsonify(users)

@app.route('/users', methods=['POST'])
def add_user():
    data = request.json
    create_user(data['username'], data['password_hash'], data['role'])
    return jsonify({"message": "User created successfully"}), 201

@app.route('/bookings', methods=['GET'])
def get_all_bookings():
    bookings = get_bookings(db)
    return jsonify(bookings)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)