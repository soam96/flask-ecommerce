from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

users_bp = Blueprint('users', __name__, url_prefix='/users')

class User:
    def __init__(self, user_id, username, email, role):
        self.id = user_id
        self.username = username
        self.email = email
        self.role = role
    
    def is_authenticated(self):
        return True
    
    def is_active(self):
        return True
    
    def is_anonymous(self):
        return False
    
    def get_id(self):
        return str(self.id)

def get_user_by_username(username):
    conn = sqlite3.connect('ecommerce.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM Users WHERE Username = ?', (username,))
    user = cursor.fetchone()
    conn.close()
    return user

def create_user(username, email, password, role):
    conn = sqlite3.connect('ecommerce.db')
    cursor = conn.cursor()
    hashed_password = generate_password_hash(password)
    try:
        cursor.execute('''
            INSERT INTO Users (Username, Password, Email, Role) 
            VALUES (?, ?, ?, ?)
        ''', (username, hashed_password, email, role))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()

@users_bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('products.products'))
        
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        role = request.form['role']
        
        if get_user_by_username(username):
            flash('Username already exists! Please choose a different one.', 'error')
            return render_template('users/register.html')
        
        if create_user(username, email, password, role):
            flash('Registration successful! Please login to continue.', 'success')
            return redirect(url_for('users.login'))
        else:
            flash('Registration failed! Please try again.', 'error')
    
    return render_template('users/register.html')

@users_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('products.products'))
        
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        user_data = get_user_by_username(username)
        if user_data and check_password_hash(user_data[2], password):
            user = User(user_data[0], user_data[1], user_data[3], user_data[4])
            login_user(user)
            flash(f'Welcome back, {username}!', 'success')
            
            # Redirect based on role
            if user.role == 'Admin':
                return redirect(url_for('users.dashboard'))
            elif user.role == 'Seller':
                return redirect(url_for('products.manage_products'))
            else:
                return redirect(url_for('products.products'))
        else:
            flash('Invalid username or password! Please try again.', 'error')
    
    return render_template('users/login.html')

@users_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out successfully!', 'success')
    return redirect(url_for('users.login'))

@users_bp.route('/dashboard')
@login_required
def dashboard():
    if current_user.role != 'Admin':
        flash('Access denied! Admin privileges required.', 'error')
        return redirect(url_for('products.products'))
    
    conn = sqlite3.connect('ecommerce.db')
    cursor = conn.cursor()
    
    # Get user statistics
    cursor.execute('SELECT COUNT(*) FROM Users')
    total_users = cursor.fetchone()[0]
    
    cursor.execute('SELECT COUNT(*) FROM Products')
    total_products = cursor.fetchone()[0]
    
    cursor.execute('SELECT COUNT(*) FROM Orders')
    total_orders = cursor.fetchone()[0]
    
    # Get recent orders
    cursor.execute('''
        SELECT o.OrderID, u.Username, p.Name, o.Quantity, o.OrderDate, o.Status
        FROM Orders o 
        JOIN Users u ON o.UserID = u.UserID 
        JOIN Products p ON o.ProductID = p.ProductID 
        ORDER BY o.OrderDate DESC LIMIT 5
    ''')
    recent_orders = cursor.fetchall()
    
    conn.close()
    
    return render_template('users/dashboard.html', 
                         total_users=total_users,
                         total_products=total_products,
                         total_orders=total_orders,
                         recent_orders=recent_orders)

@users_bp.route('/profile')
@login_required
def profile():
    return render_template('users/profile.html', user=current_user)