# Upwise 💰

A full-stack expense tracking application that helps users build discipline in financial management — by recording, categorizing, and visualizing where their money actually goes.

---

## 🎯 Purpose

Upwise was built to solve a real problem: poor money management habits. Instead of wondering where your salary disappeared, Upwise gives you a clear, visual breakdown of your spending by category — turning scattered transactions into actionable insight that builds financial discipline over time.

---

## 🛠️ Tech Stack

**Frontend**
- HTML5
- CSS3 (Flexbox, CSS animations, marquee effect)
- JavaScript (DOM manipulation, Fetch API, Chart.js)
- Jinja2 (templating)

**Backend**
- Python (Flask)
- MySQL (via XAMPP)
- Flask-Bcrypt (password hashing)
- python-dotenv (environment variable management)

**Data Visualization**
- Chart.js (donut chart with real-time filtering)

---

## ✨ Features

- [x] Public landing page (hero, scrolling logo marquee, features, testimonials, FAQ, newsletter CTA)
- [x] User registration with bcrypt password hashing
- [x] Secure login with session-based authentication
- [x] Protected dashboard — only accessible when logged in
- [x] Add expenses via modal popup (amount, category, date, description)
- [x] Expense table showing last 10 expenses with JOIN query (category name + expense data)
- [x] Summary cards (total spent, top category, expense count — all this month)
- [x] Donut chart showing spending split by category
- [x] Category filter — filters both the table AND the chart simultaneously
- [x] Environment variables for all sensitive credentials (.env)

---

## 📁 Project Structure

```
Upwise/
├── app.py
├── requirements.txt
├── .env                  # not pushed to GitHub
├── .gitignore
├── templates/
│   ├── home.html
│   ├── login.html
│   ├── signup.html
│   └── dashboard.html
└── static/
    ├── css/
    │   ├── home.css
    │   ├── auth.css
    │   └── dashboard.css
    ├── js/
    │   └── dashboard.js
    └── images/
```

---

## 🚀 Setup & Installation

### 1. Clone the repository
```bash
git clone https://github.com/CipherNex0/upwise-expense-tracker.git
cd upwise-expense-tracker
```

### 2. Create and activate a virtual environment
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Set up the database
- Start MySQL (via XAMPP or your preferred method)
- Create a database called `expense_tracker_db`
- Run the following SQL:

```sql
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE categories (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(200) NOT NULL
);

CREATE TABLE expenses (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    category_id INT,
    amount DECIMAL(10, 2),
    date DATE,
    time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    description TEXT,
    FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY(category_id) REFERENCES categories(id) ON DELETE CASCADE
);

INSERT INTO categories (name) VALUES
('Food & Dining'),
('Clothing'),
('Transport & Travel'),
('Personal Care'),
('Entertainment');
```

### 5. Create your `.env` file in the project root
```
ADMIN_SECRET_KEY=your_random_secret_key
DB_HOST=127.0.0.1
DB_PORT=3306
DB_USER=root
DB_PASSWORD=
DB_NAME=expense_tracker_db
```

Generate a secret key:
```bash
python3 -c "import secrets; print(secrets.token_hex(32))"
```

### 6. Run the app
```bash
python3 app.py
```

Visit `http://127.0.0.1:5000` in your browser.

---

## 📸 Screenshots

![Home Page](/static/images/screenshots/home.png)
![Dashboard](/static/images/screenshots/dashboard.png)
![Add Expense Modal](/static/images/screenshots/expenseModal.png)

---

## 📚 What I Learned

- **SQL JOINs** — how to combine data from two tables in a single query, specifically joining `expenses` and `categories` to display the category name instead of just the id number stored in the database.
- **SQL aggregation** — using `GROUP BY`, `SUM()`, and `COUNT()` to calculate totals per category, total monthly spending, and expense counts directly in the database instead of processing data in Python.
- **Chart.js** — how to create a donut chart, pass real data from Flask/Python into JavaScript via Jinja2's `tojson` filter, and dynamically update the chart when the user applies a filter.
- **Filter logic in JavaScript** — how to filter table rows and update a chart simultaneously based on a dropdown selection, keeping both the table and the visualization in sync.

---

## 🔭 Future Improvements

- [ ] AI integration — an AI assistant that analyzes your spending and gives personalized financial advice
- [ ] Telegram integration via n8n — chat with your expense data directly from Telegram without opening the site
- [ ] User profile page — change username, upload profile picture, manage account settings
- [ ] Sidebar navigation — collapsible left sidebar for easier dashboard navigation
- [ ] Weekly and yearly views — toggle between week, month, and year spending breakdowns
- [ ] Budget limits — set spending limits per category and get alerts when approaching them
- [ ] Delete and edit expenses

---

## 📄 License

This project was built for personal learning purposes as part of a full-stack development journey toward AI Systems Architecture.