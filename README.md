Flask E-Commerce Web Application
A complete, feature-rich Flask-based E-Commerce web application with user authentication, product management, and order processing system. This project demonstrates full-stack web development skills with Python, Flask, SQLite, and Bootstrap.

https://img.shields.io/badge/Flask-2.3.3-green
https://img.shields.io/badge/Python-3.8%252B-blue
https://img.shields.io/badge/Bootstrap-5.1-purple
https://img.shields.io/badge/SQLite-Database-lightgrey

🎯 Live Demo
🌐 Application URL: [Coming Soon]
📚 API Documentation: View API Docs

🚀 Features
👥 Multi-Role User System
👤 Customers: Browse products, place orders, view order history

🏪 Sellers: Add/update products, manage inventory, track sales

👑 Admin: Full platform management, user management, order oversight

🛍️ E-Commerce Features
📦 Product Catalog with search and filtering

🛒 Shopping Cart functionality

💳 Order Management system

📊 Inventory Management with stock tracking

👤 User Authentication with secure password hashing

📱 Responsive Design for all devices

🔒 Security Features
Password hashing with Werkzeug

Session management with Flask-Login

Role-based access control

SQL injection prevention

XSS protection

📸 Screenshots
Login Page	Product Catalog	Admin Dashboard
https://via.placeholder.com/400x250?text=Login+Page	https://via.placeholder.com/400x250?text=Product+Catalog	https://via.placeholder.com/400x250?text=Admin+Dashboard
Order Management	Product Management	Mobile View
https://via.placeholder.com/400x250?text=Order+Management	https://via.placeholder.com/400x250?text=Product+Management	https://via.placeholder.com/400x250?text=Mobile+View
🛠️ Technology Stack
Backend
🖥️ Framework: Flask 2.3.3

🔐 Authentication: Flask-Login

🔒 Security: Werkzeug

🗄️ Database: SQLite3

🔄 ORM: SQLite3 (Raw SQL with parameterized queries)

Frontend
🎨 Styling: Bootstrap 5.1

📱 Responsive: Mobile-first design

⚡ Icons: Font Awesome

📄 Templates: Jinja2 templating engine

Development Tools
🐍 Python: 3.8+

🔧 Version Control: Git

📦 Package Management: pip

⚙️ IDE: VS Code (recommended)

📁 Project Structure
text
flask-ecommerce/
│
├── 📄 app.py                 # Main application entry point
├── 📄 run.py                 # Development server runner
├── 📄 requirements.txt       # Python dependencies
├── 📄 .env.example          # Environment variables template
├── 📄 .gitignore            # Git ignore rules
│
├── 📁 routes/               # Application route handlers
│   ├── 📄 __init__.py
│   ├── 📁 users/           # User authentication routes
│   │   ├── 📄 __init__.py
│   │   └── 📄 users.py     # Login, register, dashboard
│   ├── 📁 products/        # Product management routes
│   │   ├── 📄 __init__.py
│   │   └── 📄 products.py  # CRUD operations, catalog
│   └── 📁 orders/          # Order processing routes
│       ├── 📄 __init__.py
│       └── 📄 orders.py    # Order placement, management
│
├── 📁 templates/           # HTML templates
│   ├── 📄 base.html       # Base template with navigation
│   ├── 📁 users/          # User-related templates
│   │   ├── 📄 login.html
│   │   ├── 📄 register.html
│   │   └── 📄 dashboard.html
│   ├── 📁 products/       # Product-related templates
│   │   ├── 📄 products.html
│   │   ├── 📄 add_product.html
│   │   ├── 📄 update_product.html
│   │   └── 📄 manage_products.html
│   └── 📁 orders/         # Order-related templates
│       ├── 📄 place_order.html
│       ├── 📄 order_history.html
│       └── 📄 manage_orders.html
│
└── 📁 static/             # Static assets
    ├── 📁 css/
    │   └── 📄 style.css   # Custom styles
    └── 📁 images/         # Product images
        ├── 📄 mobile1.jpg
        ├── 📄 mobile2.jpg
        ├── 📄 headphone1.jpg
        └── ... (10+ sample images)
🚀 Quick Start
Prerequisites
🐍 Python 3.8 or higher

📦 pip (Python package manager)

