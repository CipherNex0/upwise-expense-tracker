from flask import Flask, render_template, session, jsonify, request, redirect, url_for
from flask_bcrypt import Bcrypt
from dotenv import load_dotenv
from flask_mysqldb import MySQL
import os
from functools import wraps

load_dotenv()

app = Flask(__name__)

app.secret_key = os.getenv('ADMIN_SECRET_KEY')

bcrypt = Bcrypt(app)

app.config['MYSQL_HOST'] = os.getenv('DB_HOST')
app.config['MYSQL_PORT'] = int(os.getenv('DB_PORT'))
app.config['MYSQL_USER'] = os.getenv('DB_USER')
app.config['MYSQL_PASSWORD'] = os.getenv('DB_PASSWORD')
app.config['MYSQL_DB'] = os.getenv('DB_NAME')

mysql = MySQL(app)

def login_required(f):
    @wraps(f)

    def decorated_function(*args, **kwargs):
        if not session.get('user_id'):
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return(decorated_function)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '').strip()
        confirm_password = request.form.get('confirmPassword', '').strip()

        if not username or not password or not confirm_password:
            return render_template('signup.html', error='All fields are required.')
        
        if password != confirm_password:
            return render_template('signup.html', error='Passwords do not match.')
        
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

        cursor = mysql.connection.cursor()

        cursor.execute("SELECT id FROM users WHERE username=%s", (username,))

        existing_user = cursor.fetchone()

        if existing_user:
            cursor.close()
            return render_template('signup.html', error='Username already exists.')
        
        cursor.execute ("INSERT INTO users (username, password) VALUES(%s, %s)", (username, hashed_password))
        mysql.connection.commit()
        cursor.close()
        
        return redirect(url_for('login'))
    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '').strip()

        cursor = mysql.connection.cursor()

        cursor.execute("SELECT id, username, password FROM users WHERE username=%s", (username,))

        user = cursor.fetchone()
        cursor.close()

        if user and bcrypt.check_password_hash(user[2], password):
            print("Login Successful!")
            session['user_id']  = user[0]
            session['username'] = user[1]

            print("Redirecting to dashboard...")

            return redirect(url_for('dashboard'))
        
        return render_template('login.html', error="Invalid username or password.")
    return render_template('login.html')

@app.route('/dashboard')
@login_required
def dashboard():
    cursor = mysql.connection.cursor()

    #JOIN Query - gets last 10 expenses with category name
    cursor.execute(""" SELECT expenses.id, expenses.amount, expenses.date, expenses.description, categories.name FROM expenses JOIN categories ON expenses.category_id = categories.id WHERE expenses.user_id=%s ORDER BY expenses.date DESC LIMIT 10""", (session['user_id'],))

    expenses = cursor.fetchall()

    #Total spent this month
    cursor.execute(""" SELECT SUM(amount) FROM expenses WHERE user_id=%s AND MONTH(date) = MONTH(CURDATE()) AND YEAR(date) = YEAR(CURDATE())""", (session['user_id'],))

    total_spent = cursor.fetchone()[0] or 0

    #Number of expenses this month
    cursor.execute(""" SELECT COUNT(*) FROM expenses WHERE user_id=%s AND MONTH(date) = MONTH(CURDATE()) AND YEAR(date) = YEAR(CURDATE()) """, (session['user_id'],))
    
    expense_count = cursor.fetchone()[0]

    #Top spending this month
    cursor.execute(""" SELECT categories.name, SUM(expenses.amount) as total FROM expenses JOIN categories ON expenses.category_id = categories.id WHERE expenses.user_id=%s AND MONTH(expenses.date) = MONTH(CURDATE()) AND YEAR(expenses.date) = YEAR(CURDATE()) GROUP BY categories.name ORDER BY total DESC LIMIT 1 """, (session['user_id'],))
    
    top_category = cursor.fetchone()

    #Totals per category for the chart
    cursor.execute(""" SELECT categories.name, SUM(expenses.amount) as total FROM expenses JOIN categories ON expenses.category_id = categories.id WHERE expenses.user_id=%s AND MONTH(expenses.date) = MONTH(CURDATE()) AND YEAR(expenses.date) = YEAR(CURDATE()) GROUP BY categories.name ORDER BY total DESC""", (session['user_id'],))

    category_totals = cursor.fetchall()

    cursor.close()

    return render_template(
        'dashboard.html',
        username=session.get('username'),
        expenses=expenses,
        total_spent=total_spent,
        expense_count=expense_count,
        top_category=top_category[0] if top_category else 'None',
        category_totals=category_totals
        )

@app.route('/expenses/create', methods=['POST'])
@login_required
def create_expense():
    amount = request.form.get('amount', '').strip()
    category_id = request.form.get('category_id', '').strip()
    date = request.form.get('date', '').strip()
    description = request.form.get('description', '').strip()

    if not amount:
        return jsonify({'status': 'error', 'message': 'Amount is required'}), 400
    
    cursor = mysql.connection.cursor()

    cursor.execute(""" INSERT INTO expenses (user_id, category_id, amount, date, description) VALUES(%s, %s, %s, %s, %s)""", (session['user_id'], category_id, amount, date or None, description))

    mysql.connection.commit()

    new_expense_id = cursor.lastrowid
    cursor.close()

    return jsonify({'status': 'success', 'expense': {
        'id': new_expense_id,
        'amount': amount,
        'category_id':'Food & Dining',
        'date': date,
        'description': description
    }})

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(debug=True)