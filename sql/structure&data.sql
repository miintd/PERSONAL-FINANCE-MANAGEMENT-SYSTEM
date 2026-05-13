CREATE DATABASE IF NOT EXISTS personal_finance;
USE personal_finance;

CREATE TABLE USERS (
  UserID      INT          NOT NULL AUTO_INCREMENT,
  UserName    VARCHAR(100) NOT NULL,
  Email       VARCHAR(100) NOT NULL UNIQUE,
  PhoneNumber VARCHAR(20),
  Password    VARCHAR(100) NOT NULL DEFAULT '123456',
  PRIMARY KEY (UserID)
);

CREATE TABLE BANKACCOUNTS (
  AccountID INT           NOT NULL AUTO_INCREMENT,
  UserID    INT           NOT NULL,
  BankName  VARCHAR(100)  NOT NULL,
  Balance   DECIMAL(15,2) NOT NULL DEFAULT 0,
  PRIMARY KEY (AccountID),
  FOREIGN KEY (UserID) REFERENCES USERS(UserID) ON DELETE CASCADE
);

CREATE TABLE INCOME (
  IncomeID    INT          NOT NULL AUTO_INCREMENT,
  UserID      INT          NOT NULL,
  Amount      DECIMAL(15,2) NOT NULL CHECK (Amount > 0),
  IncomeDate  DATE         NOT NULL,
  AccountID   INT 		   NOT NULL,
  Description VARCHAR(255),
  PRIMARY KEY (IncomeID),
  FOREIGN KEY (UserID) REFERENCES USERS(UserID) ON DELETE CASCADE,
  FOREIGN KEY (AccountID) REFERENCES BANKACCOUNTS(AccountID)
);

CREATE TABLE EXPENSECATEGORIES (
  CategoryID   INT          NOT NULL AUTO_INCREMENT,
  CategoryName VARCHAR(100) NOT NULL,
  PRIMARY KEY (CategoryID)
);

CREATE TABLE EXPENSES (
  ExpenseID   INT          NOT NULL AUTO_INCREMENT,
  UserID      INT          NOT NULL,
  CategoryID  INT          NOT NULL,
  Amount      DECIMAL(15,2) NOT NULL CHECK (Amount > 0),
  ExpenseDate DATE         NOT NULL,
  AccountID   INT 		   NOT NULL,
  Description VARCHAR(255),
  PRIMARY KEY (ExpenseID),
  FOREIGN KEY (UserID)     REFERENCES USERS(UserID) ON DELETE CASCADE,
  FOREIGN KEY (CategoryID) REFERENCES EXPENSECATEGORIES(CategoryID),
  FOREIGN KEY (AccountID) REFERENCES BANKACCOUNTS(AccountID)
);


-- ===========================================================================================================
-- Xóa dữ liệu cũ nếu có
DELETE FROM BANKACCOUNTS;
DELETE FROM EXPENSES;
DELETE FROM INCOME;
DELETE FROM EXPENSECATEGORIES;
DELETE FROM USERS;

-- Reset AUTO_INCREMENT
ALTER TABLE BANKACCOUNTS AUTO_INCREMENT = 1;
ALTER TABLE EXPENSES AUTO_INCREMENT = 1;
ALTER TABLE INCOME AUTO_INCREMENT = 1;
ALTER TABLE EXPENSECATEGORIES AUTO_INCREMENT = 1;
ALTER TABLE USERS AUTO_INCREMENT = 1;

-- 1. USERS (10 records)
INSERT INTO USERS (UserName, Email, PhoneNumber) VALUES
('Nguyen Van An',    'an.nguyen@gmail.com',    '0901234567'),
('Tran Thi Bich',    'bich.tran@gmail.com',    '0912345678'),
('Le Hoang Nam',     'nam.le@gmail.com',        '0923456789'),
('Pham Thi Lan',     'lan.pham@gmail.com',      '0934567890'),
('Hoang Minh Duc',   'duc.hoang@gmail.com',    '0945678901'),
('Vu Thi Mai',       'mai.vu@gmail.com',        '0956789012'),
('Dang Van Tuan',    'tuan.dang@gmail.com',    '0967890123'),
('Bui Thi Hoa',      'hoa.bui@gmail.com',       '0978901234'),
('Do Quang Huy',     'huy.do@gmail.com',        '0989012345'),
('Nguyen Thi Linh',  'linh.nguyen@gmail.com',  '0990123456');

-- 2. EXPENSECATEGORIES (10 records)
INSERT INTO EXPENSECATEGORIES (CategoryName) VALUES
('Food & Drink'),
('Transport'),
('Education'),
('Healthcare'),
('Entertainment'),
('Shopping'),
('Utilities'),
('Housing'),
('Travel'),
('Personal Care');

-- 3. BANKACCOUNTS (10 records)
INSERT INTO BANKACCOUNTS (UserID, BankName, Balance) VALUES
( 1, 'Vietcombank',  25000000),
( 2, 'BIDV',         15000000),
( 3, 'VPBank',       40000000),
( 4, 'Agribank',      5000000),
( 5, 'MB Bank',      30000000),
( 6, 'Techcombank',  18000000),
( 7, 'Vietinbank',   50000000),
( 8, 'TPBank',        8000000),
( 9, 'ACB',          22000000),
(10, 'SHB',          11000000);

-- 4. INCOME (10 records)
INSERT INTO INCOME (UserID, AccountID, Amount, IncomeDate, Description) VALUES
(1, 1, 15000000, '2025-01-05', 'Monthly salary'),
(2, 2, 12000000, '2025-01-05', 'Monthly salary'),
(3, 3, 20000000, '2025-01-05', 'Monthly salary'),
(4, 4,  8000000, '2025-01-05', 'Part-time job'),
(5, 5, 18000000, '2025-01-05', 'Monthly salary'),
(6, 6, 10000000, '2025-01-05', 'Monthly salary'),
(7, 7, 22000000, '2025-01-05', 'Monthly salary'),
(8, 8,  9000000, '2025-01-05', 'Freelance design'),
(9, 9, 16000000, '2025-01-05', 'Monthly salary'),
(10,10,13000000, '2025-01-05', 'Monthly salary');

-- 5. EXPENSES (10 records)
INSERT INTO EXPENSES (UserID, CategoryID, AccountID, Amount, ExpenseDate, Description) VALUES
(1, 1, 1,  500000, '2025-01-06', 'Grocery shopping'),
(2, 2, 2,  200000, '2025-01-07', 'Grab bike'),
(3, 3, 3, 3000000, '2025-01-08', 'Online course fee'),
(4, 4, 4,  500000, '2025-01-09', 'Medical checkup'),
(5, 5, 5, 1200000, '2025-01-10', 'Cinema & dinner'),
(6, 6, 6, 2500000, '2025-01-11', 'Clothes shopping'),
(7, 7, 7,  800000, '2025-01-12', 'Electric bill'),
(8, 8, 8, 5000000, '2025-01-13', 'Monthly rent'),
(9, 9, 9, 7000000, '2025-01-14', 'Da Nang trip'),
(10,10,10, 350000, '2025-01-15', 'Haircut & spa');


DESCRIBE USERS;
DESCRIBE INCOME;
DESCRIBE EXPENSECATEGORIES;
DESCRIBE EXPENSES;
DESCRIBE BANKACCOUNTS;