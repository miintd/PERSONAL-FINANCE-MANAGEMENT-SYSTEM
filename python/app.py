# app.py - English version
import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from datetime import date, datetime
import csv, os
from database import Database

# ── Color scheme ──────────────────────────────────────────
BG       = "#F0F4F8"
SIDEBAR  = "#1E2A3A"
CARD     = "#FFFFFF"
PRIMARY  = "#4F8EF7"
SUCCESS  = "#2ECC71"
DANGER   = "#E74C3C"
WARNING  = "#F39C12"
TEXT     = "#2C3E50"
MUTED    = "#7F8C8D"
FONT     = ("Segoe UI", 10)
FONT_B   = ("Segoe UI", 10, "bold")
FONT_H   = ("Segoe UI", 14, "bold")
FONT_BIG = ("Segoe UI", 22, "bold")


# ════════════════════════════════════════════════════════════════
#  LOGIN WINDOW
# ════════════════════════════════════════════════════════════════
class LoginWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("Personal Finance — Login")
        self.root.geometry("420x540")
        self.root.configure(bg=SIDEBAR)
        self.root.resizable(False, False)
        self._center_window(420, 540)
        self._build_ui()

    def _center_window(self, w, h):
        sw = self.root.winfo_screenwidth()
        sh = self.root.winfo_screenheight()
        self.root.geometry(f"{w}x{h}+{(sw-w)//2}+{(sh-h)//2}")

    def _build_ui(self):
        tk.Label(self.root, text="💰", font=("Segoe UI", 48),
                 bg=SIDEBAR, fg=PRIMARY).pack(pady=(40, 0))
        tk.Label(self.root, text="Personal Finance",
                 font=("Segoe UI", 18, "bold"),
                 bg=SIDEBAR, fg="white").pack()
        tk.Label(self.root, text="Management System",
                 font=("Segoe UI", 11), bg=SIDEBAR, fg=MUTED).pack(pady=(0, 30))

        card = tk.Frame(self.root, bg=CARD, bd=0)
        card.pack(padx=30, fill="x")

        tk.Label(card, text="Email", font=FONT_B,
                 bg=CARD, fg=TEXT).pack(anchor="w", padx=20, pady=(20, 2))
        self.email_var = tk.StringVar()
        tk.Entry(card, textvariable=self.email_var, font=FONT,
                 bd=0, bg="#F0F4F8", fg=TEXT,
                 insertbackground=TEXT).pack(fill="x", padx=20, ipady=8)
        tk.Frame(card, bg="#E0E0E0", height=1).pack(fill="x", padx=20)

        tk.Label(card, text="Password", font=FONT_B,
                 bg=CARD, fg=TEXT).pack(anchor="w", padx=20, pady=(14, 2))
        self.pass_var = tk.StringVar()
        tk.Entry(card, textvariable=self.pass_var, font=FONT,
                 show="•", bd=0, bg="#F0F4F8", fg=TEXT,
                 insertbackground=TEXT).pack(fill="x", padx=20, ipady=8)
        tk.Frame(card, bg="#E0E0E0", height=1).pack(fill="x", padx=20)

        self.err_label = tk.Label(card, text="", font=("Segoe UI", 9),
                                  bg=CARD, fg=DANGER)
        self.err_label.pack(pady=(6, 0))

        btn_frame = tk.Frame(card, bg=CARD)
        btn_frame.pack(fill="x", padx=20, pady=(10, 20))

        tk.Button(btn_frame, text="Login", font=FONT_B,
                  bg=PRIMARY, fg="white", bd=0, cursor="hand2",
                  activebackground="#3a7be0", activeforeground="white",
                  command=self.login).pack(fill="x", ipady=10)

        tk.Button(btn_frame, text="Create new account", font=FONT,
                  bg=CARD, fg=PRIMARY, bd=0, cursor="hand2",
                  command=self.open_register).pack(pady=(8, 0))

    def login(self):
        email    = self.email_var.get().strip()
        password = self.pass_var.get().strip()
        if not email or not password:
            self.err_label.config(text="Please enter email and password")
            return
        db = Database()
        user = db.fetchone(
            "SELECT * FROM USERS WHERE Email = %s AND Password = %s",
            (email, password)
        )
        db.close()
        if user:
            self.root.destroy()
            main_root = tk.Tk()
            MainApp(main_root, user)
            main_root.mainloop()
        else:
            db2 = Database()
            exists = db2.fetchone(
                "SELECT UserID FROM USERS WHERE Email = %s", (email,))
            db2.close()
            if not exists:
                if messagebox.askyesno(
                    "Account not found",
                    "This email is not registered.\nDo you want to create a new account?"
                ):
                    self.open_register()
            else:
                self.err_label.config(text="Incorrect password")

    def open_register(self):
        RegisterWindow(self.root)


# ════════════════════════════════════════════════════════════════
#  REGISTER WINDOW
# ════════════════════════════════════════════════════════════════
class RegisterWindow:
    def __init__(self, parent):
        self.win = tk.Toplevel(parent)
        self.win.title("Register Account")
        self.win.geometry("420x500")
        self.win.configure(bg=BG)
        self.win.resizable(False, False)
        self.win.grab_set()
        self._build_ui()

    def _build_ui(self):
        tk.Label(self.win, text="Create new account",
                 font=FONT_H, bg=BG, fg=TEXT).pack(pady=20)

        fields = [
            ("Full Name *",      "name_var",  False),
            ("Email *",          "email_var", False),
            ("Phone Number *",   "phone_var", False),
            ("Password *",       "pass_var",  True),
        ]
        for label, var, is_pass in fields:
            tk.Label(self.win, text=label, font=FONT_B,
                     bg=BG, fg=TEXT).pack(anchor="w", padx=30, pady=(8, 0))
            setattr(self, var, tk.StringVar())
            tk.Entry(self.win, textvariable=getattr(self, var),
                     font=FONT, bd=1, relief="solid",
                     show="•" if is_pass else "").pack(
                fill="x", padx=30, ipady=7)

        self.err = tk.Label(self.win, text="", font=("Segoe UI", 9),
                            bg=BG, fg=DANGER)
        self.err.pack(pady=6)

        tk.Button(self.win, text="Register", font=FONT_B,
                  bg=SUCCESS, fg="white", bd=0, cursor="hand2",
                  command=self.register).pack(fill="x", padx=30, ipady=10)

        tk.Label(self.win, text="* Required fields", font=("Segoe UI", 8),
                 bg=BG, fg=MUTED).pack(pady=(6, 0))

    def register(self):
        name  = self.name_var.get().strip()
        email = self.email_var.get().strip()
        phone = self.phone_var.get().strip()
        pwd   = self.pass_var.get().strip()

        if not all([name, email, phone, pwd]):
            self.err.config(text="Please fill in all fields")
            return
        if "@" not in email or "." not in email:
            self.err.config(text="Invalid email address")
            return
        if len(pwd) < 6:
            self.err.config(text="Password must be at least 6 characters")
            return

        db = Database()
        try:
            existing = db.fetchone(
                "SELECT UserID FROM USERS WHERE Email = %s", (email,))
            if existing:
                self.err.config(text="Email already in use")
                return
            db.execute(
                "INSERT INTO USERS (UserName, Email, PhoneNumber, Password) "
                "VALUES (%s, %s, %s, %s)",
                (name, email, phone, pwd)
            )
            messagebox.showinfo(
                "Registration successful",
                f"Welcome {name}!\nPlease login to continue."
            )
            self.win.destroy()
        except Exception as e:
            self.err.config(text=f"Error: {e}")
        finally:
            db.close()


