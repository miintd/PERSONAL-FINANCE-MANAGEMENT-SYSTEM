# 🏦 Personal Finance Management System — Sơ đồ Kiến trúc

## 1. Cấu trúc Thư mục (Folder Structure)

```
personal_finance_project/
│
├── 📁 sql/                          ← Tầng Cơ sở dữ liệu (Database Layer)
│   ├── structure&data.sql           ← Tạo bảng + dữ liệu mẫu (10 records/bảng)
│   ├── advanced.sql                 ← Index, View, Function, Procedure, Trigger
│   └── admin&security.sql           ← Phân quyền user + View bảo mật
│
├── 📁 python/                       ← Tầng Ứng dụng (Application Layer)
│   ├── config.py                    ← Cấu hình kết nối MySQL
│   ├── database.py                  ← Database wrapper (CRUD + call procedure)
│   ├── income_expense.py            ← Business logic (thu nhập, chi tiêu, báo cáo)
│   └── app.py                       ← GUI Tkinter (Login, Register, Dashboard, ...)
│
├── 📁 backup/                       ← Sao lưu dữ liệu
│   ├── personal_finance_backup.sql  ← Backup đầy đủ
│   ├── schema_only.sql              ← Chỉ cấu trúc
│   └── data_only.sql                ← Chỉ dữ liệu
│
└── 📁 .git/                         ← Git version control
```

---

## 2. Kiến trúc Tổng quan (Architecture Overview)

```mermaid
graph TB
    subgraph "🖥️ Presentation Layer"
        APP["app.py<br/>(Tkinter GUI)"]
        LOGIN["LoginWindow"]
        REG["RegisterWindow"]
        MAIN["MainApp<br/>Dashboard, Income, Expense,<br/>Accounts, Reports"]
        SETUP["SetupBankWindow"]
        DIALOG["AddBankDialog"]
        
        APP --> LOGIN
        APP --> REG
        APP --> MAIN
        APP --> SETUP
        APP --> DIALOG
    end

    subgraph "⚙️ Business Logic Layer"
        IE["income_expense.py<br/>(24 hàm)"]
        IE_ACC["Tài khoản<br/>get_user_accounts<br/>get_account_balance<br/>get_total_balance<br/>set_initial_balance"]
        IE_INC["Thu nhập<br/>add / get_all / delete"]
        IE_EXP["Chi tiêu<br/>add / get_all / delete<br/>check_sufficient_balance"]
        IE_RPT["Báo cáo<br/>monthly_summary<br/>budget_status<br/>monthly_closure<br/>trend / alerts"]
        
        IE --> IE_ACC
        IE --> IE_INC
        IE --> IE_EXP
        IE --> IE_RPT
    end

    subgraph "🔌 Data Access Layer"
        DB["database.py"]
        DB_EXEC["execute()"]
        DB_FETCH["fetchall() / fetchone()"]
        DB_PROC["call_procedure()"]
        CFG["config.py<br/>host, user, password, database"]
        
        DB --> DB_EXEC
        DB --> DB_FETCH
        DB --> DB_PROC
        DB --> CFG
    end

    subgraph "🗄️ Database Layer - MySQL"
        TABLES["Tables:<br/>USERS, BANKACCOUNTS,<br/>INCOME, EXPENSES,<br/>EXPENSECATEGORIES"]
        PROCS["Procedures:<br/>sp_add_income<br/>sp_add_expense<br/>sp_set_initial_balance<br/>sp_monthly_closure"]
        FUNCS["Functions:<br/>fn_income/expense_by_account<br/>fn_sufficient_balance<br/>fn_budget_status_by_account/user<br/>fn_total_income/expense_by_user"]
        TRIGS["Triggers:<br/>trg_after_income_insert<br/>trg_before_expense_insert<br/>trg_after_expense_insert<br/>trg_after_expense/income_delete"]
        VIEWS["Views:<br/>vw_monthly_summary_by_account<br/>vw_category_spending_by_account<br/>vw_user_total_balance<br/>vw_users_safe"]
        INDEXES["Indexes:<br/>idx_income_user/date/account<br/>idx_expenses_user/date/category/account<br/>idx_bankaccount_user"]
    end

    MAIN -->|"import ie"| IE
    LOGIN --> DB
    REG --> DB
    SETUP --> DB
    DIALOG --> DB
    IE --> DB
    DB --> TABLES
    DB --> PROCS
    DB --> FUNCS
    PROCS --> FUNCS
    PROCS --> TABLES
    TRIGS --> TABLES
    VIEWS --> TABLES
    INDEXES --> TABLES
```

---

## 3. Sơ đồ ERD — Quan hệ giữa các bảng

```mermaid
erDiagram
    USERS ||--o{ BANKACCOUNTS : "1 user → nhiều tài khoản"
    USERS ||--o{ INCOME : "1 user → nhiều khoản thu"
    USERS ||--o{ EXPENSES : "1 user → nhiều khoản chi"
    BANKACCOUNTS ||--o{ INCOME : "1 TK → nhiều thu nhập"
    BANKACCOUNTS ||--o{ EXPENSES : "1 TK → nhiều chi tiêu"
    EXPENSECATEGORIES ||--o{ EXPENSES : "1 danh mục → nhiều chi tiêu"

    USERS {
        INT UserID PK
        VARCHAR UserName
        VARCHAR Email UK
        VARCHAR PhoneNumber
        VARCHAR Password
    }

    BANKACCOUNTS {
        INT AccountID PK
        INT UserID FK
        VARCHAR BankName
        DECIMAL Balance
    }

    INCOME {
        INT IncomeID PK
        INT UserID FK
        INT AccountID FK
        DECIMAL Amount
        DATE IncomeDate
        VARCHAR Description
    }

    EXPENSES {
        INT ExpenseID PK
        INT UserID FK
        INT CategoryID FK
        INT AccountID FK
        DECIMAL Amount
        DATE ExpenseDate
        VARCHAR Description
    }

    EXPENSECATEGORIES {
        INT CategoryID PK
        VARCHAR CategoryName
    }
```

