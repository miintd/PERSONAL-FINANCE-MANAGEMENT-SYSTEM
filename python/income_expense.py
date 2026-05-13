# income_expense.py — Business Logic Layer
# Tất cả hàm chỉ return data, KHÔNG print. GUI/CLI tự xử lý hiển thị.
from database import Database
from datetime import date, datetime


# ==================== TÀI KHOẢN NGÂN HÀNG ====================
def get_user_accounts(user_id):
    """Trả về danh sách tài khoản ngân hàng của user"""
    db = Database()
    try:
        return db.fetchall(
            "SELECT AccountID, BankName, Balance FROM BANKACCOUNTS "
            "WHERE UserID = %s ORDER BY AccountID",
            (user_id,)
        )
    finally:
        db.close()


def get_account_balance(account_id):
    """Lấy số dư hiện tại của một tài khoản"""
    db = Database()
    try:
        row = db.fetchone(
            "SELECT Balance FROM BANKACCOUNTS WHERE AccountID = %s",
            (account_id,))
        return float(row['Balance']) if row else 0
    finally:
        db.close()


def get_account_info(account_id):
    """Lấy thông tin đầy đủ của một tài khoản (BankName, Balance)"""
    db = Database()
    try:
        return db.fetchone(
            "SELECT AccountID, BankName, Balance FROM BANKACCOUNTS "
            "WHERE AccountID = %s", (account_id,))
    finally:
        db.close()


def get_total_balance(user_id):
    """Tổng số dư tất cả tài khoản của user"""
    db = Database()
    try:
        row = db.fetchone(
            "SELECT IFNULL(SUM(Balance),0) AS total FROM BANKACCOUNTS "
            "WHERE UserID = %s", (user_id,))
        return float(row['total']) if row and row['total'] else 0
    finally:
        db.close()


# ==================== THU NHẬP ====================
def add_income(user_id, account_id, amount, description, income_date=None):
    """Thêm thu nhập — dùng sp_add_income. Trả về (success, message)"""
    if income_date is None:
        income_date = date.today().strftime("%Y-%m-%d")
    db = Database()
    try:
        result = db.call_procedure("sp_add_income", (
            user_id, account_id, amount, income_date, description
        ))
        if result and len(result) > 0:
            msg = result[0][0] if isinstance(result[0], tuple) else result[0]
            if isinstance(msg, dict):
                msg = msg.get('Message', str(msg))
            if "Error" in str(msg):
                return False, str(msg)
        return True, f"Đã thêm thu nhập: {amount:,.0f} VND"
    except Exception as e:
        return False, str(e)
    finally:
        db.close()


def get_all_income(user_id, account_id=None):
    """Lấy danh sách thu nhập (JOIN BankName). Trả về list[dict]"""
    db = Database()
    try:
        if account_id:
            return db.fetchall(
                "SELECT i.IncomeID, b.BankName, i.Amount, i.IncomeDate, i.Description "
                "FROM INCOME i JOIN BANKACCOUNTS b ON i.AccountID = b.AccountID "
                "WHERE i.UserID = %s AND i.AccountID = %s ORDER BY i.IncomeDate DESC",
                (user_id, account_id)
            )
        else:
            return db.fetchall(
                "SELECT i.IncomeID, b.BankName, i.Amount, i.IncomeDate, i.Description "
                "FROM INCOME i JOIN BANKACCOUNTS b ON i.AccountID = b.AccountID "
                "WHERE i.UserID = %s ORDER BY i.IncomeDate DESC",
                (user_id,)
            )
    finally:
        db.close()


def delete_income(income_id):
    """Xóa thu nhập (trigger tự trừ Balance). Trả về (success, message)"""
    db = Database()
    try:
        db.execute("DELETE FROM INCOME WHERE IncomeID = %s", (income_id,))
        return True, f"Đã xóa thu nhập ID {income_id}"
    except Exception as e:
        return False, str(e)
    finally:
        db.close()


# ==================== DANH MỤC CHI TIÊU ====================
def get_categories():
    """Trả về danh sách danh mục chi tiêu"""
    db = Database()
    try:
        return db.fetchall(
            "SELECT * FROM EXPENSECATEGORIES ORDER BY CategoryID")
    finally:
        db.close()


# ==================== CHI TIÊU ====================
def add_expense(user_id, account_id, category_id, amount, description,
                expense_date=None):
    """Thêm chi tiêu — dùng sp_add_expense. Trả về (success, message)"""
    if expense_date is None:
        expense_date = date.today().strftime("%Y-%m-%d")
    db = Database()
    try:
        result = db.call_procedure("sp_add_expense", (
            user_id, account_id, category_id, amount, expense_date, description
        ))
        if result and len(result) > 0:
            msg = result[0][0] if isinstance(result[0], tuple) else result[0]
            if isinstance(msg, dict):
                msg = msg.get('Message', str(msg))
            if "Insufficient" in str(msg) or "Error" in str(msg):
                return False, str(msg)
        return True, f"Đã thêm chi tiêu: {amount:,.0f} VND"
    except Exception as e:
        return False, str(e)
    finally:
        db.close()


