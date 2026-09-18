
-- Visitor Management System (VMS) - Schema & Seed Data
-- Database: remunerx_payroll

CREATE DATABASE IF NOT EXISTS remunerx_payroll;
USE remunerx_payroll;

DROP TABLE IF EXISTS APPROVALS;
DROP TABLE IF EXISTS NOTIFICATIONS;
DROP TABLE IF EXISTS INVITATIONS;
DROP TABLE IF EXISTS VISITS;
DROP TABLE IF EXISTS VISITORS;
DROP TABLE IF EXISTS EMPLOYEE;
DROP TABLE IF EXISTS USERS;
DROP TABLE IF EXISTS TENANT;

-- 0. Tenant

CREATE TABLE TENANT
	(
	tenantid            INT NOT NULL auto_increment,
	tenantname          VARCHAR (200) NOT NULL,
	LEAVESPERMONTH      INT DEFAULT NULL,
	pfpercentage        FLOAT DEFAULT NULL,
	esipercentage       FLOAT DEFAULT 0,
	basicpercentage     FLOAT DEFAULT 0,
	ishra               INT DEFAULT 0,
	hrapercentage       FLOAT DEFAULT 0,
	isconveyance        INT DEFAULT 0,
	conveyanceallowance FLOAT DEFAULT 0,
	ismedical           INT DEFAULT 0,
	medicalallowance    FLOAT DEFAULT 0,
	islta               INT DEFAULT 0,
	ltaallowance        FLOAT DEFAULT 0,
	isspecial           INT DEFAULT 1,
	specialallowance    FLOAT DEFAULT 0,
	pflimit             FLOAT DEFAULT 0,
	isprofessionaltax   INT DEFAULT 0,
	professionaltax     FLOAT DEFAULT 0,
	PRIMARY KEY (tenantid),
	UNIQUE KEY tenantname (tenantname)
	);

-- 1. Employees Table

CREATE TABLE EMPLOYEE
(
	msid                 INT NOT NULL auto_increment,
	empid                VARCHAR (300) NOT NULL,
	tenantid             INT NOT NULL,
	empname              VARCHAR (300) NOT NULL,
	phoneno              VARCHAR (100) DEFAULT NULL,
	email                VARCHAR (100) DEFAULT NULL,
	designation          VARCHAR (100) DEFAULT NULL,
	department           VARCHAR (100) DEFAULT NULL,
	emptype              VARCHAR (100) DEFAULT NULL,
	empstatus            VARCHAR (100) DEFAULT NULL,
	doj                  DATE DEFAULT NULL,
	dot                  DATE DEFAULT NULL,
	loanbalance          INT DEFAULT 0,
	leavebalance         FLOAT DEFAULT 0,
	address1             VARCHAR (5000) DEFAULT NULL,
	medicalinsurance     VARCHAR (100) DEFAULT NULL,
	createdt             DATETIME DEFAULT current_timestamp(),
	tenure               VARCHAR (300) DEFAULT NULL,
	paycycle             VARCHAR (300) DEFAULT NULL,
	bonus                FLOAT DEFAULT 0,
	loandeduction        FLOAT DEFAULT 0,
	leavestaken          FLOAT DEFAULT 0,
	leavesearned         FLOAT DEFAULT 0,
	netpay               FLOAT DEFAULT 0,
	remuneration         FLOAT DEFAULT 0,
	loanbalancebkp       INT DEFAULT 0,
	leavebalancebkp      FLOAT DEFAULT 0,
	locationname         VARCHAR (100) DEFAULT NULL,
	empphoto             TEXT DEFAULT NULL,
	leavestakenbkp       FLOAT DEFAULT NULL,
	pfeligible           VARCHAR (100) DEFAULT 'No',
	employeenameperbank  VARCHAR (100) DEFAULT NULL,
	bankname             VARCHAR (100) DEFAULT 'CASH',
	accountnumber        VARCHAR (100) DEFAULT 'NA',
	ifsccode             VARCHAR (100) DEFAULT 'NA',
	attendanceincentive  FLOAT DEFAULT 0,
	performanceincentive FLOAT DEFAULT 0,
	foodallowance        FLOAT DEFAULT 0,
	houserentallowance   FLOAT DEFAULT 0,
	fooddeduction        FLOAT DEFAULT 0,
	otherdeduction       FLOAT DEFAULT 0,
	pfnumber             VARCHAR (200) DEFAULT NULL,
	agencyname           VARCHAR (200) DEFAULT NULL,
	agencycontactnumber  VARCHAR (200) DEFAULT NULL,
	agencyaddress        VARCHAR (500) DEFAULT NULL,
	siblingrelative      VARCHAR (200) DEFAULT NULL,
	collectionbalance    INT DEFAULT 0,
	esieligible          VARCHAR (100) DEFAULT 'No',
	shift                VARCHAR (300) DEFAULT NULL,
	remotepunch          VARCHAR (10) DEFAULT NULL,
	manager              VARCHAR (300) DEFAULT NULL,
	probationperiod      VARCHAR (2) DEFAULT NULL,
	selfservice          VARCHAR (3) DEFAULT NULL,
	requestapprover      VARCHAR (3) DEFAULT '0',
	positive_conduct     LONGTEXT DEFAULT NULL,
	negative_conduct     LONGTEXT DEFAULT NULL,
	DEPT_NAME            VARCHAR (300) DEFAULT NULL,
	transportation       VARCHAR (300) DEFAULT NULL,
	skilllevel           VARCHAR (300) DEFAULT NULL,
	password             VARCHAR (200) DEFAULT NULL,
	password_hash        VARCHAR (200) DEFAULT NULL,
	PRIMARY KEY (msid),
	UNIQUE KEY empid (empid, tenantid),
	KEY idx_employee_tenant (tenantid, empid),
	KEY idx_employee_active (tenantid, empid, empstatus)
);