🌐 Web browser

💻 Git (for version control)

Installation & Setup
1. 📥 Clone the Repository
bash
git clone https://github.com/YOUR_USERNAME/flask-ecommerce.git
cd flask-ecommerce
2. 🏗️ Create Virtual Environment
bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
3. 📦 Install Dependencies
bash
pip install -r requirements.txt
4. ⚙️ Environment Configuration
bash
# Copy environment template
cp .env.example .env

# Edit .env file with your preferred editor
# Add your configuration:
SECRET_KEY=your-super-secret-key-here
DEBUG=True
PORT=5000
5. 🗄️ Database Initialization
The SQLite database is automatically created with sample data on first run.

6. 🎯 Run the Application
bash
# Method 1: Using run.py (Recommended for development)
python run.py

# Method 2: Using flask command
flask run

# Method 3: Direct execution
python app.py
7. 🌐 Access the Application
Open your web browser and navigate to:

text
http://localhost:5000
👤 Default Accounts
🔧 Administrator Account
Username: admin

Password: admin123

Role: Admin (Full system access)

Permissions: User management, product oversight, order management

🎭 Demo User Roles
Register new accounts with different roles:

Role	Permissions	Use Case
Customer	Browse products, place orders, view history	End users
Seller	Add products, manage inventory, track sales	Business owners
Admin	Full system access	Platform administrators
📊 Database Schema
🗃️ Users Table
sql
CREATE TABLE Users (
    UserID INTEGER PRIMARY KEY AUTOINCREMENT,
    Username TEXT UNIQUE NOT NULL,
    Password TEXT NOT NULL,
    Email TEXT NOT NULL,
    Role TEXT CHECK(Role IN ('Customer','Seller','Admin')) NOT NULL
);
🗃️ Products Table
sql
CREATE TABLE Products (
    ProductID INTEGER PRIMARY KEY AUTOINCREMENT,
    Name TEXT NOT NULL,
    Description TEXT,
    Price REAL NOT NULL,
    Stock INTEGER NOT NULL,
    SellerID INTEGER NOT NULL,
    Image TEXT,
    FOREIGN KEY (SellerID) REFERENCES Users(UserID)
);
🗃️ Orders Table
sql
CREATE TABLE Orders (
    OrderID INTEGER PRIMARY KEY AUTOINCREMENT,
    UserID INTEGER NOT NULL,
    ProductID INTEGER NOT NULL,
    Quantity INTEGER NOT NULL,
    OrderDate DATETIME DEFAULT CURRENT_TIMESTAMP,
    Status TEXT DEFAULT 'Pending',
    FOREIGN KEY (UserID) REFERENCES Users(UserID),
    FOREIGN KEY (ProductID) REFERENCES Products(ProductID)
);
📋 API Documentation
🔐 Authentication Routes
Method	Endpoint	Description	Access
GET	/users/register	Registration form	Public
POST	/users/register	Create new account	Public
GET	/users/login	Login form	Public
POST	/users/login	User authentication	Public
GET	/users/logout	User logout	Authenticated
GET	/users/dashboard	Admin dashboard	Admin only
📦 Product Routes
Method	Endpoint	Description	Access
GET	/products/	Browse products	Public
GET	/products/add	Add product form	Seller/Admin
POST	/products/add	Create new product	Seller/Admin
GET	/products/manage	Manage products	Seller/Admin
GET	/products/update/<id>	Update product form	Owner/Admin
POST	/products/update/<id>	Update product	Owner/Admin
GET	/products/delete/<id>	Delete product	Owner/Admin
📋 Order Routes
Method	Endpoint	Description	Access
GET	/orders/place/<product_id>	Order form	Customer
POST	/orders/place/<product_id>	Place order	Customer
GET	/orders/history	Order history	Authenticated
GET	/orders/manage	Manage orders	Admin only
POST	/orders/update_status/<id>	Update order status	Admin only
🎯 Usage Guide
For Customers 🛍️
Register/Login with Customer role

Browse products in the catalog

Search products using the search bar

Place orders by clicking "Buy Now"

View order history in your profile

For Sellers 🏪
Register/Login with Seller role

Add products through the management panel

Manage inventory and update stock levels

Track sales through the order system

