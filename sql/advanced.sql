USE personal_finance;

-- =================================== INDEX =================================================
-- Tìm kiếm income/expense theo UserID nhanh hơn
CREATE INDEX idx_income_user     ON INCOME(UserID);
CREATE INDEX idx_expenses_user   ON EXPENSES(UserID);
CREATE INDEX idx_bankaccount_user ON BANKACCOUNTS(UserID);

-- Lọc theo ngày tháng nhanh hơn
CREATE INDEX idx_income_date     ON INCOME(IncomeDate);
CREATE INDEX idx_expenses_date   ON EXPENSES(ExpenseDate);

-- Lọc expense theo category
CREATE INDEX idx_expenses_category ON EXPENSES(CategoryID);
CREATE INDEX idx_income_account    ON INCOME(AccountID);
CREATE INDEX idx_expenses_account  ON EXPENSES(AccountID);


-- =================================== VIEW =================================================
-- View 1: Tổng thu - chi theo tháng, theo user và theo tài khoản
CREATE VIEW vw_monthly_summary_by_account AS
SELECT 
    u.UserID,
    u.UserName,
    b.AccountID,
    b.BankName,
    YEAR(i.IncomeDate) AS Year,
    MONTH(i.IncomeDate) AS Month,
    IFNULL(SUM(i.Amount), 0) AS TotalIncome,
    IFNULL(SUM(e.Amount), 0) AS TotalExpense,
    IFNULL(SUM(i.Amount), 0) - IFNULL(SUM(e.Amount), 0) AS NetCashFlow
FROM USERS u
JOIN BANKACCOUNTS b ON u.UserID = b.UserID
LEFT JOIN INCOME i ON b.AccountID = i.AccountID
LEFT JOIN EXPENSES e ON b.AccountID = e.AccountID
    AND YEAR(e.ExpenseDate) = YEAR(i.IncomeDate)
    AND MONTH(e.ExpenseDate) = MONTH(i.IncomeDate)
GROUP BY u.UserID, u.UserName, b.AccountID, b.BankName, Year, Month;

-- View 2: Chi tiêu theo danh mục (phân biệt tài khoản)
CREATE VIEW vw_category_spending_by_account AS
SELECT 
    u.UserID,
    u.UserName,
    b.AccountID,
    b.BankName,
    c.CategoryName,
    COUNT(e.ExpenseID) AS TotalTransactions,
    SUM(e.Amount) AS TotalSpent,
    ROUND(AVG(e.Amount), 2) AS AvgPerTransaction
FROM USERS u
JOIN BANKACCOUNTS b ON u.UserID = b.UserID
JOIN EXPENSES e ON b.AccountID = e.AccountID
JOIN EXPENSECATEGORIES c ON e.CategoryID = c.CategoryID
GROUP BY u.UserID, u.UserName, b.AccountID, b.BankName, c.CategoryName;

-- View 3: Tổng số dư tất cả tài khoản của từng user
CREATE VIEW vw_user_total_balance AS
SELECT 
    u.UserID,
    u.UserName,
    COUNT(b.AccountID) AS TotalAccounts,
    SUM(b.Balance) AS TotalBalance
FROM USERS u
LEFT JOIN BANKACCOUNTS b ON u.UserID = b.UserID
GROUP BY u.UserID, u.UserName;


-- ---------- FUNCTIONS ----------
-- Function 1: Tổng thu nhập của một tài khoản trong tháng
DELIMITER $$
CREATE FUNCTION fn_income_by_account(
    p_AccountID INT,
    p_Month     INT,
    p_Year      INT
) RETURNS DECIMAL(15,2)
DETERMINISTIC
BEGIN
    DECLARE total DECIMAL(15,2);
    SELECT IFNULL(SUM(Amount), 0) INTO total
    FROM INCOME
    WHERE AccountID = p_AccountID
      AND MONTH(IncomeDate) = p_Month
      AND YEAR(IncomeDate) = p_Year;
    RETURN total;
END$$
DELIMITER ;

-- Function 2: Tổng chi tiêu của một tài khoản trong tháng
DELIMITER $$
CREATE FUNCTION fn_expense_by_account(
    p_AccountID INT,
    p_Month     INT,
    p_Year      INT
) RETURNS DECIMAL(15,2)
DETERMINISTIC
BEGIN
    DECLARE total DECIMAL(15,2);
    SELECT IFNULL(SUM(Amount), 0) INTO total
    FROM EXPENSES
    WHERE AccountID = p_AccountID
      AND MONTH(ExpenseDate) = p_Month
      AND YEAR(ExpenseDate) = p_Year;
    RETURN total;
END$$
DELIMITER ;

-- Function 3: Kiểm tra số dư đủ không
DELIMITER $$
CREATE FUNCTION fn_sufficient_balance(
    p_AccountID INT,
    p_Amount    DECIMAL(15,2)
) RETURNS BOOLEAN
DETERMINISTIC
BEGIN
    DECLARE bal DECIMAL(15,2);
    SELECT Balance INTO bal FROM BANKACCOUNTS WHERE AccountID = p_AccountID;
    RETURN bal >= p_Amount;
