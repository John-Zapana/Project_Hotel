# mongo_operations.py
# cd Project_Hotel
# cd src_codes
# python3 mongo_operations.py

from pymongo import MongoClient
import uuid
from datetime import datetime
import time
import random

def create_mongo_connection():
    """Create a MongoDB connection."""
    connection_string = "mongodb+srv://carlossibaja24:DouglasDB2@clusterproject.nj7kypt.mongodb.net/"
    client = MongoClient(connection_string)
    db = client['starlight_hotel_db']
    print("Successfully connected to MongoDB database")
    return db
    
def validate_date(date_str):
    """Validate date format YYYY-MM-DD."""
    try:
        datetime.datetime.strptime(date_str, '%Y-%m-%d')
        return True
    except ValueError:
        return False

def generate_booking_id():
    return f"{int(time.time())}{random.randint(1000, 9999)}"

def create_booking(db, user_id, room_id, check_in, check_out, status='Pending', room_type=None):
    """Create a new booking in MongoDB with validation."""
    bookings_collection = db['Bookings']
    
    # Debug prints
    print(f"Creating booking with user_id={user_id}, room_id={room_id}, check_in={check_in}, check_out={check_out}, status={status}, room_type={room_type}")
    
    # Validate dates
    if not (validate_date(check_in) and validate_date(check_out)):
        print("Invalid date format. Use YYYY-MM-DD.")
        return

    # Generate booking ID
    booking_id = generate_booking_id()

    # Construct the booking document
    booking = {
        'booking_id': booking_id,
        'user_id': user_id,
        'room_id': int(room_id),  # Ensure room_id is stored as an integer
        'check_in': check_in,
        'check_out': check_out,
        'status': status,
        'room_type': room_type
    }

    # Insert into MongoDB
    bookings_collection.insert_one(booking)
    print("Booking successfully created.")

def get_bookings(db):
    """Get all bookings from MongoDB."""
    bookings_collection = db['Bookings']
    return list(bookings_collection.find())

def update_booking(db, booking_id, updated_fields):
    """Update an existing booking in MongoDB."""
    bookings_collection = db['Bookings']
    result = bookings_collection.update_one({"booking_id": booking_id}, {"$set": updated_fields})
    if result.modified_count == 0:
        print(f"No booking found with booking_id={booking_id} to update.")
    else:
        print(f"Booking {booking_id} updated successfully.")

def delete_booking(db, booking_id):
    """Delete a booking from MongoDB."""
    bookings_collection = db['Bookings']
    result = bookings_collection.delete_one({"booking_id": booking_id})
    if result.deleted_count == 0:
        print(f"No booking found with booking_id={booking_id} to delete.")
    else:
        print(f"Booking {booking_id} deleted successfully.")