For Administrators 👑
Login with Admin credentials

Access dashboard for platform overview

Manage all users, products, and orders

Monitor system performance and metrics

⚙️ Configuration
Environment Variables
Create a .env file in the root directory:

env
# Flask Configuration
SECRET_KEY=your-super-secret-key-change-in-production
DEBUG=True
PORT=5000

# Database Configuration
DATABASE_URL=sqlite:///ecommerce.db
Customization Options
🖼️ Product Images: Add images to static/images/ directory

🎨 Styling: Modify static/css/style.css

📊 Database: Switch to PostgreSQL/MySQL in production

🔐 Authentication: Integrate OAuth providers

🚀 Deployment
Local Development
bash
python run.py
Production Deployment
Option 1: Traditional VPS
bash
# Install production WSGI server
pip install gunicorn

# Run with gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
Option 2: Docker Deployment
dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app:app"]
Option 3: Platform as a Service
Heroku: Use Procfile and Heroku CLI

PythonAnywhere: Upload via Git or ZIP

AWS Elastic Beanstalk: Use EB CLI

Google App Engine: Use app.yaml

Production Checklist
Set DEBUG=False

Use strong SECRET_KEY

Configure production database

Set up proper logging

Configure static file serving

Set up SSL/HTTPS

Configure backup strategy

🧪 Testing
Manual Testing Checklist
User registration and login

Product CRUD operations

Order placement and management

Role-based access control

Form validation and error handling

Responsive design on mobile devices

Automated Testing (Future Enhancement)
bash
# Install testing dependencies
pip install pytest flask-testing

# Run tests
pytest tests/
🐛 Troubleshooting
Common Issues
1. Port Already in Use
bash
# Find and kill process using port 5000
lsof -ti:5000 | xargs kill -9

# Or use different port
python run.py --port 5001
2. Database Issues
bash
# Delete and recreate database
rm ecommerce.db
python app.py
3. Module Not Found
bash
# Reinstall dependencies
pip install -r requirements.txt

# Check Python path
python -c "import flask; print(flask.__file__)"
4. Authentication Errors
Verify password hashing is working

Check user role assignments

Verify session configuration

Debug Mode
Enable debug mode for detailed error messages:

python
app.config['DEBUG'] = True
🤝 Contributing
We welcome contributions! Please follow these steps:

1. Fork the Repository
Click "Fork" on GitHub

Clone your fork locally

Create a feature branch

2. Development Setup
bash
git clone https://github.com/YOUR_USERNAME/flask-ecommerce.git
cd flask-ecommerce
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
3. Make Changes
Follow PEP 8 style guide

Add comments for complex logic

Update documentation as needed

Test your changes thoroughly

4. Submit Pull Request
Commit your changes

Push to your fork

Create PR with detailed description

Wait for code review

Contribution Areas
🐛 Bug fixes

✨ New features

📚 Documentation improvements

🎨 UI/UX enhancements

🧪 Test coverage

🔒 Security improvements

📄 License
This project is licensed under the MIT License - see the LICENSE file for details.

text
MIT License

Copyright (c) 2024 Flask E-Commerce

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.
🙏 Acknowledgments
Technologies Used
Flask - The web framework used

Bootstrap - Frontend component library

SQLite - Database engine

Font Awesome - Icon library

Inspiration
Modern e-commerce platforms

Clean admin dashboard designs

User-friendly interface patterns

Special Thanks
Flask community for excellent documentation

Contributors and testers

Open source community

📞 Support
Getting Help
📖 Documentation: Check this README first

🐛 Issues: Create a GitHub issue

💬 Discussions: Use GitHub Discussions

📧 Email: Contact maintainers

Resources
Flask Documentation

Bootstrap Documentation

SQLite Documentation

🔮 Roadmap
Version 1.1 (Planned)
Payment gateway integration

Email notifications

Product categories and filters

Shopping cart functionality

Version 1.2 (Future)
Product reviews and ratings

Image upload functionality

Order tracking system

Inventory management alerts

Version 2.0 (Long-term)
REST API endpoints

Mobile app companion

Multi-vendor marketplace

Advanced analytics

<div align="center">
⭐ Don't forget to star this repository if you find it helpful!

Built with ❤️ using Flask and Bootstrap

</div>