END$$
DELIMITER ;

-- Function 4: Trạng thái ngân sách theo tài khoản
DELIMITER $$
CREATE FUNCTION fn_budget_status_by_account(
    p_AccountID INT,
    p_Month     INT,
    p_Year      INT
) RETURNS VARCHAR(20)
DETERMINISTIC
BEGIN
    DECLARE income  DECIMAL(15,2);
    DECLARE expense DECIMAL(15,2);
    SET income  = fn_income_by_account(p_AccountID, p_Month, p_Year);
    SET expense = fn_expense_by_account(p_AccountID, p_Month, p_Year);
    IF income > expense THEN RETURN 'Surplus';
    ELSEIF income < expense THEN RETURN 'Deficit';
    ELSE RETURN 'Balanced';
    END IF;
END$$
DELIMITER ;

-- Function 5: tổng thu nhập của tất cả tài khoản của một user trong tháng
DELIMITER $$
CREATE FUNCTION fn_total_income_by_user(
    p_UserID INT,
    p_Month  INT,
    p_Year   INT
) RETURNS DECIMAL(15,2)
DETERMINISTIC
BEGIN
    DECLARE total DECIMAL(15,2);
    SELECT IFNULL(SUM(Amount), 0) INTO total
    FROM INCOME
    WHERE UserID = p_UserID
      AND MONTH(IncomeDate) = p_Month
      AND YEAR(IncomeDate) = p_Year;
    RETURN total;
END$$
DELIMITER ;

-- Function 6: tổng chi tiêu của tất cả tài khoản của một user trong tháng
DELIMITER $$
CREATE FUNCTION fn_total_expense_by_user(
    p_UserID INT,
    p_Month  INT,
    p_Year   INT
) RETURNS DECIMAL(15,2)
DETERMINISTIC
BEGIN
    DECLARE total DECIMAL(15,2);
    SELECT IFNULL(SUM(Amount), 0) INTO total
    FROM EXPENSES
    WHERE UserID = p_UserID
      AND MONTH(ExpenseDate) = p_Month
      AND YEAR(ExpenseDate) = p_Year;
    RETURN total;
END$$
DELIMITER ;

-- Function 7: Trạng thái ngân sách theo user
DELIMITER $$
CREATE FUNCTION fn_budget_status_by_user(
    p_UserID INT,
    p_Month  INT,
    p_Year   INT
) RETURNS VARCHAR(20)
DETERMINISTIC
BEGIN
    DECLARE income  DECIMAL(15,2);
    DECLARE expense DECIMAL(15,2);
    SET income  = fn_total_income_by_user(p_UserID, p_Month, p_Year);
    SET expense = fn_total_expense_by_user(p_UserID, p_Month, p_Year);
    IF income > expense THEN RETURN 'Surplus';
    ELSEIF income < expense THEN RETURN 'Deficit';
    ELSE RETURN 'Balanced';
    END IF;
END$$
DELIMITER ;


-- =================================== PROCEDURE =================================================
-- Procedure 1: Thêm giao dịch thu nhập mới và tự cập nhật số dư
DELIMITER $$
CREATE PROCEDURE sp_add_income(
    IN p_UserID      INT,
    IN p_AccountID   INT,
    IN p_Amount      DECIMAL(15,2),
    IN p_IncomeDate  DATE,
    IN p_Description VARCHAR(255)
)
BEGIN
    IF NOT EXISTS (SELECT 1 FROM BANKACCOUNTS WHERE AccountID = p_AccountID AND UserID = p_UserID) THEN
        SELECT 'Error: Account does not belong to user' AS Message;
    ELSE
        INSERT INTO INCOME (UserID, AccountID, Amount, IncomeDate, Description)
        VALUES (p_UserID, p_AccountID, p_Amount, p_IncomeDate, p_Description);
        SELECT 'Income added successfully' AS Message;
    END IF;
END$$
DELIMITER ;

-- Procedure 2: Thêm chi tiêu mới và tự cập nhật số dư
DELIMITER $$
CREATE PROCEDURE sp_add_expense(
    IN p_UserID      INT,
    IN p_AccountID   INT,
    IN p_CategoryID  INT,
    IN p_Amount      DECIMAL(15,2),
    IN p_ExpenseDate DATE,
    IN p_Description VARCHAR(255)
)
BEGIN
    DECLARE current_balance DECIMAL(15,2);
    IF NOT EXISTS (SELECT 1 FROM BANKACCOUNTS WHERE AccountID = p_AccountID AND UserID = p_UserID) THEN
        SELECT 'Error: Account does not belong to user' AS Message;
    ELSE
        SELECT Balance INTO current_balance FROM BANKACCOUNTS WHERE AccountID = p_AccountID;
        IF current_balance < p_Amount THEN
            SELECT 'Insufficient balance' AS Message;
        ELSE
            INSERT INTO EXPENSES (UserID, AccountID, CategoryID, Amount, ExpenseDate, Description)
            VALUES (p_UserID, p_AccountID, p_CategoryID, p_Amount, p_ExpenseDate, p_Description);
            SELECT 'Expense added successfully' AS Message;
        END IF;
    END IF;
