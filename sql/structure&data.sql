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

-- ============================================================
DELETE FROM expenses WHERE UserID >= 11;
DELETE FROM income WHERE UserID >= 11;
DELETE FROM USERS WHERE UserID >= 11;
--  USER 11 — Nguyen Minh Khoa  (lương cao, nhiều accounts)
--  Password: 123456
-- ──────────────────────────────────────────────────────────
INSERT INTO USERS (UserName, Email, PhoneNumber, Password) VALUES
('Nguyen Minh Khoa', 'khoa.nguyen@gmail.com', '0911222333', '123456');
-- Giả sử UserID = 11

-- 4 bank accounts
INSERT INTO BANKACCOUNTS (UserID, BankName, Balance) VALUES
(11, 'Vietcombank',  45000000),   -- AccountID = 11 (tài khoản lương chính)
(11, 'Techcombank',  20000000),   -- AccountID = 12 (tiết kiệm)
(11, 'MB Bank',       8000000),   -- AccountID = 13 (chi tiêu hằng ngày)
(11, 'VPBank',       15000000);   -- AccountID = 14 (đầu tư / dự phòng)

-- ── INCOME User 11 (12/2024 – 5/2026, mỗi tháng 1-2 khoản) ──
-- 2025-10
INSERT INTO INCOME (UserID, AccountID, Amount, IncomeDate, Description) VALUES
(11, 11, 28000000, '2025-10-05', 'Monthly salary');
-- 2025-11
INSERT INTO INCOME (UserID, AccountID, Amount, IncomeDate, Description) VALUES
(11, 11, 28000000, '2025-11-05', 'Monthly salary'),
(11, 13,  4000000, '2025-11-12', 'Part-time consulting');
-- 2025-12
INSERT INTO INCOME (UserID, AccountID, Amount, IncomeDate, Description) VALUES
(11, 11, 28000000, '2025-12-05', 'Monthly salary'),
(11, 12,  8000000, '2025-12-20', 'Year-end bonus');
-- 2026-01
INSERT INTO INCOME (UserID, AccountID, Amount, IncomeDate, Description) VALUES
(11, 11, 30000000, '2026-01-05', 'Monthly salary (raise)'),
(11, 13,  2000000, '2026-01-20', 'Tutoring income');
-- 2026-02
INSERT INTO INCOME (UserID, AccountID, Amount, IncomeDate, Description) VALUES
(11, 11, 30000000, '2026-02-05', 'Monthly salary');
-- 2026-03
INSERT INTO INCOME (UserID, AccountID, Amount, IncomeDate, Description) VALUES
(11, 11, 30000000, '2026-03-05', 'Monthly salary'),
(11, 14,  5000000, '2026-03-18', 'Investment return');
-- 2026-04
INSERT INTO INCOME (UserID, AccountID, Amount, IncomeDate, Description) VALUES
(11, 11, 30000000, '2026-04-05', 'Monthly salary');
-- 2026-05 (tháng hiện tại)
INSERT INTO INCOME (UserID, AccountID, Amount, IncomeDate, Description) VALUES
(11, 11, 30000000, '2026-05-05', 'Monthly salary'),
(11, 13,  3500000, '2026-05-08', 'Freelance project'),
(11, 12,  2000000, '2026-05-10', 'Stock dividend');