def get_all_expenses(user_id, account_id=None):
    """Lấy danh sách chi tiêu (JOIN BankName, CategoryName). Trả về list[dict]"""
    db = Database()
    try:
        if account_id:
            return db.fetchall(
                "SELECT e.ExpenseID, b.BankName, c.CategoryName, "
                "e.Amount, e.ExpenseDate, e.Description "
                "FROM EXPENSES e "
                "JOIN BANKACCOUNTS b ON e.AccountID = b.AccountID "
                "JOIN EXPENSECATEGORIES c ON e.CategoryID = c.CategoryID "
                "WHERE e.UserID = %s AND e.AccountID = %s "
                "ORDER BY e.ExpenseDate DESC",
                (user_id, account_id)
            )
        else:
            return db.fetchall(
                "SELECT e.ExpenseID, b.BankName, c.CategoryName, "
                "e.Amount, e.ExpenseDate, e.Description "
                "FROM EXPENSES e "
                "JOIN BANKACCOUNTS b ON e.AccountID = b.AccountID "
                "JOIN EXPENSECATEGORIES c ON e.CategoryID = c.CategoryID "
                "WHERE e.UserID = %s "
                "ORDER BY e.ExpenseDate DESC",
                (user_id,)
            )
    finally:
        db.close()


def delete_expense(expense_id):
    """Xóa chi tiêu (trigger tự hoàn Balance). Trả về (success, message)"""
    db = Database()
    try:
        db.execute("DELETE FROM EXPENSES WHERE ExpenseID = %s", (expense_id,))
        return True, f"Đã xóa chi tiêu ID {expense_id}"
    except Exception as e:
        return False, str(e)
    finally:
        db.close()


# ==================== SQL FUNCTION — Kiểm tra số dư ====================
def check_sufficient_balance(account_id, amount):
    """Kiểm tra số dư có đủ không — dùng fn_sufficient_balance. Trả về bool"""
    db = Database()
    try:
        row = db.fetchone(
            "SELECT fn_sufficient_balance(%s, %s) AS ok",
            (account_id, amount))
        return bool(row['ok']) if row else False
    finally:
        db.close()


# ==================== BÁO CÁO — dùng SQL Function ====================
def get_monthly_summary(user_id, month=None, year=None):
    """Tổng thu, chi, tiết kiệm — dùng fn_total_income/expense_by_user.
    Trả về (income: float, expense: float, savings: float)"""
    if month is None or year is None:
        now = datetime.now()
        month = month or now.month
        year = year or now.year
    db = Database()
    try:
        inc = db.fetchone(
            "SELECT fn_total_income_by_user(%s, %s, %s) AS v",
            (user_id, month, year))
        exp = db.fetchone(
            "SELECT fn_total_expense_by_user(%s, %s, %s) AS v",
            (user_id, month, year))
        total_inc = float(inc['v']) if inc and inc['v'] else 0
        total_exp = float(exp['v']) if exp and exp['v'] else 0
        return total_inc, total_exp, total_inc - total_exp
    finally:
        db.close()


def get_monthly_income_sum(user_id, month, year):
    """Tổng thu nhập trong tháng cụ thể (query trực tiếp, không dùng function)"""
    db = Database()
    try:
        row = db.fetchone(
            "SELECT IFNULL(SUM(Amount),0) AS v FROM INCOME "
            "WHERE UserID=%s AND MONTH(IncomeDate)=%s AND YEAR(IncomeDate)=%s",
            (user_id, month, year))
        return float(row['v']) if row else 0
    finally:
        db.close()


def get_monthly_expense_sum(user_id, month, year):
    """Tổng chi tiêu trong tháng cụ thể"""
    db = Database()
    try:
        row = db.fetchone(
            "SELECT IFNULL(SUM(Amount),0) AS v FROM EXPENSES "
            "WHERE UserID=%s AND MONTH(ExpenseDate)=%s AND YEAR(ExpenseDate)=%s",
            (user_id, month, year))
        return float(row['v']) if row else 0
    finally:
        db.close()


def get_budget_status_by_user(user_id, month, year):
    """Trạng thái ngân sách — dùng fn_budget_status_by_user. Trả về str"""
    db = Database()
    try:
        row = db.fetchone(
            "SELECT fn_budget_status_by_user(%s, %s, %s) AS v",
            (user_id, month, year))
        return row['v'] if row and row['v'] else 'N/A'
    finally:
        db.close()


