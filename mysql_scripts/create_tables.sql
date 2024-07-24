-- sudo mysql -u root -p < ./Project_Hotel/mysql_scripts/create_tables.sql

-- mysql -u user1 -p

DROP DATABASE IF EXISTS starlight_hotel_db;
CREATE DATABASE starlight_hotel_db;

USE starlight_hotel_db;
GRANT ALL ON starlight_hotel_db.* TO 'user1'@'%';

-- Users Table:
CREATE TABLE Users (
  user_id INT AUTO_INCREMENT PRIMARY KEY,
  username VARCHAR(50) NOT NULL UNIQUE,
  password_hash VARCHAR(255) NOT NULL,
  role ENUM('Admin', 'Manager', 'Staff', 'Customer') NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Rooms Table:
CREATE TABLE Rooms (
  room_id INT AUTO_INCREMENT PRIMARY KEY,
  room_type VARCHAR(50) NOT NULL,
  status ENUM('Available', 'Occupied', 'Under Maintenance') NOT NULL,
  price DECIMAL(10, 2) NOT NULL
);

-- Bookings Table:
CREATE TABLE Bookings (
  booking_id INT AUTO_INCREMENT PRIMARY KEY,
  user_id INT,
  room_id INT,
  check_in DATE,
  check_out DATE,
  status ENUM('Pending', 'Approved', 'Rejected') NOT NULL,
  FOREIGN KEY (user_id) REFERENCES Users(user_id),
  FOREIGN KEY (room_id) REFERENCES Rooms(room_id)
);

-- Services Table:
CREATE TABLE Services (
  service_id INT AUTO_INCREMENT PRIMARY KEY,
  service_name VARCHAR(100) NOT NULL,
  description TEXT,
  fee DECIMAL(10, 2) NOT NULL
);

-- Fees Table:
CREATE TABLE Fees (
  fee_id INT AUTO_INCREMENT PRIMARY KEY,
  fee_type VARCHAR(50) NOT NULL,
  amount DECIMAL(10, 2) NOT NULL
);

-- INSERT INTO Users (username, password, role) VALUES ('admin', 'adminpass', 'Admin');
-- INSERT INTO Rooms (room_type, status) VALUES ('Deluxe', 'Available');
-- INSERT INTO Services (service_name, fee) VALUES ('Room Service', 20.00);
-- INSERT INTO Fees (room_type, fee) VALUES ('Deluxe', 100.00);