-- ── EXPENSES User 11 ──
-- 2025-10
INSERT INTO EXPENSES (UserID, CategoryID, AccountID, Amount, ExpenseDate, Description) VALUES
(11,  1, 13,  2050000, '2025-10-02', 'Grocery & dining'),
(11,  8, 11, 8000000, '2025-10-06', 'Monthly rent'),
(11,  7, 11, 1250000, '2025-10-10', 'Electric & water bill'),
(11,  5, 12, 1500000, '2025-10-18', 'Halloween party'),
(11,  2, 13,  600000, '2025-10-24', 'Grab / taxi');
-- 2025-11
INSERT INTO EXPENSES (UserID, CategoryID, AccountID, Amount, ExpenseDate, Description) VALUES
(11,  1, 13,  2150000, '2025-11-03', 'Grocery & dining'),
(11,  8, 11, 8000000, '2025-11-06', 'Monthly rent'),
(11,  4, 13,  900000, '2025-11-12', 'Eye checkup & glasses'),
(11,  6, 13, 3000000, '2025-11-11', '11.11 sale shopping'),
(11,  2, 13,  750000, '2025-11-22', 'Grab / taxi');
-- 2025-12
INSERT INTO EXPENSES (UserID, CategoryID, AccountID, Amount, ExpenseDate, Description) VALUES
(11,  1, 13,  2500000, '2025-12-03', 'Grocery & Tet food prep'),
(11,  8, 11, 8000000, '2025-12-06', 'Monthly rent'),
(11,  9, 14, 11000000, '2025-12-20', 'Year-end trip - Japan'),
(11,  5, 13, 2000000, '2025-12-25', 'Christmas party'),
(11,  6, 12, 3500000, '2025-12-27', 'Year-end gift shopping');
-- 2026-01
INSERT INTO EXPENSES (UserID, CategoryID, AccountID, Amount, ExpenseDate, Description) VALUES
(11,  1, 11,  2200000, '2026-01-04', 'Grocery & dining'),
(11,  8, 11, 8500000, '2026-01-06', 'Monthly rent (new contract)'),
(11,  9, 14, 6000000, '2026-01-18', 'Tet holiday trip'),
(11,  6, 12, 2800000, '2026-01-22', 'Tet clothing & gifts'),
(11,  2, 13,  800000, '2026-01-28', 'Grab / taxi');
-- 2026-02
INSERT INTO EXPENSES (UserID, CategoryID, AccountID, Amount, ExpenseDate, Description) VALUES
(11,  1, 12,  1900000, '2026-02-02', 'Grocery & dining'),
(11,  8, 11, 8500000, '2026-02-06', 'Monthly rent'),
(11,  7, 11, 1350000, '2026-02-10', 'Electric & water bill'),
(11,  4, 12,  500000, '2026-02-14', 'Medical checkup'),
(11,  3, 12, 2500000, '2026-02-20', 'Online course - AI');
-- 2026-03
INSERT INTO EXPENSES (UserID, CategoryID, AccountID, Amount, ExpenseDate, Description) VALUES
(11,  1, 12,  2100000, '2026-03-03', 'Grocery & dining'),
(11,  8, 11, 8500000, '2026-03-06', 'Monthly rent'),
(11,  9, 11, 7500000, '2026-03-15', 'Trip - Hoi An'),
(11,  6, 13, 1800000, '2026-03-22', 'Spring clothes'),
(11,  5, 14, 1000000, '2026-03-28', 'Movies & dinner');
-- 2026-04
INSERT INTO EXPENSES (UserID, CategoryID, AccountID, Amount, ExpenseDate, Description) VALUES
(11,  1, 11,  2300000, '2026-04-02', 'Grocery & dining'),
(11,  8, 11, 8500000, '2026-04-06', 'Monthly rent'),
(11,  7, 11, 1400000, '2026-04-10', 'Electric & water bill'),
(11,  3, 12, 3000000, '2026-04-15', 'Semester tuition'),
(11,  2, 14,  900000, '2026-04-20', 'Grab / taxi'),
(11, 10, 13,  500000, '2026-04-26', 'Haircut & spa');
-- 2026-05 (tháng hiện tại — có giao dịch tuần này để test "1 week trend")
INSERT INTO EXPENSES (UserID, CategoryID, AccountID, Amount, ExpenseDate, Description) VALUES
(11,  1, 11,  2400000, '2026-05-02', 'Grocery & dining'),
(11,  8, 11, 8500000, '2026-05-06', 'Monthly rent'),
(11,  2, 14,   650000, '2026-05-07', 'Grab / taxi'),
(11,  5, 12,  800000, '2026-05-08', 'Cinema'),
(11,  6, 12, 1200000, '2026-05-09', 'Online shopping'),
(11,  1, 13,   450000, '2026-05-10', 'Coffee & snacks'),
(11,  4, 11,   600000, '2026-05-11', 'Pharmacy'),
(11,  7, 11, 1300000, '2026-05-12', 'Electric bill');


