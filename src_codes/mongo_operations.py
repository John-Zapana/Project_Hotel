# cd Project_Hotel
# cd src_codes
# python3 mongo_operations.py

from pymongo import MongoClient
import uuid
from datetime import datetime

def create_mongo_connection():
    """Create a MongoDB connection."""
    connection_string = "mongodb+srv://carlossibaja24:DouglasDB2@clusterproject.nj7kypt.mongodb.net/"
    client = MongoClient(connection_string)
    db = client['starlight_hotel_db']
    print("Successfully connected to MongoDB database")
    return db

def validate_date(date_str):
    """Validate date format."""
    try:
        datetime.strptime(date_str, '%Y-%m-%d')
        return True
    except ValueError:
        return False

def create_booking(db, user_id, room_id, check_in, check_out, status='Pending', room_type=None):
    """Create a new booking in MongoDB with validation."""
    bookings_collection = db['Bookings']
    
    # Debug prints
    print(f"Creating booking with user_id={user_id}, room_id={room_id}, check_in={check_in}, check_out={check_out}, status={status}, room_type={room_type}")
    
    # Validate dates
    if not (validate_date(check_in) and validate_date(check_out)):
        print("Invalid date format. Use YYYY-MM-DD.")
        return

    # Validate status
    valid_statuses = ['Pending', 'Confirmed', 'Cancelled']
    if status not in valid_statuses:
        print("Invalid status. Must be one of ['Pending', 'Confirmed', 'Cancelled'].")
        return

    if room_type is None:
        print("Room type must be provided.")
        return

    booking_id = str(uuid.uuid4())  # Generate a unique booking ID
    booking_document = {
        "booking_id": booking_id,
        "user_id": user_id,
        "room_id": room_id,
        "check_in": check_in,
        "check_out": check_out,
        "status": status,
        "room_type": room_type  # Ensure room_type is always included
    }
    
    try:
        result = bookings_collection.insert_one(booking_document)
        if result.acknowledged:
            print(f"Booking {booking_id} created successfully with details: {booking_document}")
        else:
            print("Booking insertion was not acknowledged.")
    except Exception as e:
        print(f"Failed to create booking: {e}")

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

#if __name__ == "__main__":
#    db = create_mongo_connection()
    # Test CRUD operations with validation
#    create_booking(db, None, "user2", "room102", "2024-07-29", "2024-07-31", "Pending", "suite")  # Valid booking
#    bookings = get_bookings(db)
#    print("Bookings in database:", bookings)