-- 2. Users Table (Authentication)
CREATE TABLE USERS
	(
	userid                 INT NOT NULL auto_increment,
	tenantid               INT NOT NULL,
	firstname              VARCHAR (200) NOT NULL,
	lastname               VARCHAR (200) NOT NULL,
	email                  VARCHAR (200) NOT NULL,
	password               VARCHAR (200) NOT NULL,
	verified               VARCHAR (10) DEFAULT '0',
	isadmin                INT DEFAULT 0,
	createdt               DATETIME DEFAULT current_timestamp(),
	ispayroll              INT DEFAULT 1,
	isinventory            INT DEFAULT 0,
	isassignment           INT DEFAULT 0,
	issales                INT DEFAULT 0,
	isrealtimeattendance   INT DEFAULT 0,
	iscombinedimport       INT DEFAULT 0,
	ismobileenroll         INT DEFAULT 0,
	ismanualattendance     INT DEFAULT 0,
	isdashboard            INT DEFAULT 0,
	isemployee             INT DEFAULT 0,
	isapproval             INT DEFAULT 0,
	isattendancemobileview INT DEFAULT NULL,
	istextile              INT DEFAULT 0,
	password_hash          VARCHAR (255) DEFAULT NULL,
	PRIMARY KEY (userid)
);

-- 3. Datamapping
DROP TABLE IF EXISTS DATAMAPPING;
CREATE TABLE DATAMAPPING
(
    datamappingid INT NOT NULL AUTO_INCREMENT,
    tenantid      INT NOT NULL,
    `grouping`    VARCHAR(200) NOT NULL,
    description   VARCHAR(200) NOT NULL,
    internalcode  VARCHAR(200) NOT NULL,
    externalcode  VARCHAR(200) NOT NULL,
    fieldvalue    VARCHAR(200) DEFAULT NULL,

    PRIMARY KEY (datamappingid),

    UNIQUE KEY datamappingunique
    (
        tenantid,
        `grouping`,
        description,
        internalcode,
        externalcode
    ),

    KEY idx_datamapping_skill
    (
        tenantid,
        `grouping`,
        description,
        internalcode
    )
);