# ==================== BÁO CÁO — dùng SQL View ====================
def get_monthly_trend_data(user_id, limit=6):
    """Dữ liệu trend thu-chi — dùng vw_monthly_summary_by_account.
    Trả về list[dict] có Month, Year, Inc, Exp"""
    db = Database()
    try:
        return db.fetchall(
            "SELECT Month, Year, "
            "SUM(TotalIncome) AS Inc, SUM(TotalExpense) AS Exp "
            "FROM vw_monthly_summary_by_account "
            "WHERE UserID=%s "
            "GROUP BY Year, Month "
            "ORDER BY Year DESC, Month DESC LIMIT %s",
            (user_id, limit))
    finally:
        db.close()


def get_category_spending_by_month(user_id, month, year):
    """Chi tiêu theo danh mục trong tháng. Trả về list[dict]"""
    db = Database()
    try:
        return db.fetchall(
            "SELECT c.CategoryName, COUNT(e.ExpenseID) AS Cnt, "
            "SUM(e.Amount) AS Total, AVG(e.Amount) AS Avg "
            "FROM EXPENSES e "
            "JOIN EXPENSECATEGORIES c ON e.CategoryID=c.CategoryID "
            "WHERE e.UserID=%s AND MONTH(e.ExpenseDate)=%s "
            "AND YEAR(e.ExpenseDate)=%s "
            "GROUP BY c.CategoryName ORDER BY Total DESC",
            (user_id, month, year))
    finally:
        db.close()


# ==================== BÁO CÁO — Alerts ====================
def get_low_balance_accounts(user_id, threshold=1000000):
    """Danh sách tài khoản có số dư thấp hơn threshold"""
    db = Database()
    try:
        return db.fetchall(
            "SELECT BankName, Balance FROM BANKACCOUNTS "
            "WHERE UserID=%s AND Balance < %s",
            (user_id, threshold))
    finally:
        db.close()


def get_deficit_months(user_id, limit=6):
    """Các tháng chi vượt thu — dùng vw_monthly_summary_by_account"""
    db = Database()
    try:
        return db.fetchall(
            "SELECT Month, Year, SUM(TotalIncome) AS Inc, "
            "SUM(TotalExpense) AS Exp "
            "FROM vw_monthly_summary_by_account WHERE UserID=%s "
            "GROUP BY Year, Month "
            "HAVING Exp > Inc ORDER BY Year DESC, Month DESC LIMIT %s",
            (user_id, limit))
    finally:
        db.close()


def get_top_categories(user_id, month, year, limit=3):
    """Top N danh mục chi tiêu lớn nhất trong tháng"""
    db = Database()
    try:
        return db.fetchall(
            "SELECT c.CategoryName, SUM(e.Amount) AS Total "
            "FROM EXPENSES e "
            "JOIN EXPENSECATEGORIES c ON e.CategoryID=c.CategoryID "
            "WHERE e.UserID=%s AND MONTH(e.ExpenseDate)=%s "
            "AND YEAR(e.ExpenseDate)=%s "
            "GROUP BY c.CategoryName ORDER BY Total DESC LIMIT %s",
            (user_id, month, year, limit))
    finally:
        db.close()


# ==================== BÁO CÁO — Lịch sử & Trend ====================
def get_transaction_history(user_id):
    """Lịch sử giao dịch (thu + chi) — UNION ALL. Trả về list[dict]"""
    db = Database()
    try:
        return db.fetchall(
            "SELECT 'income' AS type, AccountID, IncomeDate AS txDate, Amount "
            "FROM INCOME WHERE UserID=%s "
            "UNION ALL "
            "SELECT 'expense', AccountID, ExpenseDate, Amount "
            "FROM EXPENSES WHERE UserID=%s "
            "ORDER BY txDate",
            (user_id, user_id))
    finally:
        db.close()


def get_daily_income(user_id, start_date):
    """Thu nhập theo ngày từ start_date. Trả về list[dict] có d, v"""
    db = Database()
    try:
        return db.fetchall(
            "SELECT DATE(IncomeDate) AS d, SUM(Amount) AS v "
            "FROM INCOME WHERE UserID=%s AND IncomeDate >= %s "
            "GROUP BY DATE(IncomeDate) ORDER BY d",
            (user_id, str(start_date)))
    finally:
        db.close()


def get_daily_expense(user_id, start_date):
    """Chi tiêu theo ngày từ start_date. Trả về list[dict] có d, v"""
    db = Database()
    try:
        return db.fetchall(
            "SELECT DATE(ExpenseDate) AS d, SUM(Amount) AS v "
            "FROM EXPENSES WHERE UserID=%s AND ExpenseDate >= %s "
            "GROUP BY DATE(ExpenseDate) ORDER BY d",
            (user_id, str(start_date)))
    finally:
        db.close()