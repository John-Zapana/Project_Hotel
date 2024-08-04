# cd Project_Hotel
# cd src_codes
# python3 mysql_operations.py

from database import create_connection

def create_user(username, password_hash, role):
    """Create a new user in the Users table."""
    connection = create_connection()
    cursor = connection.cursor()
    query = "INSERT INTO Users (username, password_hash, role) VALUES (%s, %s, %s)"
    cursor.execute(query, (username, password_hash, role))
    connection.commit()
    cursor.close()
    connection.close()
    print("User created successfully")

def get_users():
    """Retrieve all users from the Users table."""
    connection = create_connection()
    cursor = connection.cursor(dictionary=True)  # Ensure results are dictionaries
    query = "SELECT * FROM Users"
    cursor.execute(query)
    result = cursor.fetchall()
    cursor.close()
    connection.close()
    return result

def update_user(user_id, username, password_hash, role):
    """Update user information in the Users table."""
    connection = create_connection()
    cursor = connection.cursor()
    query = "UPDATE Users SET username = %s, password_hash = %s, role = %s WHERE user_id = %s"
    cursor.execute(query, (username, password_hash, role, user_id))
    connection.commit()
    cursor.close()
    connection.close()
    print("User updated successfully")

def delete_user(user_id):
    """Delete a user from the Users table."""
    connection = create_connection()
    cursor = connection.cursor()
    query = "DELETE FROM Users WHERE user_id = %s"
    cursor.execute(query, (user_id,))
    connection.commit()
    cursor.close()
    connection.close()
    print("User deleted successfully")

def get_user_by_id(user_id):
    """Retrieve a single user from the Users table by user_id."""
    connection = create_connection()
    cursor = connection.cursor(dictionary=True)
    query = "SELECT * FROM Users WHERE user_id = %s"
    cursor.execute(query, (user_id,))
    user = cursor.fetchone()
    cursor.close()
    connection.close()
    return user
    

    
    

# Example usage (for testing)
if __name__ == "__main__":
    # Test the functions
    print("Testing create_user:")
    create_user('testuser', 'hashedpassword', 'staff')
    
    print("\nTesting get_users:")
    users = get_users()
    print(users)
    
    print("\nTesting update_user:")
    update_user(1, 'updateduser', 'newhashedpassword', 'admin')
    
    print("\nTesting delete_user:")
    delete_user(1)