-- 4. Visitors Table
CREATE TABLE VISITORS (
    visitor_id INT AUTO_INCREMENT PRIMARY KEY,
    tenantid  INT NOT NULL,
    name VARCHAR(100) NOT NULL,
    phone VARCHAR(20) NOT NULL,
    email VARCHAR(100),
    company VARCHAR(100),
    photo_url VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 5. Visits Table (Central Entity)

CREATE TABLE VISITS (
    visit_id INT AUTO_INCREMENT PRIMARY KEY,
    tenantid INT NOT NULL,
    visitor_id INT NOT NULL,
    empid VARCHAR (300) NOT NULL,
    locations VARCHAR (300) NOT NULL,
    meetingroom VARCHAR (300) NOT NULL,
    purpose VARCHAR(255) NOT NULL,
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
    start_time TIME NOT NULL,
    end_time TIME NOT NULL,
    status VARCHAR(50) DEFAULT 'CREATED',
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    KEY idx_visits_employee (empid, tenantid),
    FOREIGN KEY (visitor_id) REFERENCES VISITORS(visitor_id) ON DELETE CASCADE
);

-- 6. Invitations Table

CREATE TABLE INVITATIONS (
    invitation_id INT AUTO_INCREMENT PRIMARY KEY,
    visit_id INT NOT NULL,
    qr_code VARCHAR(64) UNIQUE NOT NULL,
    sent_at DATETIME NULL,
    expires_at DATETIME NOT NULL,
    status VARCHAR(50) DEFAULT 'GENERATED',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (visit_id) REFERENCES visits(visit_id) ON DELETE CASCADE
);

-- 7. Notifications Table

CREATE TABLE NOTIFICATIONS (
    notification_id INT AUTO_INCREMENT PRIMARY KEY,
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
CREATE TABLE APPROVALS (
    approval_id INT AUTO_INCREMENT PRIMARY KEY,
    visit_id INT NOT NULL,
    approver_id INT NULL,
    status VARCHAR(50) DEFAULT 'PENDING',
    comments TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    decided_at DATETIME NULL,
    FOREIGN KEY (visit_id) REFERENCES visits(visit_id) ON DELETE CASCADE
);

-- 9. Visit Events Table (Check-in / Check-out log)
CREATE TABLE VISIT_EVENTS (
    visit_event_id INT AUTO_INCREMENT PRIMARY KEY,
    visit_id INT NOT NULL,
    event_type VARCHAR(20) NOT NULL,
    event_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    recorded_by VARCHAR(300) NULL,
    FOREIGN KEY (visit_id) REFERENCES visits(visit_id) ON DELETE CASCADE
);

-- 10. Badges Table
CREATE TABLE BADGES (
    badge_id INT AUTO_INCREMENT PRIMARY KEY,
    visit_id INT NOT NULL,
    badge_code VARCHAR(32) UNIQUE NOT NULL,
    status VARCHAR(50) DEFAULT 'ISSUED',
    issued_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (visit_id) REFERENCES visits(visit_id) ON DELETE CASCADE
);



-- ===================================================
-- SEED DATA
-- ===================================================

-- Sample Tenant
INSERT INTO TENANT (tenantid, tenantname, LEAVESPERMONTH, pfpercentage, esipercentage, basicpercentage, ishra, hrapercentage, isconveyance, conveyanceallowance, ismedical, medicalallowance, islta, ltaallowance, isspecial, specialallowance, pflimit, isprofessionaltax, professionaltax)
VALUES (1, 'FacePoint Demo', NULL, NULL, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0);

-- Sample Users (Default password for sample accounts: password123)
-- Password Hash for 'password123' using bcrypt: $2b$12$EqMpNlbs3AMD3DvWD53Zo.cOZ/2vHRIGYqY8wyL3a029aJur/1bRq
INSERT INTO USERS (tenantid, firstname, lastname, email, password, verified, isadmin, createdt, ispayroll, isinventory, isassignment, issales, isrealtimeattendance, iscombinedimport, ismobileenroll, ismanualattendance, isdashboard, isemployee, isapproval, isattendancemobileview, istextile, password_hash)
VALUES (1, 'Facepoint', 'Demo', 'admin@fpd.com', 'fpd123', '1', 0, '2024-10-16 17:24:33', 1, 0, 0, 0, 1, 1, 0, 0, 1, 1, 1, NULL, 0, '$2b$12$EqMpNlbs3AMD3DvWD53Zo.cOZ/2vHRIGYqY8wyL3a029aJur/1bRq');

-- Sample Employees
INSERT INTO EMPLOYEE (empid, tenantid, empname, phoneno, email, designation, department, emptype, empstatus, doj, dot, loanbalance, leavebalance, address1, medicalinsurance, createdt, tenure, paycycle, bonus, loandeduction, leavestaken, leavesearned, netpay, remuneration, loanbalancebkp, leavebalancebkp, locationname, empphoto, leavestakenbkp, pfeligible, employeenameperbank, bankname, accountnumber, ifsccode, attendanceincentive, performanceincentive, foodallowance, houserentallowance, fooddeduction, otherdeduction, pfnumber, agencyname, agencycontactnumber, agencyaddress, siblingrelative, collectionbalance, esieligible, shift, remotepunch, manager, probationperiod, selfservice, requestapprover, positive_conduct, negative_conduct, DEPT_NAME, transportation, skilllevel, password, password_hash)
VALUES ('FPD0001', 1, 'Magesh Sankaran', '09886066110', 'magesh.sankaran@gmail.com', '', 'Engineering', 'Board Of Directors', 'Active', '2026-07-01', NULL, 0, 0, '', NULL, '2026-07-27 23:33:55', 'Monthly', 'Monthly', 0, 0, 0, 0, 0, 50000, 0, 0, 'Coimbatore', '', 0, 'No', '', 'CASH', 'NA', 'NA', 0, 0, 0, 0, 0, 0, '', '', '', '', '', 0, 'No', 'Staff', '0', '', '', '1', '1', '[]', '[]', NULL, '', 'Skilled', 'magakavi', NULL);
INSERT INTO EMPLOYEE (empid, tenantid, empname, phoneno, email, designation, department, emptype, empstatus, doj, dot, loanbalance, leavebalance, address1, medicalinsurance, createdt, tenure, paycycle, bonus, loandeduction, leavestaken, leavesearned, netpay, remuneration, loanbalancebkp, leavebalancebkp, locationname, empphoto, leavestakenbkp, pfeligible, employeenameperbank, bankname, accountnumber, ifsccode, attendanceincentive, performanceincentive, foodallowance, houserentallowance, fooddeduction, otherdeduction, pfnumber, agencyname, agencycontactnumber, agencyaddress, siblingrelative, collectionbalance, esieligible, shift, remotepunch, manager, probationperiod, selfservice, requestapprover, positive_conduct, negative_conduct, DEPT_NAME, transportation, skilllevel, password, password_hash)
VALUES ('FPD0002', 1, 'Shanmathi', '5104565652', 'srishanmathianbalagan@gmail.com', NULL, 'Sales', 'Employee', 'Active', '2026-08-07', NULL, 0, 0, NULL, NULL, '2026-07-27 23:40:33', 'Monthly', 'Monthly', 0, 0, 0, 0, 0, 40000, 0, 0, 'Coimbatore', '', 0, 'No', NULL, 'CASH', 'NA', 'NA', 0, 0, 0, 0, 0, 0, NULL, NULL, NULL, NULL, NULL, 0, 'No', 'Staff', '0', 'FPD0001', NULL, '1', '1', NULL, NULL, NULL, NULL, 'Skilled', NULL, NULL);

-- Sample Datamapping
INSERT INTO DATAMAPPING (tenantid, `grouping`, description, internalcode, externalcode, fieldvalue)
VALUES (1, 'LOCATION', 'LOCATION', 'Coimbatore', 'Coimbatore', 'Dropdown Value');
INSERT INTO DATAMAPPING (tenantid, `grouping`, description, internalcode, externalcode, fieldvalue)
VALUES (1, 'LOCATION', 'LOCATION', 'Bangalore', 'Bangalore', 'Dropdown Value');
INSERT INTO DATAMAPPING (tenantid, `grouping`, description, internalcode, externalcode, fieldvalue)
VALUES (1, 'MEETING ROOM', 'MEETING ROOM', 'CONF ROOM 1', 'CONF ROOM 1', 'Dropdown Value');
INSERT INTO DATAMAPPING (tenantid, `grouping`, description, internalcode, externalcode, fieldvalue)
VALUES (1, 'MEETING ROOM', 'MEETING ROOM', 'CONF ROOM 2', 'CONF ROOM 2', 'Dropdown Value');

INSERT INTO VISITORS(visitor_id, tenantid, name, phone, email, company)
VALUES
    (101, 1, 'Rahul Kumar', '+91 9123456789', 'rahul.k@abcltd.com', 'ABC Ltd'),
    (102, 1, 'Priya Mehta', '+91 9234567890', 'priya.m@techcorp.com', 'Tech Corp'),
    (103, 1, 'Suresh Verma', '+91 9345678901', 'suresh@vendorpro.in', 'VendorPro');