-- ──────────────────────────────────────────────────────────
--  USER 12 — Tran Phuong Thao  (freelancer, thu nhập biến động)
--  Password: 123456
-- ──────────────────────────────────────────────────────────
INSERT INTO USERS (UserName, Email, PhoneNumber, Password) VALUES
('Tran Phuong Thao', 'thao.tran@gmail.com', '0922333444', '123456');
-- Giả sử UserID = 12

-- 3 bank accounts
INSERT INTO BANKACCOUNTS (UserID, BankName, Balance) VALUES
(12, 'BIDV',        20000000),   -- AccountID = 15 (thu nhập chính)
(12, 'TPBank',      10500000),   -- AccountID = 16 (chi tiêu hằng ngày)
(12, 'Agribank',    15000000);   -- AccountID = 17 (tiết kiệm)

-- ── INCOME User 12 (12/2024 – 5/2026, freelancer = biến động mạnh) ──
-- 2025-10
INSERT INTO INCOME (UserID, AccountID, Amount, IncomeDate, Description) VALUES
(12, 15, 16000000, '2025-10-10', 'Freelance dashboard design'),
(12, 16,  3500000, '2025-10-28', 'Online course sales');
-- 2025-11
INSERT INTO INCOME (UserID, AccountID, Amount, IncomeDate, Description) VALUES
(12, 15, 11000000, '2025-11-08', 'Logo design batch'),
(12, 16,  4000000, '2025-11-20', 'Teaching design workshop');
-- 2025-12
INSERT INTO INCOME (UserID, AccountID, Amount, IncomeDate, Description) VALUES
(12, 15, 26000000, '2025-12-10', 'Year-end big project'),
(12, 17,  5000000, '2025-12-22', 'Year-end bonus');
-- 2026-01
INSERT INTO INCOME (UserID, AccountID, Amount, IncomeDate, Description) VALUES
(12, 15, 10000000, '2026-01-15', 'Small freelance project'),
(12, 16,  2500000, '2026-01-28', 'Social media management');
-- 2026-02
INSERT INTO INCOME (UserID, AccountID, Amount, IncomeDate, Description) VALUES
(12, 15, 19000000, '2026-02-10', 'App redesign project'),
(12, 17,  3000000, '2026-02-22', 'Passive income - Gumroad');
-- 2026-03
INSERT INTO INCOME (UserID, AccountID, Amount, IncomeDate, Description) VALUES
(12, 15, 22000000, '2026-03-08', 'SaaS product design'),
(12, 16,  5000000, '2026-03-25', 'Design workshop');
-- 2026-04
INSERT INTO INCOME (UserID, AccountID, Amount, IncomeDate, Description) VALUES
(12, 15, 14000000, '2026-04-12', 'Freelance illustration batch'),
(12, 17,  3500000, '2026-04-28', 'Stock dividend');
-- 2026-05 (tháng hiện tại)
INSERT INTO INCOME (UserID, AccountID, Amount, IncomeDate, Description) VALUES
(12, 15, 18000000, '2026-05-06', 'E-commerce UX project'),
(12, 16,  4500000, '2026-05-09', 'Workshop fee'),
(12, 17,  2000000, '2026-05-12', 'Passive income');