END$$
DELIMITER ;

-- Procedure 3: Khai báo số dư ban đầu (cho một tài khoản)
DELIMITER $$
CREATE PROCEDURE sp_set_initial_balance(
    IN p_AccountID INT,
    IN p_Balance   DECIMAL(15,2)
)
BEGIN
    UPDATE BANKACCOUNTS SET Balance = p_Balance WHERE AccountID = p_AccountID;
    SELECT CONCAT('Updated balance for account ', p_AccountID, ' to ', p_Balance) AS Message;
END$$
DELIMITER ;

-- Procedure 4: Báo cáo tài chính theo tháng
DELIMITER $$
CREATE PROCEDURE sp_monthly_closure(
    IN p_UserID    INT,
    IN p_AccountID INT,   -- =0: tổng hợp tất cả tài khoản; >0: chỉ một tài khoản
    IN p_Year      INT,
    IN p_Month     INT
)
BEGIN
    DECLARE total_income DECIMAL(15,2);
    DECLARE total_expense DECIMAL(15,2);
    DECLARE closing_balance DECIMAL(15,2);
    
    IF p_AccountID = 0 THEN
        -- Dùng hàm tổng hợp theo user
        SET total_income = fn_total_income_by_user(p_UserID, p_Month, p_Year);
        SET total_expense = fn_total_expense_by_user(p_UserID, p_Month, p_Year);
        SELECT SUM(Balance) INTO closing_balance
        FROM BANKACCOUNTS WHERE UserID = p_UserID;
        
        SELECT 
            p_UserID AS UserID,
            p_Month AS Month,
            p_Year AS Year,
            'All Accounts' AS AccountInfo,
            total_income AS TotalIncome,
            total_expense AS TotalExpense,
            total_income - total_expense AS NetCashFlow,
            IFNULL(closing_balance, 0) AS ClosingBalance;
    ELSE
        -- Dùng hàm theo tài khoản
        SET total_income = fn_income_by_account(p_AccountID, p_Month, p_Year);
        SET total_expense = fn_expense_by_account(p_AccountID, p_Month, p_Year);
        SELECT Balance INTO closing_balance
        FROM BANKACCOUNTS WHERE AccountID = p_AccountID;
        
        SELECT 
            p_UserID AS UserID,
            (SELECT BankName FROM BANKACCOUNTS WHERE AccountID = p_AccountID) AS BankName,
            p_Month AS Month,
            p_Year AS Year,
            total_income AS TotalIncome,
            total_expense AS TotalExpense,
            total_income - total_expense AS NetCashFlow,
            IFNULL(closing_balance, 0) AS ClosingBalance;
    END IF;
END$$
DELIMITER ;


-- ====================================== TRIGGER ==========================================================
-- Trigger 1: Tự động cộng số dư khi INSERT income
DELIMITER $$
CREATE TRIGGER trg_after_income_insert
AFTER INSERT ON INCOME
FOR EACH ROW
BEGIN
    UPDATE BANKACCOUNTS
    SET Balance = Balance + NEW.Amount
    WHERE AccountID = NEW.AccountID;
END$$
DELIMITER ;

-- Trigger 2: Trước khi thêm EXPENSE -> kiểm tra số dư (BEFORE)
DELIMITER $$
CREATE TRIGGER trg_before_expense_insert
BEFORE INSERT ON EXPENSES
FOR EACH ROW
BEGIN
    DECLARE current_balance DECIMAL(15,2);
    SELECT Balance INTO current_balance FROM BANKACCOUNTS WHERE AccountID = NEW.AccountID;
    IF current_balance < NEW.Amount THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Insufficient balance';
    END IF;
END$$
DELIMITER ;

-- Trigger 3: Tự động trừ số dư khi INSERT expense
DELIMITER $$
CREATE TRIGGER trg_after_expense_insert
AFTER INSERT ON EXPENSES
FOR EACH ROW
BEGIN
    UPDATE BANKACCOUNTS
    SET Balance = Balance - NEW.Amount
	WHERE AccountID = NEW.AccountID;
END$$
DELIMITER ;

-- Trigger 4: Hoàn lại số dư khi DELETE expense
DELIMITER $$
CREATE TRIGGER trg_after_expense_delete
AFTER DELETE ON EXPENSES
FOR EACH ROW
BEGIN
    UPDATE BANKACCOUNTS
    SET Balance = Balance + OLD.Amount
    WHERE AccountID = OLD.AccountID;
END$$
DELIMITER ;

-- Trigger 5: Xóa INCOME -> trừ lại Balance
DELIMITER $$
CREATE TRIGGER trg_after_income_delete
AFTER DELETE ON INCOME
FOR EACH ROW
BEGIN
    UPDATE BANKACCOUNTS
    SET Balance = Balance - OLD.Amount
    WHERE AccountID = OLD.AccountID;
END$$