---

## 4. Luồng hoạt động của ứng dụng (Application Flow)

```mermaid
flowchart TD
    START(["Khởi chạy app.py"]) --> LOGIN_SCREEN["Màn hình đăng nhập"]
    
    LOGIN_SCREEN -->|"Có tài khoản"| AUTH{"Xác thực<br/>Email + Password"}
    LOGIN_SCREEN -->|"Chưa có"| REGISTER["Đăng ký tài khoản mới"]
    REGISTER --> LOGIN_SCREEN
    
    AUTH -->|"Thất bại"| LOGIN_SCREEN
    AUTH -->|"Thành công"| CHECK_BANK{"Kiểm tra<br/>có tài khoản<br/>ngân hàng?"}
    
    CHECK_BANK -->|"Chưa có"| SETUP_BANK["Setup Bank Account"]
    SETUP_BANK --> DASHBOARD
    CHECK_BANK -->|"Có rồi"| DASHBOARD
    
    DASHBOARD["🏠 Dashboard<br/>• Tổng thu/chi/tiết kiệm<br/>• Biểu đồ 6 tháng<br/>• Số dư hiện tại"]
    
    DASHBOARD <--> INCOME["💵 Income<br/>• Thêm thu nhập<br/>• Xem danh sách<br/>• Xóa thu nhập"]
    DASHBOARD <--> EXPENSE["💸 Expense<br/>• Thêm chi tiêu<br/>• Kiểm tra số dư<br/>• Xóa chi tiêu"]
    DASHBOARD <--> ACCOUNTS["🏦 Accounts<br/>• Danh sách TK ngân hàng<br/>• Trạng thái ngân sách/TK<br/>• Chỉnh sửa số dư<br/>• Thêm TK mới"]
    DASHBOARD <--> REPORTS["📊 Reports<br/>• Summary, Category, Trend<br/>• Closure - chốt sổ tháng<br/>• Alerts, Balance History<br/>• Xuất CSV/PDF"]
    
    INCOME -->|"ie.add_income<br/>sp_add_income"| IE_LAYER["income_expense.py"]
    EXPENSE -->|"ie.add_expense<br/>ie.check_sufficient_balance"| IE_LAYER
    ACCOUNTS -->|"ie.set_initial_balance<br/>ie.get_budget_status_by_account"| IE_LAYER
    REPORTS -->|"ie.get_monthly_closure<br/>ie.get_monthly_summary"| IE_LAYER
    
    IE_LAYER -->|"database.py"| DB_LAYER[("MySQL Database")]
    
    DB_LAYER -->|"Trigger cộng/trừ Balance"| DB_LAYER
```

---

## 5. Phân quyền User trong MySQL

```mermaid
graph LR
    subgraph "MySQL Users & Roles"
        ADMIN["🔑 pf_admin<br/>ALL PRIVILEGES"]
        APP_USER["🔧 pf_app<br/>SELECT, INSERT,<br/>UPDATE, DELETE,<br/>EXECUTE"]
        REPORT["📊 pf_report<br/>SELECT only"]
        READONLY["👁️ pf_readonly<br/>SELECT on Views only"]
    end

    DB[("personal_finance<br/>Database")]

    ADMIN -->|"Toàn quyền"| DB
    APP_USER -->|"CRUD + Procedures"| DB
    REPORT -->|"Đọc tất cả bảng"| DB
    READONLY -->|"Chỉ xem Views"| DB
```

---

## 6. Mô tả chi tiết từng file

| File | Vai trò | Chi tiết |
|------|---------|----------|
| `config.py` | Cấu hình DB | Host, user, password, database name |
| `database.py` | Data Access | Class `Database` với `execute()`, `fetchall()`, `fetchone()`, `call_procedure()`, `close()` |
| `income_expense.py` | Business Logic | **24 hàm**: quản lý tài khoản, thu nhập, chi tiêu, danh mục, báo cáo (summary, budget status, closure, trend, alerts), kiểm tra số dư |
| `app.py` | GUI (~1670 dòng) | 6 class Tkinter + 5 trang (Dashboard, Income, Expense, Accounts, Reports) + 6 tab Reports (Summary, Category, Trend, **Closure**, Alerts, History) |
| `structure&data.sql` | Schema + Seed | 5 bảng + 10 records mẫu mỗi bảng |
| `advanced.sql` | Advanced DB | 8 Index, 3 View, 7 Function, 4 Procedure, 5 Trigger |
| `admin&security.sql` | Security | 4 MySQL users, phân quyền RBAC, View ẩn thông tin nhạy cảm |

---

## 7. Công nghệ sử dụng

| Thành phần | Công nghệ |
|------------|-----------|
| **Database** | MySQL |
| **Backend** | Python 3 |
| **GUI Framework** | Tkinter + ttk |
| **Charting** | Matplotlib (embedded in Tkinter) |
| **DB Connector** | mysql-connector-python |
| **Export** | CSV |
