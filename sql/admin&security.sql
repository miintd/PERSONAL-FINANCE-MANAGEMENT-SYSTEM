USE personal_finance;

-- User 1: Admin — toàn quyền
CREATE USER 'pf_admin'@'localhost' IDENTIFIED BY 'Admin@123456';

-- User 2: App user — dùng cho Python app, đọc/ghi dữ liệu
CREATE USER 'pf_app'@'localhost' IDENTIFIED BY 'App@123456';

-- User 3: Report user — chỉ đọc, dùng cho báo cáo
CREATE USER 'pf_report'@'localhost' IDENTIFIED BY 'Report@123456';

-- User 4: Readonly user — chỉ xem View, không thấy bảng gốc
CREATE USER 'pf_readonly'@'localhost' IDENTIFIED BY 'Readonly@123456';


-- Admin: toàn quyền trên database
GRANT ALL PRIVILEGES ON personal_finance.* TO 'pf_admin'@'localhost' WITH GRANT OPTION;

-- App user: đọc/ghi bảng + gọi procedure & function
GRANT SELECT, INSERT, UPDATE, DELETE 
    ON personal_finance.* 
    TO 'pf_app'@'localhost';

GRANT EXECUTE 
    ON personal_finance.* 
    TO 'pf_app'@'localhost';

-- Report user: chỉ đọc toàn bộ database
GRANT SELECT 
    ON personal_finance.* 
    TO 'pf_report'@'localhost';
    
-- Tạo view che giấu thông tin nhạy cảm (dành cho readonly)
CREATE OR REPLACE VIEW vw_users_safe AS
SELECT 
    UserID,
    UserName,
    CONCAT(LEFT(Email, 3), '***@***.com') AS Email,
    CONCAT('***', RIGHT(PhoneNumber, 3)) AS PhoneNumber
FROM USERS;

-- Readonly user: chỉ xem các view cụ thể
GRANT SELECT ON personal_finance.vw_users_safe TO 'pf_readonly'@'localhost';
GRANT SELECT ON personal_finance.vw_monthly_summary_by_account  TO 'pf_readonly'@'localhost';
GRANT SELECT ON personal_finance.vw_category_spending_by_account TO 'pf_readonly'@'localhost';
GRANT SELECT ON personal_finance.vw_user_total_balance      TO 'pf_readonly'@'localhost';

-- Áp dụng thay đổi
FLUSH PRIVILEGES;

-- Xem quyền của từng user
SHOW GRANTS FOR 'pf_admin'@'localhost';
SHOW GRANTS FOR 'pf_app'@'localhost';
SHOW GRANTS FOR 'pf_report'@'localhost';
SHOW GRANTS FOR 'pf_readonly'@'localhost';


-- ====================== OPTIMIZATION =============================
-- Kiểm tra index đã tạo ở bước 4
SHOW INDEX FROM INCOME;
SHOW INDEX FROM EXPENSES;
SHOW INDEX FROM BANKACCOUNTS;

-- Phân tích hiệu suất câu truy vấn (EXPLAIN)
EXPLAIN SELECT * FROM EXPENSES WHERE UserID = 1;
EXPLAIN SELECT * FROM INCOME  WHERE IncomeDate = '2025-01-05';

-- Xem trạng thái tổng quát của MySQL server
SHOW STATUS LIKE 'Slow_queries';
SHOW STATUS LIKE 'Uptime';
SHOW VARIABLES LIKE 'slow_query_log';