-- ── EXPENSES User 12 ──
-- 2025-10
INSERT INTO EXPENSES (UserID, CategoryID, AccountID, Amount, ExpenseDate, Description) VALUES
(12,  1, 16, 1650000, '2025-10-02', 'Grocery & dining'),
(12,  8, 15, 6000000, '2025-10-06', 'Monthly rent'),
(12,  7, 15, 1050000, '2025-10-10', 'Utilities'),
(12,  5, 16, 1200000, '2025-10-20', 'Halloween outing');
-- 2025-11
INSERT INTO EXPENSES (UserID, CategoryID, AccountID, Amount, ExpenseDate, Description) VALUES
(12,  1, 16, 1700000, '2025-11-03', 'Grocery & dining'),
(12,  8, 15, 6000000, '2025-11-06', 'Monthly rent'),
(12,  6, 16, 2200000, '2025-11-11', '11.11 sale'),
(12,  2, 16,  550000, '2025-11-20', 'Grab / taxi'),
(12,  4, 16,  750000, '2025-11-25', 'Eye checkup');
-- 2025-12
INSERT INTO EXPENSES (UserID, CategoryID, AccountID, Amount, ExpenseDate, Description) VALUES
(12,  1, 16, 2000000, '2025-12-03', 'Grocery & Tet prep'),
(12,  8, 15, 6000000, '2025-12-06', 'Monthly rent'),
(12,  9, 17, 6500000, '2025-12-21', 'Year-end trip - Vung Tau'),
(12,  6, 16, 1800000, '2025-12-26', 'Gift shopping'),
(12,  5, 16, 1200000, '2025-12-30', 'New Year Eve party');
-- 2026-01
INSERT INTO EXPENSES (UserID, CategoryID, AccountID, Amount, ExpenseDate, Description) VALUES
(12,  1, 16, 1800000, '2026-01-04', 'Grocery & dining'),
(12,  8, 15, 6500000, '2026-01-06', 'Monthly rent (renewed)'),
(12,  9, 17, 4000000, '2026-01-20', 'Tet travel'),
(12,  6, 16, 2500000, '2026-01-23', 'Tet gift & clothes'),
(12,  2, 16,  600000, '2026-01-29', 'Grab / taxi');
-- 2026-02
INSERT INTO EXPENSES (UserID, CategoryID, AccountID, Amount, ExpenseDate, Description) VALUES
(12,  1, 16, 1550000, '2026-02-02', 'Grocery & dining'),
(12,  8, 15, 6500000, '2026-02-06', 'Monthly rent'),
(12,  7, 15, 1000000, '2026-02-10', 'Utilities'),
(12,  3, 17, 2200000, '2026-02-18', 'Online course - Motion Design'),
(12,  5, 16,  900000, '2026-02-28', 'Movie & dining');
-- 2026-03
INSERT INTO EXPENSES (UserID, CategoryID, AccountID, Amount, ExpenseDate, Description) VALUES
(12,  1, 16, 1700000, '2026-03-03', 'Grocery & dining'),
(12,  8, 15, 6500000, '2026-03-06', 'Monthly rent'),
(12,  9, 17, 5000000, '2026-03-18', 'Trip - Mui Ne'),
(12,  6, 16, 1600000, '2026-03-24', 'Spring clothes'),
(12,  4, 16,  600000, '2026-03-29', 'Pharmacy');
-- 2026-04
INSERT INTO EXPENSES (UserID, CategoryID, AccountID, Amount, ExpenseDate, Description) VALUES
(12,  1, 16, 1800000, '2026-04-02', 'Grocery & dining'),
(12,  8, 15, 6500000, '2026-04-06', 'Monthly rent'),
(12,  7, 15, 1100000, '2026-04-10', 'Utilities'),
(12,  3, 17, 1800000, '2026-04-16', 'Design tools subscription'),
(12,  2, 16,  700000, '2026-04-25', 'Grab / taxi'),
(12, 10, 16,  400000, '2026-04-28', 'Haircut & nails');
-- 2026-05 (tháng hiện tại — giao dịch tuần này để test "1 week")
INSERT INTO EXPENSES (UserID, CategoryID, AccountID, Amount, ExpenseDate, Description) VALUES
(12,  1, 15, 1900000, '2026-05-02', 'Grocery & dining'),
(12,  8, 15, 6500000, '2026-05-06', 'Monthly rent'),
(12,  2, 16,  500000, '2026-05-07', 'Grab / taxi'),
(12,  5, 15,  700000, '2026-05-08', 'Cafe & entertainment'),
(12,  6, 17,  950000, '2026-05-09', 'Online shopping'),
(12,  1, 16,  380000, '2026-05-10', 'Lunch & coffee'),
(12,  3, 17,  800000, '2026-05-11', 'E-book purchase'),
(12,  4, 16,  500000, '2026-05-12', 'Pharmacy');