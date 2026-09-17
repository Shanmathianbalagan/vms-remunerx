-- Visitor Management System (VMS) - Schema & Seed Data
-- Database: vms_db

CREATE DATABASE IF NOT EXISTS vms_db;
USE vms_db;

-- 1. Employees Table
CREATE TABLE IF NOT EXISTS employees (
    employee_id INT AUTO_INCREMENT PRIMARY KEY,
    tenant_id INT NOT NULL DEFAULT 1,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    department VARCHAR(100) DEFAULT 'General',
    designation VARCHAR(100) DEFAULT 'Staff',
    phone VARCHAR(20),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 2. Users Table (Authentication)
CREATE TABLE IF NOT EXISTS users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    tenant_id INT NOT NULL DEFAULT 1,
    email VARCHAR(100) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    role VARCHAR(50) DEFAULT 'EMPLOYEE',
    employee_id INT UNIQUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (employee_id) REFERENCES employees(employee_id) ON DELETE SET NULL
);

-- 3. Locations Table
CREATE TABLE IF NOT EXISTS locations (
    location_id INT AUTO_INCREMENT PRIMARY KEY,
    tenant_id INT NOT NULL DEFAULT 1,
    name VARCHAR(100) NOT NULL,
    address VARCHAR(255) DEFAULT 'Headquarters',
    city VARCHAR(100) DEFAULT 'Bangalore',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 4a. Meeting Rooms Table
CREATE TABLE IF NOT EXISTS meeting_rooms (
    meeting_room_id INT AUTO_INCREMENT PRIMARY KEY,
    tenant_id INT NOT NULL DEFAULT 1,
    name VARCHAR(100) NOT NULL,
    capacity INT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 4. Visitors Table
CREATE TABLE IF NOT EXISTS visitors (
    visitor_id INT AUTO_INCREMENT PRIMARY KEY,
    tenant_id INT NOT NULL DEFAULT 1,
    name VARCHAR(100) NOT NULL,
    phone VARCHAR(20) NOT NULL,
    email VARCHAR(100),
    company VARCHAR(100),
    photo_url VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 5. Visits Table (Central Entity)
CREATE TABLE IF NOT EXISTS visits (
    visit_id INT AUTO_INCREMENT PRIMARY KEY,
    tenant_id INT NOT NULL DEFAULT 1,
    visitor_id INT NOT NULL,
    employee_id INT NOT NULL,
    location_id INT NOT NULL,
    meeting_room_id INT NULL,
    purpose VARCHAR(255) NOT NULL,
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
    start_time TIME NOT NULL,
    end_time TIME NOT NULL,
    status VARCHAR(50) DEFAULT 'CREATED',
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (visitor_id) REFERENCES visitors(visitor_id) ON DELETE CASCADE,
    FOREIGN KEY (employee_id) REFERENCES employees(employee_id) ON DELETE CASCADE,
    FOREIGN KEY (location_id) REFERENCES locations(location_id) ON DELETE CASCADE,
    FOREIGN KEY (meeting_room_id) REFERENCES meeting_rooms(meeting_room_id) ON DELETE SET NULL
);

-- 6. Invitations Table
CREATE TABLE IF NOT EXISTS invitations (
    invitation_id INT AUTO_INCREMENT PRIMARY KEY,
    tenant_id INT NOT NULL DEFAULT 1,
    visit_id INT NOT NULL,
    qr_code VARCHAR(64) UNIQUE NOT NULL,
    sent_at DATETIME NULL,
    expires_at DATETIME NOT NULL,
    status VARCHAR(50) DEFAULT 'GENERATED',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (visit_id) REFERENCES visits(visit_id) ON DELETE CASCADE
);

-- 7. Notifications Table
CREATE TABLE IF NOT EXISTS notifications (
    notification_id INT AUTO_INCREMENT PRIMARY KEY,
    tenant_id INT NOT NULL DEFAULT 1,
    visit_id INT NOT NULL,
    type VARCHAR(50) NOT NULL,
    channel VARCHAR(20) DEFAULT 'EMAIL',
    recipient VARCHAR(100),
    status VARCHAR(50) DEFAULT 'PENDING',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    sent_at DATETIME NULL,
    FOREIGN KEY (visit_id) REFERENCES visits(visit_id) ON DELETE CASCADE
);

-- 8. Approvals Table
CREATE TABLE IF NOT EXISTS approvals (
    approval_id INT AUTO_INCREMENT PRIMARY KEY,
    tenant_id INT NOT NULL DEFAULT 1,
    visit_id INT NOT NULL,
    approver_id INT NULL,
    status VARCHAR(50) DEFAULT 'PENDING',
    comments TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    decided_at DATETIME NULL,
    FOREIGN KEY (visit_id) REFERENCES visits(visit_id) ON DELETE CASCADE,
    FOREIGN KEY (approver_id) REFERENCES employees(employee_id) ON DELETE SET NULL
);

-- 9. Visit Events Table
CREATE TABLE IF NOT EXISTS visit_events (
    visit_event_id INT AUTO_INCREMENT PRIMARY KEY,
    tenant_id INT NOT NULL DEFAULT 1,
    visit_id INT NOT NULL,
    event_type VARCHAR(20) NOT NULL,
    event_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    recorded_by INT NULL,
    FOREIGN KEY (visit_id) REFERENCES visits(visit_id) ON DELETE CASCADE,
    FOREIGN KEY (recorded_by) REFERENCES employees(employee_id) ON DELETE SET NULL
);

-- 10. Badges Table
CREATE TABLE IF NOT EXISTS badges (
    badge_id INT AUTO_INCREMENT PRIMARY KEY,
    tenant_id INT NOT NULL DEFAULT 1,
    visit_id INT NOT NULL,
    badge_code VARCHAR(32) UNIQUE NOT NULL,
    status VARCHAR(50) DEFAULT 'ISSUED',
    issued_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (visit_id) REFERENCES visits(visit_id) ON DELETE CASCADE
);

-- ===================================================
-- SEED DATA
-- ===================================================

-- Sample Employees
INSERT INTO employees (employee_id, name, email, department, designation, phone) VALUES
(1, 'Rahul Sharma', 'rahul.sharma@remunerx.com', 'Human Resources', 'HR Manager', '+91 9876543210'),
(2, 'Ananya Roy', 'ananya.roy@remunerx.com', 'Engineering', 'Tech Lead', '+91 9876543211'),
(3, 'Vikram Patel', 'vikram.patel@remunerx.com', 'Finance', 'Accountant', '+91 9876543212')
ON DUPLICATE KEY UPDATE name=VALUES(name);

-- Sample Users (Default password for sample accounts: password123)
-- Password Hash for 'password123' using bcrypt: $2b$12$EqMpNlbs3AMD3DvWD53Zo.cOZ/2vHRIGYqY8wyL3a029aJur/1bRq
INSERT INTO users (user_id, email, password_hash, role, employee_id) VALUES
(1, 'rahul.sharma@remunerx.com', '$2b$12$EqMpNlbs3AMD3DvWD53Zo.cOZ/2vHRIGYqY8wyL3a029aJur/1bRq', 'EMPLOYEE', 1),
(2, 'ananya.roy@remunerx.com', '$2b$12$EqMpNlbs3AMD3DvWD53Zo.cOZ/2vHRIGYqY8wyL3a029aJur/1bRq', 'EMPLOYEE', 2),
(3, 'admin@remunerx.com', '$2b$12$EqMpNlbs3AMD3DvWD53Zo.cOZ/2vHRIGYqY8wyL3a029aJur/1bRq', 'ADMIN', 3)
ON DUPLICATE KEY UPDATE email=VALUES(email);

-- Sample Locations
INSERT INTO locations (location_id, name, address, city) VALUES
(1, 'Conference Room A (2nd Floor)', 'Building 4, Tech Park', 'Bangalore'),
(2, 'Boardroom 1 (5th Floor)', 'Building 4, Tech Park', 'Bangalore'),
(3, 'Main Reception Area', 'Ground Floor, Building 4', 'Bangalore'),
(4, 'Executive Suite', '6th Floor, Building 4', 'Bangalore')
ON DUPLICATE KEY UPDATE name=VALUES(name);

-- Sample Meeting Rooms
INSERT INTO meeting_rooms (meeting_room_id, name, capacity) VALUES
(1, 'Meeting Room 1', 6),
(2, 'Meeting Room 2', 10)
ON DUPLICATE KEY UPDATE name=VALUES(name);

-- Sample Visitors
INSERT INTO visitors (visitor_id, name, phone, email, company) VALUES
(101, 'Rahul Kumar', '+91 9123456789', 'rahul.k@abcltd.com', 'ABC Ltd'),
(102, 'Priya Mehta', '+91 9234567890', 'priya.m@techcorp.com', 'Tech Corp'),
(103, 'Suresh Verma', '+91 9345678901', 'suresh@vendorpro.in', 'VendorPro')
ON DUPLICATE KEY UPDATE name=VALUES(name);

-- Sample Visits
INSERT INTO visits (visit_id, visitor_id, employee_id, location_id, purpose, start_date, end_date, start_time, end_time, status, notes) VALUES
(1, 101, 1, 1, 'Client Meeting', '2026-09-15', '2026-09-15', '10:00:00', '11:30:00', 'APPROVED', 'Discussion regarding quarterly payroll audit.'),
(2, 102, 1, 2, 'Project Discussion', '2026-09-16', '2026-09-16', '14:00:00', '15:00:00', 'CREATED', 'Reviewing UI designs for VMS.'),
(3, 103, 2, 3, 'Vendor Inspection', '2026-09-17', '2026-09-17', '11:00:00', '12:00:00', 'PENDING_APPROVAL', 'Hardware maintenance check.')
ON DUPLICATE KEY UPDATE purpose=VALUES(purpose);
