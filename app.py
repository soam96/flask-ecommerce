from flask import Flask, render_template
from flask_login import LoginManager
import sqlite3
import os
from werkzeug.security import generate_password_hash

def init_db():
    """Initialize SQLite database with required tables"""
    conn = sqlite3.connect('ecommerce.db')
    cursor = conn.cursor()
    
    # Create Users table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Users (
            UserID INTEGER PRIMARY KEY AUTOINCREMENT,
            Username TEXT UNIQUE NOT NULL,
            Password TEXT NOT NULL,
            Email TEXT NOT NULL,
            Role TEXT CHECK(Role IN ('Customer','Seller','Admin')) NOT NULL
        )
    ''')
    
    # Create Products table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Products (
            ProductID INTEGER PRIMARY KEY AUTOINCREMENT,
            Name TEXT NOT NULL,
            Description TEXT,
            Price REAL NOT NULL,
            Stock INTEGER NOT NULL,
            SellerID INTEGER NOT NULL,
            Image TEXT,
            FOREIGN KEY (SellerID) REFERENCES Users(UserID)
        )
    ''')
    
    # Create Orders table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Orders (
            OrderID INTEGER PRIMARY KEY AUTOINCREMENT,
            UserID INTEGER NOT NULL,
            ProductID INTEGER NOT NULL,
            Quantity INTEGER NOT NULL,
            OrderDate DATETIME DEFAULT CURRENT_TIMESTAMP,
            Status TEXT DEFAULT 'Pending',
            FOREIGN KEY (UserID) REFERENCES Users(UserID),
            FOREIGN KEY (ProductID) REFERENCES Products(ProductID)
        )
    ''')
    
    # Insert default admin user with hashed password
    hashed_password = generate_password_hash('admin123')
    cursor.execute('''
        INSERT OR IGNORE INTO Users (Username, Password, Email, Role) 
        VALUES (?, ?, ?, ?)
    ''', ('admin', hashed_password, 'admin@ecommerce.com', 'Admin'))
    
    # Insert sample products
    sample_products = [
        ('iPhone 14', 'Latest Apple smartphone with advanced features', 999.99, 50, 'mobile1.jpg'),
        ('Samsung Galaxy S23', 'Powerful Android smartphone', 849.99, 30, 'mobile2.jpg'),
        ('Sony WH-1000XM4', 'Noise cancelling wireless headphones', 349.99, 25, 'headphone1.jpg'),
        ('Apple AirPods Pro', 'Wireless earbuds with active noise cancellation', 249.99, 40, 'headphone2.jpg'),
        ('MacBook Pro', '16-inch laptop for professionals', 2399.99, 15, 'laptop1.jpg'),
        ('Dell XPS 13', 'Compact and powerful laptop', 1199.99, 20, 'laptop2.jpg'),
        ('iPad Air', 'Versatile tablet for work and entertainment', 599.99, 35, 'tablet1.jpg'),
        ('Samsung Galaxy Tab', 'Android tablet with S Pen', 449.99, 25, 'tablet2.jpg'),
        ('Canon EOS R5', 'Professional mirrorless camera', 3899.99, 10, 'camera1.jpg'),
        ('Nikon Z7 II', 'High-resolution mirrorless camera', 2999.99, 12, 'camera2.jpg')
    ]
    
    cursor.executemany('''
        INSERT OR IGNORE INTO Products (Name, Description, Price, Stock, SellerID, Image) 
        VALUES (?, ?, ?, ?, 1, ?)
    ''', sample_products)
    
    conn.commit()
    conn.close()

def get_user_by_id(user_id):
    conn = sqlite3.connect('ecommerce.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM Users WHERE UserID = ?', (user_id,))
    user = cursor.fetchone()
    conn.close()
    return user

# Create Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = 'ecommerce-secret-key-2024'

# Initialize database
init_db()

# Initialize Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'users.login'
login_manager.login_message_category = 'info'

# Import blueprints after app creation to avoid circular imports
from routes.users.users import users_bp, User
from routes.products.products import products_bp
from routes.orders.orders import orders_bp

# User loader callback
@login_manager.user_loader
def load_user(user_id):
    user_data = get_user_by_id(user_id)
    if user_data:
        return User(user_data[0], user_data[1], user_data[3], user_data[4])
    return None

# Register blueprints
app.register_blueprint(users_bp)
app.register_blueprint(products_bp)
app.register_blueprint(orders_bp)

@app.route('/')
def home():
    return render_template('products/products.html')

@app.route('/about')
def about():
    return render_template('about.html')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)