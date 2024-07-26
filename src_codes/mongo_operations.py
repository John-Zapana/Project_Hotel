# cd Project_Hotel
# cd src_codes
# python3 mongo_operations.py

from pymongo import MongoClient

def create_mongo_connection():
    """ Create a MongoDB connection """
    connection_string = "mongodb+srv://carlossibaja24:DouglasDB2@clusterproject.nj7kypt.mongodb.net/"
    client = MongoClient(connection_string)
    db = client['starlight_hotel_db']
    print("Successfully connected to MongoDB database")
    return db
    
def create_booking(db, booking_id, user_id, room_id, check_in, check_out, status=None, room_type=None):
    """Create a new booking in the Bookings collection."""
    try:
        bookings = db['Bookings']
        booking = {
            "_id": booking_id,
            "user_id": user_id,
            "room_id": room_id,
            "check_in": check_in,
            "check_out": check_out
        }
        if status is not None:
            booking["status"] = status
        if room_type is not None:
            booking["room_type"] = room_type
        bookings.insert_one(booking)
        print("Booking created successfully")
    except Exception as e:
        print(f"An error occurred: {e}")

def get_bookings(db):
    """Retrieve all bookings from the Bookings collection."""
    bookings = db['Bookings']
    return list(bookings.find())

def update_booking(db, booking_id, update_fields):
    """Update booking information in the Bookings collection."""
    bookings = db['Bookings']
    bookings.update_one({"_id": booking_id}, {"$set": update_fields})
    print("Booking updated successfully")

def delete_booking(db, booking_id):
    """Delete a booking from the Bookings collection."""
    bookings = db['Bookings']
    bookings.delete_one({"_id": booking_id})
    print("Booking deleted successfully")
    
    
if __name__ == "__main__":
    db = create_mongo_connection()
    
    # Test CRUD operations
    create_booking(db, "booking123", "user1", "room101", "2024-07-25", "2024-07-30", "confirmed")
    bookings = get_bookings(db)
    print("Bookings in database:", bookings)