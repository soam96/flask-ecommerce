# Flask E-Commerce Web Application

A complete Flask-based E-Commerce web application with user authentication, product management, and order processing.

## 🚀 Features

### User Roles
- **Customer**: Browse products, place orders, view order history
- **Seller**: Add/update products, manage inventory
- **Admin**: Manage users, products, and orders

### Core Functionality
- User registration and login with role-based access
- Product catalog with search functionality
- Shopping cart and order placement
- Order management system
- Password hashing for security
- Responsive web design

## 🛠️ Installation & Setup

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/flask-ecommerce.git
cd flask-ecommerce
📁 Project Structure
text
flask-ecommerce/
│── app.py                 # Main application file
│── run.py                 # Application runner
│── requirements.txt       # Python dependencies
│── README.md             # Project documentation
│── .gitignore            # Git ignore rules
│── .env.example          # Environment variables template
├── routes/               # Application routes
│   ├── users/           # User authentication routes
│   ├── products/        # Product management routes
│   └── orders/          # Order processing routes
├── templates/           # HTML templates
│   ├── base.html       # Base template
│   ├── users/          # User-related templates
│   ├── products/       # Product-related templates
│   └── orders/         # Order-related templates
└── static/             # Static files
    ├── css/           # Stylesheets
    └── images/        # Product images
🗄️ Database Schema
Users Table
UserID (Primary Key)

Username (Unique)

Password (Hashed)

Email

Role (Customer/Seller/Admin)

Products Table
ProductID (Primary Key)

Name

Description

Price

Stock

SellerID (Foreign Key)

Image

Orders Table
OrderID (Primary Key)

UserID (Foreign Key)

ProductID (Foreign Key)

Quantity

OrderDate

Status

🎯 API Routes
Authentication Routes
GET/POST /users/register - User registration

GET/POST /users/login - User login

GET /users/logout - User logout

GET /users/dashboard - Admin dashboard

Product Routes
GET /products/ - Browse products

GET/POST /products/add - Add new product (Seller/Admin)

GET /products/manage - Manage products (Seller/Admin)

GET/POST /products/update/<id> - Update product

GET /products/delete/<id> - Delete product

Order Routes
GET/POST /orders/place/<product_id> - Place order

GET /orders/history - Order history

GET /orders/manage - Manage orders (Admin)

POST /orders/update_status/<order_id> - Update order status

🔧 Configuration
Environment Variables
SECRET_KEY: Flask secret key for session security

DEBUG: Enable/disable debug mode

PORT: Application port (default: 5000)

Database
The application uses SQLite by default. The database file (ecommerce.db) is automatically created with sample data on first run.

🚀 Deployment
Local Development
bash
python run.py
Production Deployment
For production deployment, consider:

Setting DEBUG=False

Using a production WSGI server (Gunicorn)

Using a production database (PostgreSQL)

Setting up proper environment variables

🤝 Contributing
Fork the repository

Create a feature branch (git checkout -b feature/AmazingFeature)

Commit your changes (git commit -m 'Add some AmazingFeature')

Push to the branch (git push origin feature/AmazingFeature)

Open a Pull Request

📝 License
This project is licensed under the MIT License - see the LICENSE file for details.

🆘 Support
If you encounter any issues:

Check the troubleshooting section below

Create an issue in the GitHub repository

Provide detailed information about the problem

🔮 Future Enhancements
Payment gateway integration

Email notifications

Product categories and filters

Shopping cart functionality

Product reviews and ratings

Image upload functionality

Order tracking system

Inventory management alerts

REST API endpoints

Mobile app companion

🙏 Acknowledgments
Flask framework and community

Bootstrap for UI components

Contributors and testers