# ════════════════════════════════════════════════════════════════
#  SETUP BANK ACCOUNT (shown when user has no bank account)
# ════════════════════════════════════════════════════════════════
class SetupBankWindow:
    def __init__(self, root, user, on_done):
        self.root    = root
        self.user    = user
        self.on_done = on_done
        self.win = tk.Toplevel(root)
        self.win.title("Setup Bank Account")
        self.win.configure(bg=BG)
        self.win.resizable(False, False)
        self.win.protocol("WM_DELETE_WINDOW", lambda: None)  # prevent closing
        self.win.grab_set()
        self._build_ui()
        self.win.update_idletasks()
        w = self.win.winfo_reqwidth() + 20
        h = self.win.winfo_reqheight() + 20
        sw = self.win.winfo_screenwidth()
        sh = self.win.winfo_screenheight()
        self.win.geometry(f"{w}x{h}+{(sw-w)//2}+{(sh-h)//2}")

    def _build_ui(self):
        tk.Label(self.win, text="🏦", font=("Segoe UI", 32),
                 bg=BG).pack(pady=(20, 0))
        tk.Label(self.win, text="Bank Account Setup",
                 font=FONT_H, bg=BG, fg=TEXT).pack(pady=(4, 0))
        tk.Label(self.win,
                 text="You don't have any bank account yet.\nPlease add at least one to start.",
                 font=FONT, bg=BG, fg=MUTED, justify="center").pack(pady=(4, 10))

        form = tk.Frame(self.win, bg=CARD)
        form.pack(fill="x", padx=30)

        tk.Label(form, text="Bank Name *", font=FONT_B,
                 bg=CARD, fg=TEXT).pack(anchor="w", padx=16, pady=(14, 2))
        self.bank_var = tk.StringVar()
        banks = ["Vietcombank", "BIDV", "VPBank", "Agribank", "MB Bank",
                 "Techcombank", "Vietinbank", "TPBank", "ACB", "SHB", "Other"]
        ttk.Combobox(form, textvariable=self.bank_var, values=banks,
                     font=FONT, state="normal").pack(
            fill="x", padx=16, ipady=5)

        tk.Label(form, text="Current Balance (VND) *", font=FONT_B,
                 bg=CARD, fg=TEXT).pack(anchor="w", padx=16, pady=(10, 2))
        self.balance_var = tk.StringVar()
        tk.Entry(form, textvariable=self.balance_var, font=FONT,
                 bd=1, relief="solid").pack(fill="x", padx=16, ipady=7)

        self.err = tk.Label(form, text="", font=("Segoe UI", 9),
                            bg=CARD, fg=DANGER)
        self.err.pack(pady=4)

        tk.Button(form, text="Confirm & Start", font=FONT_B,
                  bg=PRIMARY, fg="white", bd=0, cursor="hand2",
                  command=self.save).pack(fill="x", padx=16, pady=(0, 16), ipady=10)

    def save(self):
        bank    = self.bank_var.get().strip()
        balance = self.balance_var.get().strip().replace(",", "")
        if not bank:
            self.err.config(text="Please enter bank name")
            return
        try:
            balance = float(balance)
            if balance < 0:
                raise ValueError
        except ValueError:
            self.err.config(text="Invalid balance (must be >= 0)")
            return

        db = Database()
        try:
            db.execute(
                "INSERT INTO BANKACCOUNTS (UserID, BankName, Balance) "
                "VALUES (%s, %s, %s)",
                (self.user["UserID"], bank, balance)
            )
            messagebox.showinfo("Success", f"Added {bank} account!")
            self.win.destroy()
            self.on_done()
        except Exception as e:
            self.err.config(text=f"Error: {e}")
        finally:
            db.close()


# ════════════════════════════════════════════════════════════════
#  ADD BANK ACCOUNT DIALOG (used in MainApp)
# ════════════════════════════════════════════════════════════════
class AddBankDialog:
    def __init__(self, parent, user_id, on_done):
        self.user_id = user_id
        self.on_done = on_done
        self.win = tk.Toplevel(parent)
        self.win.title("Add Bank Account")
        self.win.geometry("400x300")
        self.win.configure(bg=BG)
        self.win.resizable(False, False)
        self.win.grab_set()
        self._build_ui()

    def _build_ui(self):
        tk.Label(self.win, text="Add Bank Account",
                 font=FONT_H, bg=BG, fg=TEXT).pack(pady=20)

        form = tk.Frame(self.win, bg=CARD)
        form.pack(fill="x", padx=24)

        tk.Label(form, text="Bank Name *", font=FONT_B,
                 bg=CARD, fg=TEXT).pack(anchor="w", padx=16, pady=(14, 2))
        self.bank_var = tk.StringVar()
        banks = ["Vietcombank", "BIDV", "VPBank", "Agribank", "MB Bank",
                 "Techcombank", "Vietinbank", "TPBank", "ACB", "SHB", "Other"]
        ttk.Combobox(form, textvariable=self.bank_var, values=banks,
                     font=FONT, state="normal").pack(
            fill="x", padx=16, ipady=5)

        tk.Label(form, text="Current Balance (VND) *", font=FONT_B,
                 bg=CARD, fg=TEXT).pack(anchor="w", padx=16, pady=(10, 2))
        self.balance_var = tk.StringVar(value="0")
        tk.Entry(form, textvariable=self.balance_var, font=FONT,
                 bd=1, relief="solid").pack(fill="x", padx=16, ipady=7)

        self.err = tk.Label(form, text="", font=("Segoe UI", 9),
                            bg=CARD, fg=DANGER)
        self.err.pack(pady=4)

        tk.Button(form, text="+ Add Account", font=FONT_B,
                  bg=SUCCESS, fg="white", bd=0, cursor="hand2",
                  command=self.save).pack(fill="x", padx=16, pady=(0, 16), ipady=9)

    def save(self):
        bank    = self.bank_var.get().strip()
        balance = self.balance_var.get().strip().replace(",", "")
        if not bank:
            self.err.config(text="Please enter bank name")
            return
        try:
            balance = float(balance)
            if balance < 0:
                raise ValueError
        except ValueError:
            self.err.config(text="Invalid balance (must be >= 0)")
            return
        db = Database()
        try:
            db.execute(
                "INSERT INTO BANKACCOUNTS (UserID, BankName, Balance) "
                "VALUES (%s, %s, %s)",
                (self.user_id, bank, balance)
            )
            messagebox.showinfo("Success", f"Added {bank} account!")
            self.win.destroy()
            self.on_done()
        except Exception as e:
            self.err.config(text=f"Error: {e}")
        finally:
            db.close()


