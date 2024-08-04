# cd Project_Hotel
# cd src_codes
# python3 database.py

import mysql.connector
from mysql.connector import Error

def create_connection():
    """ Create a database connection to the MySQL database """
    connection = None
    try:
        connection = mysql.connector.connect(
            host='127.0.0.1',        # Update with your MySQL host
            user='newuser',    # Update with your MySQL username
            password='password',  # Update with your MySQL password
            database='starlight_hotel_db'
        )
        if connection.is_connected():
            print("Successfully connected to MySQL database")
    except Error as e:
        print(f"Error: '{e}'")
    return connection
    
if __name__ == "__main__":
    conn = create_connection()
    if conn:
        print("Connection object is valid")
        conn.close()
        print("Connection closed")
    else:
        print("Failed to create a connection")