# expense.py
from database import Database
from datetime import date

# ==================== HÀM LẤY DANH SÁCH TÀI KHOẢN ====================
def get_user_accounts(user_id):
    """Trả về danh sách các tài khoản ngân hàng của user"""
    db = Database()
    try:
        rows = db.fetchall(
            "SELECT AccountID, BankName, Balance FROM BANKACCOUNTS WHERE UserID = %s",
            (user_id,)
        )
        return rows
    finally:
        db.close()

def get_account_balance(account_id):
    """Lấy số dư hiện tại của một tài khoản"""
    db = Database()
    try:
        row = db.fetchone("SELECT Balance FROM BANKACCOUNTS WHERE AccountID = %s", (account_id,))
        return row['Balance'] if row else 0
    finally:
        db.close()

def get_total_balance(user_id):
    """Tổng số dư tất cả tài khoản của user"""
    db = Database()
    try:
        row = db.fetchone("SELECT SUM(Balance) AS total FROM BANKACCOUNTS WHERE UserID = %s", (user_id,))
        return row['total'] if row and row['total'] else 0
    finally:
        db.close()

# ==================== THU NHẬP ====================
def add_income(user_id, account_id, amount, description):
    """Thêm thu nhập cho tài khoản cụ thể"""
    db = Database()
    try:
        result = db.call_procedure("sp_add_income", (
            user_id,
            account_id,
            amount,
            date.today().strftime("%Y-%m-%d"),
            description
        ))
        if result and len(result) > 0:
            msg = result[0][0] if isinstance(result[0], tuple) else result[0]
            if "Error" in str(msg):
                print(f"\n❌ {msg}")
            else:
                print(f"\n✅ Đã thêm thu nhập: {amount:,.0f} VND — {description}")
        else:
            print(f"\n✅ Đã thêm thu nhập: {amount:,.0f} VND — {description}")
    except Exception as e:
        print(f"❌ Lỗi: {e}")
    finally:
        db.close()

def view_income(user_id, account_id=None):
    """Xem thu nhập (tất cả hoặc lọc theo account_id)"""
    db = Database()
    try:
        if account_id:
            rows = db.fetchall(
                "SELECT IncomeID, Amount, IncomeDate, Description "
                "FROM INCOME WHERE UserID = %s AND AccountID = %s ORDER BY IncomeDate DESC",
                (user_id, account_id)
            )
        else:
            rows = db.fetchall(
                "SELECT i.IncomeID, b.BankName, i.Amount, i.IncomeDate, i.Description "
                "FROM INCOME i JOIN BANKACCOUNTS b ON i.AccountID = b.AccountID "
                "WHERE i.UserID = %s ORDER BY i.IncomeDate DESC",
                (user_id,)
            )
        if not rows:
            print("\nKhông có dữ liệu thu nhập.")
            return
        print(f"\n{'─'*70}")
        if account_id:
            print(f"{'ID':<6} {'Số tiền':>15} {'Ngày':<14} {'Mô tả'}")
            print(f"{'─'*70}")
            for r in rows:
                print(f"{r['IncomeID']:<6} {r['Amount']:>15,.0f} "
                      f"{str(r['IncomeDate']):<14} {r['Description']}")
        else:
            print(f"{'ID':<6} {'Ngân hàng':<15} {'Số tiền':>15} {'Ngày':<14} {'Mô tả'}")
            print(f"{'─'*70}")
            for r in rows:
                print(f"{r['IncomeID']:<6} {r['BankName']:<15} {r['Amount']:>15,.0f} "
                      f"{str(r['IncomeDate']):<14} {r['Description']}")
        print(f"{'─'*70}")
    finally:
        db.close()

def delete_income(income_id):
    """Xóa thu nhập (trigger sẽ tự động trừ lại số dư)"""
    db = Database()
    try:
        db.execute("DELETE FROM INCOME WHERE IncomeID = %s", (income_id,))
        print(f"\n✅ Đã xóa thu nhập ID {income_id}")
    except Exception as e:
        print(f"❌ Lỗi: {e}")
    finally:
        db.close()

# ==================== DANH MỤC CHI TIÊU ====================
def view_categories():
    """Hiển thị danh sách danh mục chi tiêu"""
    db = Database()
    try:
        rows = db.fetchall("SELECT * FROM EXPENSECATEGORIES ORDER BY CategoryID")
        if not rows:
            print("\nKhông có danh mục nào.")
            return []
        print(f"\n{'─'*30}")
        print(f"{'ID':<6} {'Danh mục'}")
        print(f"{'─'*30}")
        for r in rows:
            print(f"{r['CategoryID']:<6} {r['CategoryName']}")
        print(f"{'─'*30}")
        return rows
    finally:
        db.close()

