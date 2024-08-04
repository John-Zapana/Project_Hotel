from pymongo import MongoClient
from bson import ObjectId
import datetime

# Connect to MongoDB (make sure to replace 'your_connection_string' with your actual connection string)
client = MongoClient("mongodb+srv://carlossibaja24:DouglasDB2@clusterproject.nj7kypt.mongodb.net")
db = client['starlight_hotel_db']

# Sample service data
sample_service = {
    'booking_id': ObjectId('66a4b1d38592666a8eedeacb'),
    'room_id': '101',
    'service_type': 'Food',
    'quantity': 3,
    'service_date': datetime.datetime.utcnow(),
    'status': 'Pending',
    'created_at': datetime.datetime.utcnow(),
    'updated_at': datetime.datetime.utcnow()
}

# Insert the sample service into the 'Services' collection
result = db['Services'].insert_one(sample_service)
print(f"Inserted document ID: {result.inserted_id}")

# cd Project_Hotel
# cd src_codes
# python3 app.py