-- sudo mysql -u root -p < ./Project_Hotel/mysql_scripts/create_tables.sql

-- mysql -u user1 -p
-- use starlight_hotel_db;

DROP DATABASE IF EXISTS starlight_hotel_db;
CREATE DATABASE starlight_hotel_db;

USE starlight_hotel_db;
GRANT ALL ON starlight_hotel_db.* TO 'newuser'@'%';

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
  room_tid INT AUTO_INCREMENT PRIMARY KEY,
  room_id VARCHAR(50) NOT NULL,
  room_type VARCHAR(50) NOT NULL,
  price DECIMAL(10, 2) NOT NULL
);

Describe Rooms;

INSERT INTO Rooms (room_id, room_type, price) VALUES
('101', 'single', 100),
('102', 'single', 100),
('103', 'single', 100),
('104', 'single', 100),
('201', 'double', 150),
('202', 'double', 150), 
('203', 'double', 150),
('204', 'double', 150),
('301', 'suite',  250),
('302', 'suite',  250), 
('303', 'suite',  250),
('304', 'suite',  250); 
select *  from  Rooms;


-- Bookings Table:
CREATE TABLE Bookings (
  booking_id INT AUTO_INCREMENT PRIMARY KEY,
  user_id INT,
  room_id INT,
  check_in DATE,
  check_out DATE,
  status ENUM('Pending', 'Approved', 'Rejected', 'ReadytoBill') NOT NULL,
  FOREIGN KEY (user_id) REFERENCES Users(user_id),
  FOREIGN KEY (room_id) REFERENCES Rooms(room_tid)
);

-- Services Table:
CREATE TABLE Services (
  service_id INT AUTO_INCREMENT PRIMARY KEY,
  service_name VARCHAR(100) NOT NULL,
  description TEXT,
  fee DECIMAL(10, 2) NOT NULL
);

INSERT INTO Services (service_name, description, fee)VALUES
('Room Service', 'Breakfast', 4.99),
('Room Service', 'Lunch',   17.5),
('Room Service', 'Dinner', 24.5),
('Laundry', '0-5 pieces', 10),
('Laundry', '6-10 pieces', 15),
('Laundry', '11-20 pieces', 30),
('Laundry', 'more 20 pieces', 100),
('Maintenace', 'Urgent', 0),
('Maintenace', 'Next Day', 0),
('Room Cleaning', 'Urgent', 10),
('Room Cleaning', 'Next Day', 0),
('Wake-up Call', 'Tonight', 0)
;


-- Fees Table:
CREATE TABLE Fees (
  fee_id INT AUTO_INCREMENT PRIMARY KEY,
  fee_type VARCHAR(50) NOT NULL,
  amount DECIMAL(10, 2) NOT NULL
);


INSERT INTO Fees (fee_type, amount) VALUES
('single', 100),
('double', 150),
('suite',  250); 
--select *  from  Rooms;

-- INSERT INTO Users (username, password, role) VALUES ('admin', 'adminpass', 'Admin');
-- INSERT INTO Rooms (room_type, status) VALUES ('Deluxe', 'Available');
-- INSERT INTO Services (service_name, fee) VALUES ('Room Service', 20.00);
-- INSERT INTO Fees (room_type, fee) VALUES ('Deluxe', 100.00);

