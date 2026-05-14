# Personal Finance Management System

A comprehensive desktop application for managing personal finances with multi-account support, transaction tracking, and advanced financial reporting.

**🎥 Video Presentation & Live Demo:** [https://youtu.be/QyMR2rBR-Ho](https://youtu.be/QyMR2rBR-Ho)

---

## 📋 Table of Contents

- [Project Overview](#project-overview)
- [Directory Structure](#directory-structure)
- [Features](#features)
- [Architecture](#architecture)
- [Technology Stack](#technology-stack)
- [Installation & Setup](#installation--setup)
- [Running the Application](#running-the-application)
- [File Descriptions](#file-descriptions)
- [Application Workflow](#application-workflow)
- [Database Schema](#database-schema)

---

## 🎯 Project Overview

The **Personal Finance Management System** is a desktop application that helps users:
- Manage multiple bank accounts
- Track income and expenses with categories
- Monitor budget status (Surplus/Deficit)
- Generate comprehensive financial reports
- Export reports to CSV and PDF formats
- Analyze spending trends over time

**Key Highlights:**
- User authentication and registration
- Multi-account management
- Category-based expense tracking
- Interactive dashboards with visualizations
- Advanced financial reports (Summary, Closure, Trends, Alerts)
- Excel & PDF export functionality
- Responsive Tkinter GUI with modern UI design

---

## 📁 Directory Structure

```
personal_finance_project/
│
├── 📁 sql/                          ← Database Layer
│   ├── structure&data.sql           ← Create tables + sample data
│   ├── advanced.sql                 ← Indexes, Views, Functions, Procedures, Triggers
│   └── admin&security.sql           ← User permissions & security views
│
├── 📁 python/                       ← Application Layer
│   ├── config.py                    ← MySQL connection configuration
│   ├── database.py                  ← Database wrapper (CRUD operations)
│   ├── income_expense.py            ← Business logic & core functions
│   └── app.py                       ← GUI interface (Tkinter)
│
├── 📁 backup/                       ← Database Backups
│   ├── personal_finance_backup.sql  ← Full backup
│   ├── schema_only.sql              ← Schema only
│   └── data_only.sql                ← Data only
│
└── README.md                        ← This file
```

---

## ✨ Features

### 1. **User Management**
- User registration with email validation
- Secure login authentication
- User profile management
- Logout functionality

### 2. **Account Management**
- Create and manage multiple bank accounts
- Set account types (Savings, Checking, Credit Card, etc.)
- Track account balances
- View total balance across all accounts

### 3. **Income & Expense Tracking**
- Record income transactions
- Log expense transactions by category
- Categorized expense tracking
- Transaction history with filtering
- Date and amount tracking

### 4. **Dashboard**
- Quick overview of key metrics
- Total balance display
- Recent transactions list
- Budget status indicator
- Account summary cards

### 5. **Reports & Analytics**
- **Summary Reports:** Monthly income, expenses, savings, and budget status
- **Category Reports:** Spending breakdown by category
- **Trend Analysis:** Income/expense trends over 1 week, 3 months, 6 months, or 12 months
- **Monthly Closure:** Detailed monthly financial closure with status indicator
- **Alert System:** Deficit month warnings
- **Balance History:** Account balance tracking over time

### 6. **Export Functionality**
- Export reports to CSV (Excel-compatible)
- Export reports to PDF with professional formatting
- Transaction history export
- Category analysis export

---

## 🏗️ Architecture

### Layered Architecture

```
┌─────────────────────────────────────────────────────────┐
│           Presentation Layer (GUI)                      │
│  - Tkinter UI Components                               │
│  - Login, Register, Dashboard, Reports                 │
│  - Interactive Charts & Tables                         │
└──────────────────┬──────────────────────────────────────┘
                   │
┌──────────────────▼──────────────────────────────────────┐
│         Business Logic Layer                           │
│  - income_expense.py (24+ functions)                   │
│  - Financial calculations                             │
│  - Report generation                                  │
│  - Data aggregation                                   │
└──────────────────┬──────────────────────────────────────┘
                   │
┌──────────────────▼──────────────────────────────────────┐
│        Data Access Layer (database.py)                 │
│  - CRUD operations                                    │
│  - Stored procedure calls                             │
│  - Database connection management                     │
└──────────────────┬──────────────────────────────────────┘
                   │
┌──────────────────▼──────────────────────────────────────┐
│        Database Layer (MySQL)                          │
│  - Tables, Views, Procedures, Triggers                │
│  - Data persistence                                   │
│  - Complex queries & aggregations                     │
└─────────────────────────────────────────────────────────┘
```

---

## 🛠️ Technology Stack

| Component | Technology | Version |
|-----------|-----------|---------|
| **GUI Framework** | Tkinter | Built-in Python |
| **Database** | MySQL | 8.0+ |
| **Language** | Python | 3.8+ |
| **Visualization** | Matplotlib | Latest |
| **Database Connector** | mysql-connector-python | 8.0+ |
| **PDF Generation** | ReportLab | Latest |
| **CSV Processing** | csv module | Built-in Python |

---

## 📦 Installation & Setup

### Prerequisites
- **Python 3.8 or higher** - [Download](https://www.python.org/downloads/)
- **MySQL 8.0 or higher** - [Download](https://dev.mysql.com/downloads/mysql/)
- **MySQL Workbench (Optional)** - For database management

### Step 1: Clone/Download the Project
```bash
# Navigate to your desired directory
cd path/to/your/workspace

# Download or clone this project
git clone https://github.com/miintd/PERSONAL-FINANCE-MANAGEMENT-SYSTEM.git
cd personal_finance_project
```

### Step 2: Set Up the Database

**Option A: Using MySQL Command Line**
```bash
# Login to MySQL
mysql -u root -p

# Create database and import schema
CREATE DATABASE personal_finance;
USE personal_finance;

# Import SQL files in order
SOURCE sql/structure&data.sql;
SOURCE sql/advanced.sql;
SOURCE sql/admin&security.sql;
```

**Option B: Using MySQL Workbench**
1. Open MySQL Workbench
2. Create new database: `personal_finance`
3. Import each SQL file in order using File → Open SQL Script

### Step 3: Install Python Dependencies

```bash
# Navigate to the python directory
cd python

# Install required packages
pip install -r requirements.txt
```

### Step 4: Configure Database Connection

Edit `python/config.py` and set your MySQL credentials. You have two options:

**Option A: Use your root MySQL account**
```python
DB_CONFIG = {
    "host":     "localhost",
    "user":     "root",
    "password": "your_root_password",  # Replace with your MySQL root password
    "database": "personal_finance"
}
```

**Option B: Use the pf_app account (created by admin&security.sql)**
```python
DB_CONFIG = {
    "host":     "localhost",
    "user":     "pf_app",
    "password": "App@123456",
    "database": "personal_finance"
}
```

> **Note:** The `pf_app` user account is automatically created when you run `sql/admin&security.sql`. Choose the option that works best for your setup.

---

## 🚀 Running the Application

### Start the Application

```bash
# Navigate to python directory
cd python

# Run the application
python app.py
```

### Login Credentials (Default Sample)

The database includes sample data. Check the SQL files for default accounts or create your own.
Sample account to test:

```bash
# sample 1
Email: thao.tran@gmail.com
Password: 123456
```
```bash
# sample 2
Email: khoa.nguyen@gmail.com
Password: 123456
```

### Application Usage Flow

1. **Login/Register** → Authenticate user
2. **Setup Banks** → Create and configure bank accounts
3. **Dashboard** → View overview and recent transactions
4. **Income Tab** → Record income transactions
5. **Expense Tab** → Record expense transactions
6. **Accounts Tab** → Manage accounts and balances
7. **Reports Tab** → Generate and export financial reports

---

## 🔄 Application Workflow

### User Journey

```
1. START
   ↓
2. LOGIN/REGISTER
   ├─ New User → Register → Verify → Login
   └─ Existing User → Login
   ↓
3. SETUP BANKS (First Time)
   ├─ Add Bank Account
   ├─ Set Account Type
   └─ Set Initial Balance
   ↓
4. MAIN DASHBOARD
   ├─ View Balance Overview
   ├─ Recent Transactions
   └─ Budget Status
   ↓
5. MANAGE TRANSACTIONS
   ├─ Record Income
   ├─ Record Expense (with Category)
   └─ View Transaction History
   ↓
6. ACCOUNT MANAGEMENT
   ├─ View All Accounts
   ├─ Update Account Info
   └─ Check Balances
   ↓
7. GENERATE REPORTS
   ├─ Summary Report (Income/Expense/Savings/Status)
   ├─ Category Breakdown
   ├─ Trend Analysis (1W/3M/6M/12M)
   ├─ Monthly Closure (with Status & PDF/CSV)
   ├─ Alerts (Deficit Months)
   └─ Balance History
   ↓
8. EXPORT REPORTS
   ├─ Export to CSV
   └─ Export to PDF
   ↓
9. LOGOUT
   ↓
END
```

### Report Generation Flow

```
User selects Report Type
       ↓
Business Logic (income_expense.py)
       ├─ Query database
       ├─ Calculate totals & aggregates
       ├─ Determine budget status
       └─ Format data
       ↓
GUI Display (app.py)
       ├─ Display cards/charts
       ├─ Show details table
       └─ Provide export options
       ↓
Export Options
       ├─ CSV Export (Excel)
       └─ PDF Export (Professional Format)
```

---

## 📄 File Descriptions

### Backend Files

#### `config.py`
- **Purpose:** Database connection configuration
- **Key Variables:**
  - `DB_CONFIG`: MySQL connection parameters
- **Usage:** Imported by `database.py`

#### `database.py`
- **Purpose:** Database abstraction layer
- **Key Methods:**
  - `execute()`: Execute INSERT/UPDATE/DELETE queries
  - `fetchall()`: Retrieve multiple records
  - `fetchone()`: Retrieve single record
  - `call_procedure()`: Execute stored procedures
  - `close()`: Close database connection
- **Usage:** Used by `income_expense.py` and `app.py`

#### `income_expense.py`
- **Purpose:** Core business logic for financial operations
- **Key Functions:**
  - Account: `get_user_accounts()`, `get_total_balance()`, `set_initial_balance()`
  - Income: `add_income()`, `get_income_by_user()`
  - Expense: `add_expense()`, `get_expense_by_user()`
  - Reports: `get_monthly_summary()`, `get_monthly_closure()`, `get_budget_status_by_user()`
  - Analytics: `get_monthly_trend()`, `get_deficit_months()`, `get_category_spending()`
- **Total Functions:** 24+ financial calculation functions

#### `app.py`
- **Purpose:** Main GUI application using Tkinter
- **Key Components:**
  - `LoginWindow`: User authentication
  - `RegisterWindow`: New user registration
  - `MainApp`: Main dashboard and application
  - `SetupBankWindow`: Account setup
  - Report generation and export functions
- **Features:**
  - Modern UI with color scheme
  - Tab-based navigation
  - Real-time balance updates
  - Interactive charts and visualizations

### Database Files (SQL)

#### `sql/structure&data.sql`
- Creates database schema with 5 main tables:
  - `USERS`: User accounts
  - `BANKACCOUNTS`: User bank accounts and balances
  - `INCOME`: Income records
  - `EXPENSE`: Expense records
  - `EXPENSECATEGORIES`: Expense categories
- Includes sample data for testing

#### `sql/advanced.sql`
- **Indexes:** Performance optimization
- **Views:** Pre-built queries for reports
- **Functions:** SQL calculations
- **Stored Procedures:** Complex business logic
- **Triggers:** Automatic data validation and updates

#### `sql/admin&security.sql`
- User role definitions
- Permission assignments
- Security views for data protection

### Backup Files

- `backup/personal_finance_backup.sql`: Complete database backup
- `backup/schema_only.sql`: Database structure only
- `backup/data_only.sql`: Sample data only

---

## 🗄️ Database Schema

### Main Tables

| Table | Purpose |
|-------|---------|
| `USERS` | User authentication & profile |
| `BANKACCOUNTS` | User bank accounts and balances |
| `INCOME` | Income transaction records |
| `EXPENSE` | Expense transaction records |
| `EXPENSECATEGORIES` | Expense categories |

### Key Relationships

```
USERS (1) ──→ (N) BANKACCOUNTS
USERS (1) ──→ (N) INCOME
USERS (1) ──→ (N) EXPENSE
BANKACCOUNTS (1) ──→ (N) INCOME
BANKACCOUNTS (1) ──→ (N) EXPENSE
EXPENSECATEGORIES (1) ──→ (N) EXPENSE
```

---

## 📊 Report Types

### 1. Summary Report
- **Shows:** Total Income, Total Expense, Savings, Budget Status
- **Filter:** By Month/Year
- **Export:** CSV, PDF

### 2. By Category Report
- **Shows:** Expense breakdown by category with transaction count
- **Filter:** By Month/Year
- **Export:** CSV

### 3. Trend Report
- **Shows:** Income vs Expense trends over time
- **Options:** 1 Week, 3 Months, 6 Months, 12 Months
- **Export:** CSV

### 4. Monthly Closure Report
- **Shows:** Complete monthly financial summary with status (Surplus/Deficit)
- **Filter:** By Month/Year/Account
- **Export:** CSV, PDF

### 5. Alert Report
- **Shows:** Months with deficit (negative cash flow)
- **Display:** Last 6 deficit months

### 6. Balance History Report
- **Shows:** Account balance trends over time
- **Export:** CSV

---

## 🔧 Troubleshooting

### Connection Issues
```
Error: Can't connect to MySQL server
Solution:
1. Verify MySQL is running
2. Check credentials in config.py
3. Ensure database exists
4. Verify user has proper permissions
```

### Missing Dependencies
```
Error: ModuleNotFoundError
Solution:
pip install mysql-connector-python matplotlib reportlab
```

### Database Errors
```
Error: Tables don't exist
Solution:
1. Re-run SQL scripts in order:
   - structure&data.sql
   - advanced.sql
   - admin&security.sql
```

---

## 📚 References

- [Python Tkinter Documentation](https://docs.python.org/3/library/tkinter.html)
- [MySQL Documentation](https://dev.mysql.com/doc/)
- [mysql-connector-python](https://dev.mysql.com/doc/connector-python/en/)
- [Matplotlib](https://matplotlib.org/stable/contents.html)
- [ReportLab](https://www.reportlab.com/docs/reportlab-userguide.pdf)

---

## 🎥 Video Resources

**Project Presentation & Live Demo:**  
[https://youtu.be/QyMR2rBR-Ho](https://youtu.be/QyMR2rBR-Ho)

Watch the video to see:
- Feature walkthrough
- Live application demonstration
- Report generation examples
- PDF/CSV export functionality

---

## 🎯 Future Enhancements

- [ ] Multiple user authentication with role-based access
- [ ] Data encryption for sensitive information
- [ ] Import transactions from bank statements
- [ ] Automated recurring transactions
- [ ] Budget alerts and notifications
- [ ] Mobile app integration
- [ ] Cloud database support
- [ ] Advanced financial forecasting
- [ ] Multi-currency support

---

**Version:** 1.0.0  
**Last Updated:** May 2026  
**Status:** Production Ready 
