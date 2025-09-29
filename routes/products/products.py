from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
import sqlite3

products_bp = Blueprint('products', __name__, url_prefix='/products')

def get_products(search=''):
    conn = sqlite3.connect('ecommerce.db')
    cursor = conn.cursor()
    
    if search:
        cursor.execute('''
            SELECT p.*, u.Username 
            FROM Products p 
            JOIN Users u ON p.SellerID = u.UserID 
            WHERE p.Name LIKE ? OR p.Description LIKE ?
            ORDER BY p.ProductID DESC
        ''', (f'%{search}%', f'%{search}%'))
    else:
        cursor.execute('''
            SELECT p.*, u.Username 
            FROM Products p 
            JOIN Users u ON p.SellerID = u.UserID 
            ORDER BY p.ProductID DESC
        ''')
    
    products = cursor.fetchall()
    conn.close()
    return products

def get_product_by_id(product_id):
    conn = sqlite3.connect('ecommerce.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM Products WHERE ProductID = ?', (product_id,))
    product = cursor.fetchone()
    conn.close()
    return product

@products_bp.route('/')
def products():
    search = request.args.get('search', '')
    products_list = get_products(search)
    return render_template('products/products.html', products=products_list)

@products_bp.route('/add', methods=['GET', 'POST'])
@login_required
def add_product():
    if current_user.role not in ['Seller', 'Admin']:
        flash('Access denied! Only sellers can add products.', 'error')
        return redirect(url_for('products.products'))
    
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        price = float(request.form['price'])
        stock = int(request.form['stock'])
        image = request.form.get('image', 'default.jpg')
        
        conn = sqlite3.connect('ecommerce.db')
        cursor = conn.cursor()
        try:
            cursor.execute('''
                INSERT INTO Products (Name, Description, Price, Stock, SellerID, Image) 
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (name, description, price, stock, current_user.id, image))
            conn.commit()
            flash('Product added successfully!', 'success')
            return redirect(url_for('products.manage_products'))
        except Exception as e:
            flash(f'Error adding product: {str(e)}', 'error')
        finally:
            conn.close()
    
    return render_template('products/add_product.html')

@products_bp.route('/manage')
@login_required
def manage_products():
    if current_user.role not in ['Seller', 'Admin']:
        flash('Access denied!', 'error')
        return redirect(url_for('products.products'))
    
    conn = sqlite3.connect('ecommerce.db')
    cursor = conn.cursor()
    
    if current_user.role == 'Admin':
        cursor.execute('''
            SELECT p.*, u.Username 
            FROM Products p 
            JOIN Users u ON p.SellerID = u.UserID
            ORDER BY p.ProductID DESC
        ''')
    else:
        cursor.execute('''
            SELECT p.*, u.Username 
            FROM Products p 
            JOIN Users u ON p.SellerID = u.UserID 
            WHERE p.SellerID = ?
            ORDER BY p.ProductID DESC
        ''', (current_user.id,))
    
    products = cursor.fetchall()
    conn.close()
    
    return render_template('products/manage_products.html', products=products)

@products_bp.route('/update/<int:product_id>', methods=['GET', 'POST'])
@login_required
def update_product(product_id):
    product = get_product_by_id(product_id)
    
    if not product:
        flash('Product not found!', 'error')
        return redirect(url_for('products.manage_products'))
    
    # Check if user has permission to update this product
    if current_user.role != 'Admin' and product[5] != current_user.id:
        flash('Access denied! You can only update your own products.', 'error')
        return redirect(url_for('products.manage_products'))
    
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        price = float(request.form['price'])
        stock = int(request.form['stock'])
        image = request.form.get('image', product[6] if product[6] else 'default.jpg')
        
        conn = sqlite3.connect('ecommerce.db')
        cursor = conn.cursor()
        try:
            cursor.execute('''
                UPDATE Products 
                SET Name = ?, Description = ?, Price = ?, Stock = ?, Image = ? 
                WHERE ProductID = ?
            ''', (name, description, price, stock, image, product_id))
            conn.commit()
            flash('Product updated successfully!', 'success')
            return redirect(url_for('products.manage_products'))
        except Exception as e:
            flash(f'Error updating product: {str(e)}', 'error')
        finally:
            conn.close()
    
    return render_template('products/update_product.html', product=product)

@products_bp.route('/delete/<int:product_id>')
@login_required
def delete_product(product_id):
    product = get_product_by_id(product_id)
    
    if not product:
        flash('Product not found!', 'error')
        return redirect(url_for('products.manage_products'))
    
    if current_user.role != 'Admin' and product[5] != current_user.id:
        flash('Access denied! You can only delete your own products.', 'error')
        return redirect(url_for('products.manage_products'))
    
    conn = sqlite3.connect('ecommerce.db')
    cursor = conn.cursor()
    try:
        # Check if product has orders
        cursor.execute('SELECT COUNT(*) FROM Orders WHERE ProductID = ?', (product_id,))
        order_count = cursor.fetchone()[0]
        
        if order_count > 0:
            flash('Cannot delete product with existing orders!', 'error')
            return redirect(url_for('products.manage_products'))
        
        cursor.execute('DELETE FROM Products WHERE ProductID = ?', (product_id,))
        conn.commit()
        flash('Product deleted successfully!', 'success')
    except Exception as e:
        flash(f'Error deleting product: {str(e)}', 'error')
    finally:
        conn.close()
    
    return redirect(url_for('products.manage_products'))

@products_bp.route('/view/<int:product_id>')
def view_product(product_id):
    product = get_product_by_id(product_id)
    if not product:
        flash('Product not found!', 'error')
        return redirect(url_for('products.products'))
    
    # Get seller info
    conn = sqlite3.connect('ecommerce.db')
    cursor = conn.cursor()
    cursor.execute('SELECT Username FROM Users WHERE UserID = ?', (product[5],))
    seller = cursor.fetchone()
    conn.close()
    
    return render_template('products/view_product.html', product=product, seller=seller[0] if seller else 'Unknown')