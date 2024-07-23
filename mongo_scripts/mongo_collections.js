// Bookings Collection
{
    "_id": "booking1",  // Unique identifier for the booking
    "user_id": 2,       // ID of the user who made the booking
    "room_id": 101,     // ID of the room booked
    "check_in": "2024-08-01",  // Check-in date
    "check_out": "2024-08-05", // Check-out date
    "status": "Confirmed"      // Booking status (e.g., Pending, Approved, Rejected)
}

// Check-Ins Collection
{
    "_id": "checkin1",    // Unique identifier for the check-in record
    "booking_id": "booking1", // ID of the associated booking
    "user_id": 2,         // ID of the user who checked in
    "room_id": 101,       // ID of the room checked into
    "check_in_time": "2024-08-01T14:00:00Z", // Date and time of check-in
    "status": "Checked In" // Current status (e.g., Checked In, Checked Out)
}

// Room Services Collection
{
    "_id": "service1",       // Unique identifier for the service request
    "booking_id": "booking1", // ID of the associated booking
    "user_id": 2,            // ID of the user who made the service request
    "service_type": "Extra Towels", // Type of service requested
    "request_time": "2024-08-02T10:00:00Z", // Time when the request was made
    "status": "Pending"      // Current status of the request (e.g., Pending, Fulfilled, Cancelled)
}

// Fees Collection
{
    "_id": "fee1",         // Unique identifier for the fee record
    "room_type": "Deluxe", // Type of room
    "price_per_night": 150, // Price per night for the room
    "service_type": "Room Cleaning", // Type of service
    "price": 20             // Price of the service
}

// Rules Collection
{
    "_id": "rule1",        // Unique identifier for the rule
    "rule_type": "Check-In", // Type of rule (e.g., Check-In, Check-Out)
    "time": "15:00:00",     // Required time for check-in/check-out
    "description": "Standard check-in time is 3 PM" // Description of the rule
}