# ════════════════════════════════════════════════════════════════
#  MAIN APP
# ════════════════════════════════════════════════════════════════
class MainApp:
    def __init__(self, root, user):
        self.root    = root
        self.user    = user
        self.user_id = user["UserID"]
        self.root.title("Personal Finance Management System")
        self.root.geometry("1150x700")
        self.root.configure(bg=BG)
        self.root.resizable(True, True)
        self._center_window(1150, 700)
        self._build_layout()
        self._check_bank_accounts()

    def _center_window(self, w, h):
        sw = self.root.winfo_screenwidth()
        sh = self.root.winfo_screenheight()
        self.root.geometry(f"{w}x{h}+{(sw-w)//2}+{(sh-h)//2}")

    def _check_bank_accounts(self):
        db = Database()
        accounts = db.fetchall(
            "SELECT AccountID FROM BANKACCOUNTS WHERE UserID=%s",
            (self.user_id,))
        db.close()
        if not accounts:
            SetupBankWindow(self.root, self.user,
                            on_done=self.show_dashboard)
        else:
            self.show_dashboard()

    def _build_layout(self):
        self.sidebar = tk.Frame(self.root, bg=SIDEBAR, width=210)
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)

        tk.Label(self.sidebar, text="💰 Finance",
                 font=("Segoe UI", 14, "bold"),
                 bg=SIDEBAR, fg="white").pack(pady=(24, 4))
        tk.Label(self.sidebar,
                 text=f"Hello, {self.user['UserName'].split()[0]}",
                 font=("Segoe UI", 9), bg=SIDEBAR, fg=MUTED).pack(pady=(0, 20))
        tk.Frame(self.sidebar, bg="#2E3F52", height=1).pack(fill="x", padx=16)

        self.nav_buttons = {}
        nav_items = [
            ("Dashboard",  "🏠  Dashboard",      self.show_dashboard),
            ("Income",     "💵  Income",         self.show_income),
            ("Expense",    "💸  Expense",        self.show_expense),
            ("Accounts",   "🏦  Accounts",       self.show_accounts),
            ("Reports",    "📊  Reports",        self.show_reports),
        ]
        for key, label, cmd in nav_items:
            btn = tk.Button(
                self.sidebar, text=label, font=("Segoe UI", 10),
                bd=0, bg=SIDEBAR, fg="#B0BEC5",
                activebackground="#2E3F52", activeforeground="white",
                anchor="w", padx=20, cursor="hand2",
                command=lambda k=key, c=cmd: self._nav(c, k)
            )
            btn.pack(fill="x", ipady=10)
            self.nav_buttons[key] = btn

        tk.Frame(self.sidebar, bg="#2E3F52", height=1).pack(
            fill="x", padx=16, side="bottom", pady=10)
        tk.Button(
            self.sidebar, text="🚪  Logout",
            font=("Segoe UI", 10), bd=0, bg=SIDEBAR, fg=DANGER,
            activebackground="#2E3F52", anchor="w", padx=20, cursor="hand2",
            command=self.logout
        ).pack(fill="x", ipady=10, side="bottom")

        self.content = tk.Frame(self.root, bg=BG)
        self.content.pack(side="left", fill="both", expand=True)

    def _nav(self, cmd, key):
        for k, btn in self.nav_buttons.items():
            btn.config(bg=SIDEBAR, fg="#B0BEC5")
        self.nav_buttons[key].config(bg="#2E3F52", fg="white")
        try:
            cmd()
        except Exception as e:
            self._clear_content()
            tk.Label(self.content, text=f"Error: {e}",
                     font=FONT, bg=BG, fg=DANGER).pack(pady=40)
            print(f"ERROR in _nav [{key}]: {e}")

    def _clear_content(self):
        for w in self.content.winfo_children():
            w.destroy()

    def _page_title(self, title, subtitle=""):
        tk.Label(self.content, text=title, font=FONT_H,
                 bg=BG, fg=TEXT).pack(anchor="w", padx=24, pady=(20, 0))
        if subtitle:
            tk.Label(self.content, text=subtitle, font=("Segoe UI", 9),
                     bg=BG, fg=MUTED).pack(anchor="w", padx=24)

    def _card(self, parent, title, value, color=PRIMARY, emoji=""):
        f = tk.Frame(parent, bg=CARD, bd=0, relief="flat")
        f.pack(side="left", fill="both", expand=True, padx=8, pady=8)
        tk.Label(f, text=emoji, font=("Segoe UI", 20),
                 bg=CARD).pack(anchor="w", padx=16, pady=(14, 0))
        tk.Label(f, text=title, font=("Segoe UI", 9),
                 bg=CARD, fg=MUTED).pack(anchor="w", padx=16)
        tk.Label(f, text=value, font=("Segoe UI", 16, "bold"),
                 bg=CARD, fg=color).pack(anchor="w", padx=16, pady=(2, 14))
        return f

    def _get_accounts(self):
        db = Database()
        rows = db.fetchall(
            "SELECT AccountID, BankName, Balance FROM BANKACCOUNTS "
            "WHERE UserID=%s ORDER BY AccountID", (self.user_id,))
        db.close()
        return rows

    # ── DASHBOARD ────────────────────────────────────────────────
    def show_dashboard(self, month=None, year=None):
        # Lấy tháng/năm mặc định nếu không có
        if month is None or year is None:
            today = date.today()
            month = today.month
            year = today.year

        self._clear_content()
        self._page_title("Dashboard", f"Month {month}/{year}")

        # --- Frame chọn tháng/năm ---
        filter_frame = tk.Frame(self.content, bg=BG)
        filter_frame.pack(fill="x", padx=16, pady=(8, 4))

        tk.Label(filter_frame, text="Select month/year:", font=FONT_B, bg=BG, fg=TEXT).pack(side="left", padx=(0,8))

        # Combobox tháng
        self.month_var = tk.StringVar(value=str(month))
        month_cb = ttk.Combobox(filter_frame, textvariable=self.month_var,
                                values=[str(i) for i in range(1,13)], width=5, state="readonly")
        month_cb.pack(side="left", padx=2)

        # Combobox năm (từ 2020 đến năm sau)
        current_year = date.today().year
        years = [str(y) for y in range(2020, current_year+2)]
        self.year_var = tk.StringVar(value=str(year))
        year_cb = ttk.Combobox(filter_frame, textvariable=self.year_var,
                            values=years, width=6, state="readonly")
        year_cb.pack(side="left", padx=2)

        # Nút View
        view_btn = tk.Button(filter_frame, text="View",
                            command=lambda: self.show_dashboard(int(self.month_var.get()), int(self.year_var.get())),
                            bg=PRIMARY, fg="white", font=FONT_B, padx=10)
        view_btn.pack(side="left", padx=10)

        # --- Lấy dữ liệu từ DB ---
        db = Database()
        m, y = month, year

        income = float(db.fetchone(
            "SELECT IFNULL(SUM(Amount),0) AS v FROM INCOME "
            "WHERE UserID=%s AND MONTH(IncomeDate)=%s AND YEAR(IncomeDate)=%s",
            (self.user_id, m, y))["v"] or 0)
        expense = float(db.fetchone(
            "SELECT IFNULL(SUM(Amount),0) AS v FROM EXPENSES "
            "WHERE UserID=%s AND MONTH(ExpenseDate)=%s AND YEAR(ExpenseDate)=%s",
            (self.user_id, m, y))["v"] or 0)

        balance_now = float(db.fetchone(
            "SELECT IFNULL(SUM(Balance),0) AS v FROM BANKACCOUNTS "
            "WHERE UserID=%s", (self.user_id,))["v"] or 0)

        # Số dư đầu tháng = số dư hiện tại - thu nhập tháng này + chi tiêu tháng này
        balance_start = balance_now - income + expense
        db.close()

        savings = income - expense

        # --- Hiển thị các card ---
        cards = tk.Frame(self.content, bg=BG)
        cards.pack(fill="x", padx=16, pady=(12, 0))
        self._card(cards, "This month income",  f"{income:,.0f} VND",   SUCCESS, "💵")
        self._card(cards, "This month expense", f"{expense:,.0f} VND",  DANGER,  "💸")
        color = SUCCESS if savings >= 0 else DANGER
        self._card(cards, "This month savings", f"{savings:,.0f} VND",  color,   "💰")

        # --- Balance start và current balance ---
        bal_row = tk.Frame(self.content, bg=BG)
        bal_row.pack(fill="x", padx=16, pady=(0, 4))

        f1 = tk.Frame(bal_row, bg=CARD)
        f1.pack(side="left", fill="both", expand=True, padx=8, pady=4)
        tk.Label(f1, text="📅  Balance at start of month", font=FONT_B,
                bg=CARD, fg=MUTED).pack(anchor="w", padx=16, pady=(12, 0))
        tk.Label(f1, text=f"1/{m}/{y}",
                font=("Segoe UI", 8), bg=CARD, fg=MUTED).pack(anchor="w", padx=16)
        tk.Label(f1, text=f"{balance_start:,.0f} VND",
                font=("Segoe UI", 18, "bold"), bg=CARD, fg=TEXT).pack(
            anchor="w", padx=16, pady=(2, 12))

        tk.Label(bal_row, text="→", font=("Segoe UI", 20),
                bg=BG, fg=MUTED).pack(side="left")

        f2 = tk.Frame(bal_row, bg=PRIMARY)
        f2.pack(side="left", fill="both", expand=True, padx=8, pady=4)
        tk.Label(f2, text="💳  Current balance", font=FONT_B,
                bg=PRIMARY, fg="white").pack(anchor="w", padx=16, pady=(12, 0))
        today_str = date.today().strftime("%Y-%m-%d")
        tk.Label(f2, text=today_str,
                font=("Segoe UI", 8), bg=PRIMARY, fg="#cce0ff").pack(anchor="w", padx=16)
        tk.Label(f2, text=f"{balance_now:,.0f} VND",
                font=("Segoe UI", 18, "bold"), bg=PRIMARY, fg="white").pack(
            anchor="w", padx=16, pady=(2, 12))

        diff = balance_now - balance_start
        diff_color = SUCCESS if diff >= 0 else DANGER
        diff_sign = "▲" if diff >= 0 else "▼"
        tk.Label(bal_row,
                text=f"{diff_sign} {abs(diff):,.0f} VND\nvs start of month",
                font=("Segoe UI", 9, "bold"), bg=BG, fg=diff_color,
                justify="center").pack(side="left", padx=8)

        # --- Biểu đồ 6 tháng ---
        tk.Label(self.content, text="Income & Expense (last 6 months)",
                font=FONT_B, bg=BG, fg=TEXT).pack(anchor="w", padx=24, pady=(12, 4))
        self._draw_mini_chart(month, year)

    def _draw_mini_chart(self, base_month=None, base_year=None):
        # Nếu không có tham số, lấy tháng hiện tại làm mốc
        if base_month is None or base_year is None:
            today = date.today()
            base_month = today.month
            base_year = today.year

        # Tạo danh sách 6 tháng liên tiếp (tháng cuối là base_month/base_year)
        months_data = []
        for i in range(5, -1, -1):
            m = base_month - i
            y = base_year
            if m <= 0:
                m += 12
                y -= 1
            months_data.append((y, m))

        db = Database()
        inc_exp = []
        for y, m in months_data:
            inc = db.fetchone(
                "SELECT IFNULL(SUM(Amount),0) AS s FROM INCOME "
                "WHERE UserID=%s AND YEAR(IncomeDate)=%s AND MONTH(IncomeDate)=%s",
                (self.user_id, y, m))["s"]
            exp = db.fetchone(
                "SELECT IFNULL(SUM(Amount),0) AS s FROM EXPENSES "
                "WHERE UserID=%s AND YEAR(ExpenseDate)=%s AND MONTH(ExpenseDate)=%s",
                (self.user_id, y, m))["s"]
            inc_exp.append((inc, exp))
        db.close()

        # Tạo figure mới
        fig = Figure(figsize=(8, 2.8), dpi=100, facecolor=BG)
        ax = fig.add_subplot(111)
        ax.set_facecolor(BG)

        if months_data:
            labels = [f"{m}/{y}" for y, m in months_data]
            inc = [float(ie[0]) for ie in inc_exp]
            exp = [float(ie[1]) for ie in inc_exp]
            x = range(len(labels))

            ax.bar([i - 0.2 for i in x], inc, width=0.38,
                color=SUCCESS, label="Income", alpha=0.85)
            ax.bar([i + 0.2 for i in x], exp, width=0.38,
                color=DANGER,  label="Expense",  alpha=0.85)
            ax.set_xticks(list(x))
            ax.set_xticklabels(labels, fontsize=8)
            ax.yaxis.set_major_formatter(
                plt.FuncFormatter(lambda v, _: f"{v/1e6:.1f}M"))
            ax.legend(fontsize=8)

        ax.spines[["top", "right"]].set_visible(False)
        fig.tight_layout(pad=1.5)

        # Xóa canvas cũ (nếu có) để tránh chồng lấn
        for widget in self.content.winfo_children():
            if isinstance(widget, FigureCanvasTkAgg):
                widget.destroy()

        canvas = FigureCanvasTkAgg(fig, master=self.content)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="x", padx=24)

    # ── INCOME ───────────────────────────────────────────────────
    def show_income(self):
        self._clear_content()
        self._page_title("Income", "Manage your income")

        accounts = self._get_accounts()
        if not accounts:
            tk.Label(self.content,
                     text="⚠️ You don't have any bank account.\nPlease add an account first.",
                     font=FONT_B, bg=BG, fg=WARNING).pack(pady=40)
            return

        acc_labels = [f"{a['BankName']}  (Balance: {float(a['Balance']):,.0f} VND)"
                      for a in accounts]
        self._acc_map_inc = {lbl: a["AccountID"] for lbl, a in zip(acc_labels, accounts)}

        form = tk.Frame(self.content, bg=CARD)
        form.pack(fill="x", padx=24, pady=12)
        tk.Label(form, text="Add new income", font=FONT_B,
                 bg=CARD, fg=TEXT).grid(
            row=0, column=0, columnspan=6, sticky="w", padx=12, pady=(10, 6))

        tk.Label(form, text="Bank Account", font=FONT,
                 bg=CARD, fg=MUTED).grid(row=1, column=0, padx=12, sticky="w")
        self.inc_acc = ttk.Combobox(form, values=acc_labels, font=FONT,
                                    width=30, state="readonly")
        self.inc_acc.grid(row=1, column=1, padx=8, ipady=4)
        self.inc_acc.current(0)

        tk.Label(form, text="Amount (VND)", font=FONT,
                 bg=CARD, fg=MUTED).grid(row=1, column=2, padx=8, sticky="w")
        self.inc_amount = tk.Entry(form, font=FONT, bd=1, relief="solid", width=16)
        self.inc_amount.grid(row=1, column=3, padx=8, ipady=5)

        tk.Label(form, text="Date (YYYY-MM-DD)", font=FONT,
                 bg=CARD, fg=MUTED).grid(row=2, column=0, padx=12, pady=(6,4), sticky="w")
        self.inc_date = tk.Entry(form, font=FONT, bd=1, relief="solid", width=14)
        self.inc_date.insert(0, str(date.today()))
        self.inc_date.grid(row=2, column=1, padx=8, ipady=5, sticky="w")

        tk.Label(form, text="Description", font=FONT,
                 bg=CARD, fg=MUTED).grid(row=2, column=2, padx=8, sticky="w")
        self.inc_desc = tk.Entry(form, font=FONT, bd=1, relief="solid", width=24)
        self.inc_desc.grid(row=2, column=3, padx=8, ipady=5)

        tk.Button(form, text="+ Add", font=FONT_B,
                  bg=SUCCESS, fg="white", bd=0, cursor="hand2",
                  padx=16, command=self.add_income_action).grid(
            row=2, column=4, padx=12, ipady=6)
        tk.Frame(form, bg=BG, height=8).grid(row=3, column=0)

        self._income_table()

    def _income_table(self):
        frame = tk.Frame(self.content, bg=CARD)
        frame.pack(fill="both", expand=True, padx=24, pady=(0, 16))

        # Cột: ID (ẩn), No., Bank, Amount, Date, Description, Delete
        cols = ("ID", "No.", "Bank", "Amount", "Date", "Description", "")
        widths = [0, 50, 140, 150, 120, 280, 80]   # ID rộng 0 => ẩn
        tree = ttk.Treeview(frame, columns=cols, show="headings", height=12)
        style = ttk.Style()
        style.configure("Treeview",
                        background=CARD, fieldbackground=CARD,
                        foreground=TEXT, font=FONT, rowheight=32)
        style.configure("Treeview.Heading", font=FONT_B, foreground=TEXT)

        for col, w in zip(cols, widths):
            if col == "ID":
                # Ẩn cột ID triệt để
                tree.column(col, width=0, minwidth=0, stretch=False)
                tree.heading(col, text="")   # không hiển thị tiêu đề
            else:
                tree.heading(col, text=col if col != "" else "")
                tree.column(col, width=w, anchor="center" if col in ("No.", "") else "w")

        tree.heading("No.", text="No.") 

        db = Database()
        rows = db.fetchall(
            "SELECT i.IncomeID, b.BankName, i.Amount, i.IncomeDate, i.Description "
            "FROM INCOME i JOIN BANKACCOUNTS b ON i.AccountID = b.AccountID "
            "WHERE i.UserID=%s ORDER BY i.IncomeDate DESC",
            (self.user_id,))
        db.close()

        for idx, r in enumerate(rows, start=1):
            tree.insert("", "end", values=(
                r["IncomeID"],           # ID thật (cột 0, ẩn)
                idx,                     # No.
                r["BankName"],
                f"{float(r['Amount']):,.0f} VND",
                str(r["IncomeDate"]),
                r["Description"],
                "🗑 Delete"
            ))
        tree.pack(fill="both", expand=True)
        tree.bind("<ButtonRelease-1>", lambda e: self._delete_income(tree))

    def add_income_action(self):
        try:
            acc_label = self.inc_acc.get()
            account_id = self._acc_map_inc[acc_label]
            amount = float(self.inc_amount.get().replace(",", ""))
            if amount <= 0:
                raise ValueError("Amount must be > 0")
            date_str = self.inc_date.get().strip() or str(date.today())
            desc = self.inc_desc.get().strip() or ""
            datetime.strptime(date_str, "%Y-%m-%d")

            db = Database()
            result = db.call_procedure("sp_add_income",
                (self.user_id, account_id, amount, date_str, desc))
            db.close()

            if result and "Error" in str(result[0]):
                messagebox.showerror("Error", str(result[0]))
            else:
                db2 = Database()
                new_bal = db2.fetchone(
                    "SELECT Balance FROM BANKACCOUNTS WHERE AccountID=%s",
                    (account_id,))["Balance"]
                db2.close()
                messagebox.showinfo(
                    "Success",
                    f"✅ Added income: {amount:,.0f} VND\nNew balance: {float(new_bal):,.0f} VND"
                )
                self.inc_amount.delete(0, "end")
                self.inc_desc.delete(0, "end")
                self.show_income()
        except ValueError as ve:
            messagebox.showerror("Error", f"Invalid data: {ve}")

    def _delete_income(self, tree):
        item = tree.selection()
        if not item:
            return
        col = tree.identify_column(tree.winfo_pointerx() - tree.winfo_rootx())
        if col != "#6":
            return
        iid = tree.item(item)["values"][0]
        if messagebox.askyesno("Confirm", f"Delete income ID {iid}?"):
            db = Database()
            db.execute("DELETE FROM INCOME WHERE IncomeID=%s", (iid,))
            db.close()
            self.show_income()

    # ── EXPENSE ──────────────────────────────────────────────────
    def show_expense(self):
        self._clear_content()
        self._page_title("Expense", "Manage your expenses")

        accounts = self._get_accounts()
        if not accounts:
            tk.Label(self.content,
                     text="⚠️ You don't have any bank account.\nPlease add an account first.",
                     font=FONT_B, bg=BG, fg=WARNING).pack(pady=40)
            return

        acc_labels = [f"{a['BankName']}  (Balance: {float(a['Balance']):,.0f} VND)"
                      for a in accounts]
        self._acc_map_exp = {lbl: a["AccountID"] for lbl, a in zip(acc_labels, accounts)}

        db = Database()
        cats = db.fetchall("SELECT * FROM EXPENSECATEGORIES")
        db.close()
        cat_names = [c["CategoryName"] for c in cats]
        self._cat_map = {c["CategoryName"]: c["CategoryID"] for c in cats}

        form = tk.Frame(self.content, bg=CARD)
        form.pack(fill="x", padx=24, pady=12)
        tk.Label(form, text="Add new expense", font=FONT_B,
                 bg=CARD, fg=TEXT).grid(
            row=0, column=0, columnspan=8, sticky="w", padx=12, pady=(10, 6))

        tk.Label(form, text="Bank Account", font=FONT,
                 bg=CARD, fg=MUTED).grid(row=1, column=0, padx=12, sticky="w")
        self.exp_acc = ttk.Combobox(form, values=acc_labels, font=FONT,
                                    width=28, state="readonly")
        self.exp_acc.grid(row=1, column=1, padx=8, ipady=4)
        self.exp_acc.current(0)

        tk.Label(form, text="Category", font=FONT,
                 bg=CARD, fg=MUTED).grid(row=1, column=2, padx=8, sticky="w")
        self.exp_cat = ttk.Combobox(form, values=cat_names, font=FONT,
                                    width=16, state="readonly")
        self.exp_cat.grid(row=1, column=3, padx=8, ipady=4)
        self.exp_cat.current(0)

        tk.Label(form, text="Amount (VND)", font=FONT,
                 bg=CARD, fg=MUTED).grid(row=2, column=0, padx=12, pady=(6,4), sticky="w")
        self.exp_amount = tk.Entry(form, font=FONT, bd=1, relief="solid", width=16)
        self.exp_amount.grid(row=2, column=1, padx=8, ipady=5, sticky="w")

        tk.Label(form, text="Date (YYYY-MM-DD)", font=FONT,
                 bg=CARD, fg=MUTED).grid(row=2, column=2, padx=8, sticky="w")
        self.exp_date = tk.Entry(form, font=FONT, bd=1, relief="solid", width=14)
        self.exp_date.insert(0, str(date.today()))
        self.exp_date.grid(row=2, column=3, padx=8, ipady=5)

        tk.Label(form, text="Description", font=FONT,
                 bg=CARD, fg=MUTED).grid(row=2, column=4, padx=8, sticky="w")
        self.exp_desc = tk.Entry(form, font=FONT, bd=1, relief="solid", width=20)
        self.exp_desc.grid(row=2, column=5, padx=8, ipady=5)

        tk.Button(form, text="+ Add", font=FONT_B,
                  bg=DANGER, fg="white", bd=0, cursor="hand2",
                  padx=16, command=self.add_expense_action).grid(
            row=2, column=6, padx=12, ipady=6)
        tk.Frame(form, bg=BG, height=8).grid(row=3, column=0)

        self._expense_table()

    def _expense_table(self):
        frame = tk.Frame(self.content, bg=CARD)
        frame.pack(fill="both", expand=True, padx=24, pady=(0, 16))

        cols = ("ID", "No.", "Bank", "Category", "Amount", "Date", "Description", "")
        widths = [0, 50, 120, 120, 130, 110, 230, 80]
        tree = ttk.Treeview(frame, columns=cols, show="headings", height=11)
        style = ttk.Style()
        style.configure("Treeview", rowheight=32)
        style.configure("Treeview.Heading", font=FONT_B)

        for col, w in zip(cols, widths):
            if col == "ID":
                tree.column(col, width=0, minwidth=0, stretch=False)
                tree.heading(col, text="")
            else:
                tree.heading(col, text=col if col != "" else "")
                tree.column(col, width=w, anchor="center" if col in ("No.", "") else "w")

        tree.heading("No.", text="No.")

        db = Database()
        rows = db.fetchall(
            "SELECT e.ExpenseID, b.BankName, c.CategoryName, e.Amount, "
            "e.ExpenseDate, e.Description "
            "FROM EXPENSES e "
            "JOIN BANKACCOUNTS b ON e.AccountID = b.AccountID "
            "JOIN EXPENSECATEGORIES c ON e.CategoryID = c.CategoryID "
            "WHERE e.UserID=%s ORDER BY e.ExpenseDate DESC",
            (self.user_id,))
        db.close()

        for idx, r in enumerate(rows, start=1):
            tree.insert("", "end", values=(
                r["ExpenseID"],          # ID thật (cột 0, ẩn)
                idx,
                r["BankName"],
                r["CategoryName"],
                f"{float(r['Amount']):,.0f} VND",
                str(r["ExpenseDate"]),
                r["Description"],
                "🗑 Delete"
            ))
        tree.pack(fill="both", expand=True)
        tree.bind("<ButtonRelease-1>", lambda e: self._delete_expense(tree))

    def add_expense_action(self):
        try:
            acc_label  = self.exp_acc.get()
            account_id = self._acc_map_exp[acc_label]
            cat_name   = self.exp_cat.get()
            cat_id     = self._cat_map[cat_name]
            amount     = float(self.exp_amount.get().replace(",", ""))
            if amount <= 0:
                raise ValueError("Amount must be > 0")
            date_str = self.exp_date.get().strip() or str(date.today())
            desc     = self.exp_desc.get().strip() or ""
            datetime.strptime(date_str, "%Y-%m-%d")

            db = Database()
            ok = db.fetchone(
                "SELECT fn_sufficient_balance(%s, %s) AS ok",
                (account_id, amount))["ok"]
            db.close()

            if not ok:
                db2 = Database()
                bal = db2.fetchone(
                    "SELECT Balance, BankName FROM BANKACCOUNTS WHERE AccountID=%s",
                    (account_id,))
                db2.close()
                ans = messagebox.askyesno(
                    "Insufficient balance",
                    f"Account {bal['BankName']} has only {float(bal['Balance']):,.0f} VND.\n"
                    f"Cannot spend {amount:,.0f} VND.\n\nDo you want to choose another account?"
                )
                if ans:
                    self.exp_acc.focus_set()
                return

            db3 = Database()
            result = db3.call_procedure("sp_add_expense",
                (self.user_id, account_id, cat_id, amount, date_str, desc))
            db3.close()

            if result and ("Insufficient" in str(result[0]) or "Error" in str(result[0])):
                messagebox.showwarning("Warning", str(result[0]))
            else:
                db4 = Database()
                new_bal = db4.fetchone(
                    "SELECT Balance FROM BANKACCOUNTS WHERE AccountID=%s",
                    (account_id,))["Balance"]
                db4.close()
                messagebox.showinfo(
                    "Success",
                    f"✅ Added expense: {amount:,.0f} VND\nRemaining balance: {float(new_bal):,.0f} VND"
                )
                self.exp_amount.delete(0, "end")
                self.exp_desc.delete(0, "end")
                self.show_expense()
        except ValueError as ve:
            messagebox.showerror("Error", f"Invalid data: {ve}")

    def _delete_expense(self, tree):
        item = tree.selection()
        if not item:
            return
        col = tree.identify_column(tree.winfo_pointerx() - tree.winfo_rootx())
        if col != "#7":
            return
        eid = tree.item(item)["values"][0]
        if messagebox.askyesno("Confirm", f"Delete expense ID {eid}?"):
            db = Database()
            db.execute("DELETE FROM EXPENSES WHERE ExpenseID=%s", (eid,))
            db.close()
            self.show_expense()

    # ── ACCOUNTS ─────────────────────────────────────────────────
    def show_accounts(self):
        self._clear_content()
        self._page_title("Bank Accounts", "Manage your account balances")

        db = Database()
        rows = db.fetchall(
            "SELECT AccountID, BankName, Balance "
            "FROM BANKACCOUNTS WHERE UserID=%s ORDER BY AccountID",
            (self.user_id,))
        total = sum(float(r["Balance"]) for r in rows)
        db.close()

        card = tk.Frame(self.content, bg=PRIMARY)
        card.pack(fill="x", padx=24, pady=(12, 8))
        tk.Label(card, text="Total balance across all accounts",
                 font=FONT, bg=PRIMARY, fg="white").pack(pady=(12, 0))
        tk.Label(card, text=f"{total:,.0f} VND",
                 font=("Segoe UI", 24, "bold"),
                 bg=PRIMARY, fg="white").pack(pady=(0, 12))

        for r in rows:
            f = tk.Frame(self.content, bg=CARD)
            f.pack(fill="x", padx=24, pady=4)
            tk.Label(f, text="🏦", font=("Segoe UI", 18),
                     bg=CARD).pack(side="left", padx=16, pady=12)
            tk.Label(f, text=r["BankName"], font=FONT_B,
                     bg=CARD, fg=TEXT).pack(side="left")
            tk.Label(f, text=f"{float(r['Balance']):,.0f} VND",
                     font=FONT_B, bg=CARD, fg=SUCCESS).pack(side="right", padx=20)

        tk.Button(self.content, text="+ Add Bank Account",
                  font=FONT_B, bg=PRIMARY, fg="white", bd=0,
                  cursor="hand2", padx=20,
                  command=lambda: AddBankDialog(
                      self.root, self.user_id,
                      on_done=self.show_accounts
                  )).pack(pady=16, ipady=8)

    # ── REPORTS ──────────────────────────────────────────────────
    def show_reports(self):
        self._clear_content()
        self._page_title("Financial Reports", "Detailed analysis of income and expense")

        tab_frame = tk.Frame(self.content, bg=BG)
        tab_frame.pack(fill="x", padx=24, pady=(12, 0))

        self.report_content = tk.Frame(self.content, bg=BG)
        self.report_content.pack(fill="both", expand=True)

        self._report_tabs = {}
        tabs = [
            ("Summary",        self._report_summary),
            ("By Category",    self._report_by_category),
            ("Trend",          self._report_trend),
            ("Alerts",         self._report_alert),
            ("Balance History", self._report_balance_history),
        ]
        for name, fn in tabs:
            btn = tk.Button(tab_frame, text=name, font=FONT_B,
                            bg=CARD, fg=TEXT, bd=1, relief="solid",
                            cursor="hand2", padx=12, pady=4,
                            command=lambda f=fn, n=name: self._switch_report(f, n))
            btn.pack(side="left", padx=4)
            self._report_tabs[name] = btn

        self._switch_report(self._report_summary, "Summary")

    def _switch_report(self, fn, name):
        for n, btn in self._report_tabs.items():
            btn.config(bg=CARD, fg=TEXT)
        self._report_tabs[name].config(bg=PRIMARY, fg="white")
        for w in self.report_content.winfo_children():
            w.destroy()
        fn()

    def _report_filter_bar(self, parent):
        bar = tk.Frame(parent, bg=BG)
        bar.pack(fill="x", padx=0, pady=(8, 4))
        tk.Label(bar, text="Month:", font=FONT, bg=BG, fg=TEXT).pack(side="left", padx=(0,4))
        month_var = tk.StringVar(value=str(date.today().month))
        ttk.Combobox(bar, textvariable=month_var,
                     values=[str(i) for i in range(1, 13)],
                     width=4, state="readonly").pack(side="left")
        tk.Label(bar, text="Year:", font=FONT, bg=BG, fg=TEXT).pack(side="left", padx=(12,4))
        year_var = tk.StringVar(value=str(date.today().year))
        ttk.Combobox(bar, textvariable=year_var,
                     values=[str(y) for y in range(2022, date.today().year + 2)],
                     width=6, state="readonly").pack(side="left")
        return bar, month_var, year_var

    def _report_summary(self):
        f = self.report_content
        bar, month_var, year_var = self._report_filter_bar(f)

        result_frame = tk.Frame(f, bg=BG)
        result_frame.pack(fill="both", expand=True)

        def load(month_var=month_var, year_var=year_var, rf=result_frame):
            for w in rf.winfo_children():
                w.destroy()
            m = int(month_var.get())
            y = int(year_var.get())
            db = Database()
            income  = float(db.fetchone(
                "SELECT fn_total_income_by_user(%s,%s,%s) AS v",
                (self.user_id, m, y))["v"] or 0)
            expense = float(db.fetchone(
                "SELECT fn_total_expense_by_user(%s,%s,%s) AS v",
                (self.user_id, m, y))["v"] or 0)
            status  = db.fetchone(
                "SELECT fn_budget_status_by_user(%s,%s,%s) AS v",
                (self.user_id, m, y))["v"] or "N/A"
            db.close()

            saving = income - expense
            cards = tk.Frame(rf, bg=BG)
            cards.pack(fill="x", padx=0, pady=8)
            self._card(cards, f"Total income {m}/{y}", f"{income:,.0f} VND", SUCCESS, "💵")
            self._card(cards, f"Total expense {m}/{y}", f"{expense:,.0f} VND", DANGER, "💸")
            color = SUCCESS if saving >= 0 else DANGER
            self._card(cards, "Savings", f"{saving:,.0f} VND", color, "💰")
            sc = SUCCESS if status == "Surplus" else (DANGER if status == "Deficit" else WARNING)
            self._card(cards, "Status", status, sc, "📊")

            ebf = tk.Frame(rf, bg=BG)
            ebf.pack(anchor="e", padx=8, pady=4)
            tk.Button(ebf, text="⬇ Export CSV", font=FONT, bg=SUCCESS, fg="white",
                      bd=0, cursor="hand2", padx=10,
                      command=lambda: self._export_summary_csv(m, y, income, expense, saving, status)
                      ).pack(side="left", padx=4, ipady=5)
            tk.Button(ebf, text="⬇ Export PDF", font=FONT, bg=DANGER, fg="white",
                      bd=0, cursor="hand2", padx=10,
                      command=lambda: self._export_summary_pdf(m, y, income, expense, saving, status)
                      ).pack(side="left", padx=4, ipady=5)

        tk.Button(bar, text="View", font=FONT_B, bg=PRIMARY, fg="white",
                  bd=0, cursor="hand2", padx=10,
                  command=load).pack(side="left", padx=12, ipady=4)
        load()

    def _report_by_category(self):
        f = self.report_content
        bar, month_var, year_var = self._report_filter_bar(f)

        result_frame = tk.Frame(f, bg=BG)
        result_frame.pack(fill="both", expand=True)

        def load(rf=result_frame):
            for w in rf.winfo_children():
                w.destroy()
            m = int(month_var.get())
            y = int(year_var.get())
            db = Database()
            rows = db.fetchall(
                "SELECT c.CategoryName, COUNT(e.ExpenseID) AS Cnt, "
                "SUM(e.Amount) AS Total, AVG(e.Amount) AS Avg "
                "FROM EXPENSES e "
                "JOIN EXPENSECATEGORIES c ON e.CategoryID=c.CategoryID "
                "WHERE e.UserID=%s AND MONTH(e.ExpenseDate)=%s AND YEAR(e.ExpenseDate)=%s "
                "GROUP BY c.CategoryName ORDER BY Total DESC",
                (self.user_id, m, y))
            db.close()

            if not rows:
                tk.Label(rf, text=f"No data for {m}/{y}",
                         font=FONT, bg=BG, fg=MUTED).pack(pady=30)
                return

            tbl = tk.Frame(rf, bg=CARD)
            tbl.pack(fill="x", padx=0, pady=8)
            cols = ("Category", "Transactions", "Total", "Avg/Transaction")
            widths = [180, 120, 160, 160]
            tree = ttk.Treeview(tbl, columns=cols, show="headings", height=min(len(rows), 10))
            for col, w in zip(cols, widths):
                tree.heading(col, text=col)
                tree.column(col, width=w, anchor="w" if col == "Category" else "center")
            for r in rows:
                tree.insert("", "end", values=(
                    r["CategoryName"], r["Cnt"],
                    f"{float(r['Total']):,.0f} VND",
                    f"{float(r['Avg']):,.0f} VND"
                ))
            tree.pack(fill="x")

            fig = Figure(figsize=(5, 3.5), dpi=90, facecolor=BG)
            ax  = fig.add_subplot(111)
            ax.set_facecolor(BG)
            labels = [r["CategoryName"] for r in rows]
            vals   = [float(r["Total"]) for r in rows]
            colors = ["#4F8EF7","#2ECC71","#E74C3C","#F39C12","#9B59B6",
                      "#1ABC9C","#E67E22","#E91E63","#00BCD4","#8BC34A"]
            wedges, _, autotexts = ax.pie(
                vals, labels=None, autopct="%1.1f%%",
                colors=colors[:len(vals)], startangle=140, pctdistance=0.75)
            ax.legend(wedges, labels, loc="lower center",
                      bbox_to_anchor=(0.5, -0.22), ncol=2,
                      fontsize=7, frameon=False)
            for at in autotexts:
                at.set_fontsize(7)
            ax.set_title(f"Expenses by category — {m}/{y}",
                         fontsize=9, fontweight="bold")
            fig.tight_layout(pad=1.5)
            canvas = FigureCanvasTkAgg(fig, master=rf)
            canvas.draw()
            canvas.get_tk_widget().pack(pady=6)

            ebf = tk.Frame(rf, bg=BG)
            ebf.pack(anchor="e", padx=8, pady=4)
            tk.Button(ebf, text="⬇ Export CSV", font=FONT, bg=SUCCESS, fg="white",
                      bd=0, cursor="hand2", padx=10,
                      command=lambda: self._export_category_csv(rows, m, y)
                      ).pack(side="left", padx=4, ipady=5)

        tk.Button(bar, text="View", font=FONT_B, bg=PRIMARY, fg="white",
                  bd=0, cursor="hand2", padx=10,
                  command=load).pack(side="left", padx=12, ipady=4)
        load()

    def _report_trend(self):
        f = self.report_content

        top = tk.Frame(f, bg=BG)
        top.pack(fill="x", padx=4, pady=(8, 4))
        tk.Label(top, text="Income/Expense trend", font=FONT_B,
                 bg=BG, fg=TEXT).pack(side="left")

        self._trend_mode  = tk.StringVar(value="6month")
        self._trend_btns  = {}

        btn_frame = tk.Frame(top, bg=BG)
        btn_frame.pack(side="right")

        modes = [
            ("1 week",    "1week"),
            ("3 months",  "3month"),
            ("6 months",  "6month"),
            ("12 months", "12month"),
        ]
        for label, key in modes:
            btn = tk.Button(
                btn_frame, text=label, font=("Segoe UI", 9),
                bd=1, relief="solid", cursor="hand2", padx=10, pady=3,
                command=lambda k=key: self._load_trend(k)
            )
            btn.pack(side="left", padx=3)
            self._trend_btns[key] = btn

        self._trend_chart_frame = tk.Frame(f, bg=BG)
        self._trend_chart_frame.pack(fill="both", expand=True)

        self._load_trend("6month")

    def _load_trend(self, mode):
        from datetime import timedelta

        colors_map = {
            "1week":   "1 week",
            "3month":  "3 months",
            "6month":  "6 months",
            "12month": "12 months",
        }
        for k, btn in self._trend_btns.items():
            if k == mode:
                btn.config(bg=PRIMARY, fg="white", relief="flat")
            else:
                btn.config(bg=CARD, fg=TEXT, relief="solid")

        for w in self._trend_chart_frame.winfo_children():
            w.destroy()

        cf = self._trend_chart_frame
        db = Database()

        if mode == "1week":
            today    = date.today()
            week_ago = today - timedelta(days=6)

            inc_rows = db.fetchall(
                "SELECT DATE(IncomeDate) AS d, SUM(Amount) AS v "
                "FROM INCOME WHERE UserID=%s AND IncomeDate >= %s "
                "GROUP BY DATE(IncomeDate) ORDER BY d",
                (self.user_id, str(week_ago)))
            exp_rows = db.fetchall(
                "SELECT DATE(ExpenseDate) AS d, SUM(Amount) AS v "
                "FROM EXPENSES WHERE UserID=%s AND ExpenseDate >= %s "
                "GROUP BY DATE(ExpenseDate) ORDER BY d",
                (self.user_id, str(week_ago)))
            db.close()

            inc_map = {str(r["d"]): float(r["v"]) for r in inc_rows}
            exp_map = {str(r["d"]): float(r["v"]) for r in exp_rows}
            labels   = [(week_ago + timedelta(days=i)).strftime("%d/%m") for i in range(7)]
            day_keys = [(week_ago + timedelta(days=i)).strftime("%Y-%m-%d") for i in range(7)]
            inc_vals = [inc_map.get(k, 0) for k in day_keys]
            exp_vals = [exp_map.get(k, 0) for k in day_keys]
            net_vals = [i - e for i, e in zip(inc_vals, exp_vals)]
            title    = "Trend – last 7 days (daily)"
            use_bar  = True
        else:
            limit = {"3month": 3, "6month": 6, "12month": 12}[mode]
            rows = db.fetchall(
                "SELECT Month, Year, "
                "SUM(TotalIncome) AS Inc, SUM(TotalExpense) AS Exp "
                "FROM vw_monthly_summary_by_account "
                "WHERE UserID=%s "
                "GROUP BY Year, Month "
                "ORDER BY Year DESC, Month DESC LIMIT %s",
                (self.user_id, limit))
            db.close()
            rows     = list(reversed(rows))
            labels   = [f"{r['Month']}/{r['Year']}" for r in rows]
            inc_vals = [float(r["Inc"]) for r in rows]
            exp_vals = [float(r["Exp"]) for r in rows]
            net_vals = [i - e for i, e in zip(inc_vals, exp_vals)]
            title    = f"Trend – last {colors_map[mode]} (monthly)"
            use_bar  = False

        if not any(inc_vals) and not any(exp_vals):
            tk.Label(cf, text="No data for this period.",
                     font=FONT, bg=BG, fg=MUTED).pack(pady=30)
            return

        tk.Label(cf, text=title, font=("Segoe UI", 9),
                 bg=BG, fg=MUTED).pack(anchor="w", padx=4, pady=(2, 0))

        fig = Figure(figsize=(9, 3.8), dpi=95, facecolor=BG)
        ax  = fig.add_subplot(111)
        ax.set_facecolor(BG)
        x = list(range(len(labels)))

        if use_bar:
            w = 0.3
            ax.bar([i - w for i in x], inc_vals, width=w,
                   color=SUCCESS, label="Income", alpha=0.85)
            ax.bar(x,                  exp_vals, width=w,
                   color=DANGER,  label="Expense",  alpha=0.85)
            ax.plot(x, net_vals, color=PRIMARY, marker="s",
                    label="Savings", linewidth=1.5, linestyle="--")
        else:
            ax.plot(x, inc_vals, color=SUCCESS, marker="o",
                    label="Income", linewidth=2)
            ax.plot(x, exp_vals, color=DANGER,  marker="o",
                    label="Expense",  linewidth=2)
            ax.plot(x, net_vals, color=PRIMARY, marker="s",
                    label="Savings", linewidth=1.5, linestyle="--")

        ax.axhline(0, color=MUTED, linewidth=0.8, linestyle=":")
        ax.fill_between(x, net_vals, 0,
                        where=[v >= 0 for v in net_vals],
                        alpha=0.1, color=SUCCESS)
        ax.fill_between(x, net_vals, 0,
                        where=[v < 0 for v in net_vals],
                        alpha=0.1, color=DANGER)
        ax.set_xticks(x)
        ax.set_xticklabels(labels, fontsize=8, rotation=20 if len(labels) > 6 else 0)
        ax.yaxis.set_major_formatter(
            plt.FuncFormatter(lambda v, _: f"{v/1e6:.1f}M" if abs(v) >= 1e6 else f"{v/1e3:.0f}K"))
        ax.legend(fontsize=8)
        ax.spines[["top", "right"]].set_visible(False)
        fig.tight_layout(pad=1.5)

        canvas = FigureCanvasTkAgg(fig, master=cf)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="x", padx=4)

        summary = tk.Frame(cf, bg=BG)
        summary.pack(fill="x", padx=4, pady=(4, 0))
        total_inc = sum(inc_vals)
        total_exp = sum(exp_vals)
        total_net = total_inc - total_exp
        net_color = SUCCESS if total_net >= 0 else DANGER
        for label, val, color in [
            ("Total income", total_inc, SUCCESS),
            ("Total expense", total_exp, DANGER),
            ("Savings", total_net, net_color),
        ]:
            sf = tk.Frame(summary, bg=CARD)
            sf.pack(side="left", expand=True, fill="x", padx=4, pady=2)
            tk.Label(sf, text=label, font=("Segoe UI", 8),
                     bg=CARD, fg=MUTED).pack(anchor="w", padx=10, pady=(6, 0))
            tk.Label(sf, text=f"{val:,.0f} VND",
                     font=("Segoe UI", 11, "bold"),
                     bg=CARD, fg=color).pack(anchor="w", padx=10, pady=(0, 6))

        tk.Button(cf, text="⬇ Export CSV", font=FONT, bg=SUCCESS, fg="white",
                  bd=0, cursor="hand2", padx=10,
                  command=lambda: self._export_trend_csv_from_vals(
                      labels, inc_vals, exp_vals, net_vals, mode)
                  ).pack(anchor="e", padx=8, pady=6, ipady=5)

    def _report_alert(self):
        f = self.report_content
        tk.Label(f, text="Budget Alerts",
                 font=FONT_B, bg=BG, fg=TEXT).pack(anchor="w", padx=4, pady=(8, 4))

        db = Database()
        m, y = date.today().month, date.today().year

        low_bal = db.fetchall(
            "SELECT BankName, Balance FROM BANKACCOUNTS "
            "WHERE UserID=%s AND Balance < 1000000",
            (self.user_id,))

        deficit_months = db.fetchall(
            "SELECT Month, Year, SUM(TotalIncome) AS Inc, SUM(TotalExpense) AS Exp "
            "FROM vw_monthly_summary_by_account WHERE UserID=%s "
            "GROUP BY Year, Month "
            "HAVING Exp > Inc ORDER BY Year DESC, Month DESC LIMIT 6",
            (self.user_id,))

        top_cat = db.fetchall(
            "SELECT c.CategoryName, SUM(e.Amount) AS Total "
            "FROM EXPENSES e JOIN EXPENSECATEGORIES c ON e.CategoryID=c.CategoryID "
            "WHERE e.UserID=%s AND MONTH(e.ExpenseDate)=%s AND YEAR(e.ExpenseDate)=%s "
            "GROUP BY c.CategoryName ORDER BY Total DESC LIMIT 3",
            (self.user_id, m, y))
        db.close()

        section = tk.LabelFrame(f, text="⚠️ Low balance accounts (< 1,000,000 VND)",
                                 font=FONT_B, bg=BG, fg=WARNING, bd=1)
        section.pack(fill="x", padx=4, pady=6)
        if low_bal:
            for r in low_bal:
                tk.Label(section, text=f"🏦 {r['BankName']}: {float(r['Balance']):,.0f} VND",
                         font=FONT, bg=BG, fg=DANGER).pack(anchor="w", padx=12, pady=2)
        else:
            tk.Label(section, text="✅ All accounts have sufficient balance.",
                     font=FONT, bg=BG, fg=SUCCESS).pack(anchor="w", padx=12, pady=4)

        section2 = tk.LabelFrame(f, text="📉 Months with deficit (last 6)",
                                  font=FONT_B, bg=BG, fg=DANGER, bd=1)
        section2.pack(fill="x", padx=4, pady=6)
        if deficit_months:
            for r in deficit_months:
                diff = float(r["Exp"]) - float(r["Inc"])
                tk.Label(section2,
                         text=f"Month {r['Month']}/{r['Year']}: overspent by {diff:,.0f} VND",
                         font=FONT, bg=BG, fg=DANGER).pack(anchor="w", padx=12, pady=2)
        else:
            tk.Label(section2, text="✅ No deficit months found.",
                     font=FONT, bg=BG, fg=SUCCESS).pack(anchor="w", padx=12, pady=4)

        section3 = tk.LabelFrame(f, text=f"🔥 Top 3 expense categories this month ({m}/{y})",
                                  font=FONT_B, bg=BG, fg=TEXT, bd=1)
        section3.pack(fill="x", padx=4, pady=6)
        if top_cat:
            for i, r in enumerate(top_cat, 1):
                tk.Label(section3,
                         text=f"{i}. {r['CategoryName']}: {float(r['Total']):,.0f} VND",
                         font=FONT, bg=BG, fg=TEXT).pack(anchor="w", padx=12, pady=2)
        else:
            tk.Label(section3, text="No expenses recorded this month.",
                     font=FONT, bg=BG, fg=MUTED).pack(anchor="w", padx=12, pady=4)

    def _report_balance_history(self):
        f = self.report_content
        tk.Label(f, text="Account Balance History",
                 font=FONT_B, bg=BG, fg=TEXT).pack(anchor="w", padx=4, pady=(8, 4))

        db = Database()
        accounts = db.fetchall(
            "SELECT AccountID, BankName, Balance FROM BANKACCOUNTS "
            "WHERE UserID=%s", (self.user_id,))

        rows = db.fetchall(
            "SELECT 'income' AS type, AccountID, IncomeDate AS txDate, Amount "
            "FROM INCOME WHERE UserID=%s "
            "UNION ALL "
            "SELECT 'expense', AccountID, ExpenseDate, Amount "
            "FROM EXPENSES WHERE UserID=%s "
            "ORDER BY txDate",
            (self.user_id, self.user_id))
        db.close()

        tbl = tk.Frame(f, bg=CARD)
        tbl.pack(fill="x", padx=0, pady=6)
        cols = ("Date", "Type", "Bank", "Amount", "Note")
        tree = ttk.Treeview(tbl, columns=cols, show="headings", height=12)
        widths = [120, 90, 140, 150, 200]
        for col, w in zip(cols, widths):
            tree.heading(col, text=col)
            tree.column(col, width=w, anchor="center" if col != "Bank" else "w")

        acc_map = {a["AccountID"]: a["BankName"] for a in accounts}
        for r in reversed(rows):
            kind   = "Income" if r["type"] == "income" else "Expense"
            prefix = "+" if r["type"] == "income" else "-"
            tree.insert("", "end", values=(
                str(r["txDate"]), kind,
                acc_map.get(r["AccountID"], "?"),
                f"{prefix}{float(r['Amount']):,.0f} VND", ""
            ))
        tree.pack(fill="x")

        tk.Button(f, text="⬇ Export CSV History", font=FONT, bg=SUCCESS, fg="white",
                  bd=0, cursor="hand2", padx=10,
                  command=lambda: self._export_history_csv(rows, acc_map)
                  ).pack(anchor="e", padx=8, pady=6, ipady=5)

    # ════════════════════════════════════════════════════════════════
    #  EXPORT FUNCTIONS (English)
    # ════════════════════════════════════════════════════════════════
    def _get_export_path(self, filename):
        from tkinter import filedialog
        ext = os.path.splitext(filename)[1]
        if ext == ".csv":
            filetypes = [("CSV files", "*.csv"), ("All files", "*.*")]
        else:
            filetypes = [("PDF files", "*.pdf"), ("All files", "*.*")]
        path = filedialog.asksaveasfilename(
            initialfile=filename,
            defaultextension=ext,
            filetypes=filetypes,
            title="Save file as"
        )
        return path

    def _export_summary_csv(self, m, y, income, expense, saving, status):
        path = self._get_export_path(f"summary_{m}_{y}.csv")
        if not path:
            return
        try:
            with open(path, "w", newline="", encoding="utf-8-sig") as fh:
                w = csv.writer(fh)
                w.writerow(["Financial Summary Report"])
                w.writerow([f"Month {m}/{y}"])
                w.writerow([])
                w.writerow(["Item", "Value (VND)"])
                w.writerow(["Total Income", f"{income:,.0f}"])
                w.writerow(["Total Expense", f"{expense:,.0f}"])
                w.writerow(["Savings",     f"{saving:,.0f}"])
                w.writerow(["Status",      status])
            messagebox.showinfo("Export CSV", f"File saved:\n{path}")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def _export_summary_pdf(self, m, y, income, expense, saving, status):
        try:
            from reportlab.lib.pagesizes import A4
            from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
            from reportlab.lib import colors
            from reportlab.lib.styles import getSampleStyleSheet

            path = self._get_export_path(f"summary_{m}_{y}.pdf")
            if not path:
                return
            doc  = SimpleDocTemplate(path, pagesize=A4)
            styles = getSampleStyleSheet()
            story = []
            story.append(Paragraph(f"Financial Summary Report — Month {m}/{y}",
                                   styles["Title"]))
            story.append(Spacer(1, 12))
            data = [
                ["Item", "Value (VND)"],
                ["Total Income", f"{income:,.0f}"],
                ["Total Expense", f"{expense:,.0f}"],
                ["Savings",     f"{saving:,.0f}"],
                ["Status",      status],
            ]
            t = Table(data, colWidths=[250, 200])
            t.setStyle(TableStyle([
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#4F8EF7")),
                ("TEXTCOLOR",  (0, 0), (-1, 0), colors.white),
                ("FONTNAME",   (0, 0), (-1, 0), "Helvetica-Bold"),
                ("ROWBACKGROUNDS", (0, 1), (-1, -1),
                 [colors.white, colors.HexColor("#F0F4F8")]),
                ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
                ("ALIGN", (1, 0), (1, -1), "RIGHT"),
            ]))
            story.append(t)
            doc.build(story)
            messagebox.showinfo("Export PDF", f"File saved:\n{path}")
        except ImportError:
            messagebox.showerror(
                "Missing library",
                "Please install reportlab:\n  pip install reportlab"
            )
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def _export_category_csv(self, rows, m, y):
        path = self._get_export_path(f"expenses_by_category_{m}_{y}.csv")
        if not path:
            return
        try:
            with open(path, "w", newline="", encoding="utf-8-sig") as fh:
                w = csv.writer(fh)
                w.writerow([f"Expenses by category — Month {m}/{y}"])
                w.writerow([])
                w.writerow(["Category", "Transactions", "Total (VND)", "Avg/Tx (VND)"])
                for r in rows:
                    w.writerow([r["CategoryName"], r["Cnt"],
                                f"{float(r['Total']):,.0f}",
                                f"{float(r['Avg']):,.0f}"])
            messagebox.showinfo("Export CSV", f"File saved:\n{path}")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def _export_trend_csv_from_vals(self, labels, inc_vals, exp_vals, net_vals, mode):
        mode_names = {"1week": "1week", "3month": "3months", "6month": "6months", "12month": "12months"}
        filename = f"trend_{mode_names.get(mode, mode)}.csv"
        path = self._get_export_path(filename)
        if not path:
            return
        try:
            with open(path, "w", newline="", encoding="utf-8-sig") as fh:
                w = csv.writer(fh)
                w.writerow(["Period", "Income (VND)", "Expense (VND)", "Savings (VND)"])
                for label, inc, exp, net in zip(labels, inc_vals, exp_vals, net_vals):
                    w.writerow([label, f"{inc:,.0f}", f"{exp:,.0f}", f"{net:,.0f}"])
            messagebox.showinfo("Export CSV", f"File saved:\n{path}")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def _export_history_csv(self, rows, acc_map):
        path = self._get_export_path("transaction_history.csv")
        if not path:
            return
        try:
            with open(path, "w", newline="", encoding="utf-8-sig") as fh:
                w = csv.writer(fh)
                w.writerow(["Date", "Type", "Bank", "Amount (VND)"])
                for r in reversed(rows):
                    kind   = "Income" if r["type"] == "income" else "Expense"
                    prefix = "+" if r["type"] == "income" else "-"
                    w.writerow([str(r["txDate"]), kind,
                                acc_map.get(r["AccountID"], "?"),
                                f"{prefix}{float(r['Amount']):,.0f}"])
            messagebox.showinfo("Export CSV", f"File saved:\n{path}")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    # ── LOGOUT ───────────────────────────────────────────────────
    def logout(self):
        if messagebox.askyesno("Logout", "Do you want to logout?"):
            self.root.destroy()
            login_root = tk.Tk()
            LoginWindow(login_root)
            login_root.mainloop()


# ════════════════════════════════════════════════════════════════
#  ENTRY POINT
# ════════════════════════════════════════════════════════════════
if __name__ == "__main__":
    root = tk.Tk()
    LoginWindow(root)
    root.mainloop()