# ==================== CHI TIÊU ====================
def add_expense(user_id, account_id, category_id, amount, description):
    """Thêm chi tiêu, có kiểm tra số dư (do stored procedure kiểm tra)"""
    db = Database()
    try:
        result = db.call_procedure("sp_add_expense", (
            user_id,
            account_id,
            category_id,
            amount,
            date.today().strftime("%Y-%m-%d"),
            description
        ))
        if result and len(result) > 0:
            msg = result[0][0] if isinstance(result[0], tuple) else result[0]
            if "Insufficient" in str(msg) or "Error" in str(msg):
                print(f"\n❌ {msg}")
            else:
                print(f"\n✅ Đã thêm chi tiêu: {amount:,.0f} VND — {description}")
        else:
            print(f"\n✅ Đã thêm chi tiêu: {amount:,.0f} VND — {description}")
    except Exception as e:
        print(f"❌ Lỗi: {e}")
    finally:
        db.close()

def view_expenses(user_id, account_id=None):
    """Xem chi tiêu (tất cả hoặc lọc theo account_id)"""
    db = Database()
    try:
        if account_id:
            rows = db.fetchall(
                "SELECT e.ExpenseID, c.CategoryName, e.Amount, e.ExpenseDate, e.Description "
                "FROM EXPENSES e "
                "JOIN EXPENSECATEGORIES c ON e.CategoryID = c.CategoryID "
                "WHERE e.UserID = %s AND e.AccountID = %s "
                "ORDER BY e.ExpenseDate DESC",
                (user_id, account_id)
            )
        else:
            rows = db.fetchall(
                "SELECT e.ExpenseID, b.BankName, c.CategoryName, e.Amount, e.ExpenseDate, e.Description "
                "FROM EXPENSES e "
                "JOIN BANKACCOUNTS b ON e.AccountID = b.AccountID "
                "JOIN EXPENSECATEGORIES c ON e.CategoryID = c.CategoryID "
                "WHERE e.UserID = %s "
                "ORDER BY e.ExpenseDate DESC",
                (user_id,)
            )
        if not rows:
            print("\nKhông có dữ liệu chi tiêu.")
            return
        print(f"\n{'─'*80}")
        if account_id:
            print(f"{'ID':<6} {'Danh mục':<18} {'Số tiền':>12} {'Ngày':<14} {'Mô tả'}")
            print(f"{'─'*80}")
            for r in rows:
                print(f"{r['ExpenseID']:<6} {r['CategoryName']:<18} "
                      f"{r['Amount']:>12,.0f} {str(r['ExpenseDate']):<14} {r['Description']}")
        else:
            print(f"{'ID':<6} {'Ngân hàng':<15} {'Danh mục':<18} {'Số tiền':>12} {'Ngày':<14} {'Mô tả'}")
            print(f"{'─'*80}")
            for r in rows:
                print(f"{r['ExpenseID']:<6} {r['BankName']:<15} {r['CategoryName']:<18} "
                      f"{r['Amount']:>12,.0f} {str(r['ExpenseDate']):<14} {r['Description']}")
        print(f"{'─'*80}")
    finally:
        db.close()

def delete_expense(expense_id):
    """Xóa chi tiêu (trigger sẽ tự động hoàn lại số dư)"""
    db = Database()
    try:
        db.execute("DELETE FROM EXPENSES WHERE ExpenseID = %s", (expense_id,))
        print(f"\n✅ Đã xóa chi tiêu ID {expense_id}")
    except Exception as e:
        print(f"❌ Lỗi: {e}")
    finally:
        db.close()

# ==================== BÁO CÁO NHANH ====================
def get_balance_summary(user_id):
    """Hiển thị tổng số dư và từng tài khoản"""
    accounts = get_user_accounts(user_id)
    if not accounts:
        print("\n⚠️ Bạn chưa có tài khoản ngân hàng nào. Hãy thêm tài khoản trước.")
        return
    print(f"\n{'─'*50}")
    print(f"{'Ngân hàng':<20} {'Số dư':>20}")
    print(f"{'─'*50}")
    total = 0
    for acc in accounts:
        print(f"{acc['BankName']:<20} {acc['Balance']:>20,.0f} VND")
        total += acc['Balance']
    print(f"{'─'*50}")
    print(f"{'Tổng số dư':<20} {total:>20,.0f} VND")
    print(f"{'─'*50}")
    return accounts

def get_monthly_summary(user_id, month=None, year=None):
    """Trả về tổng thu, chi trong tháng (dùng function có sẵn)"""
    if month is None or year is None:
        from datetime import datetime
        now = datetime.now()
        month = month or now.month
        year = year or now.year
    db = Database()
    try:
        income = db.fetchone("SELECT fn_total_income_by_user(%s, %s, %s) AS inc", (user_id, month, year))
        expense = db.fetchone("SELECT fn_total_expense_by_user(%s, %s, %s) AS exp", (user_id, month, year))
        total_income = income['inc'] if income else 0
        total_expense = expense['exp'] if expense else 0
        savings = total_income - total_expense
        print(f"\n{'─'*40}")
        print(f"BÁO CÁO THÁNG {month}/{year}")
        print(f"{'─'*40}")
        print(f"Tổng thu nhập: {total_income:>15,.0f} VND")
        print(f"Tổng chi tiêu: {total_expense:>15,.0f} VND")
        print(f"Tiết kiệm:     {savings:>15,.0f} VND")
        print(f"{'─'*40}")
        return total_income, total_expense, savings
    finally:
        db.close()