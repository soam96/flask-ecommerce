from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
import sqlite3
from datetime import datetime

orders_bp = Blueprint('orders', __name__, url_prefix='/orders')

def get_order_by_id(order_id):
    conn = sqlite3.connect('ecommerce.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM Orders WHERE OrderID = ?', (order_id,))
    order = cursor.fetchone()
    conn.close()
    return order

@orders_bp.route('/place/<int:product_id>', methods=['GET', 'POST'])
@login_required
def place_order(product_id):
    if current_user.role != 'Customer':
        flash('Only customers can place orders!', 'error')
        return redirect(url_for('products.products'))
    
    conn = sqlite3.connect('ecommerce.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM Products WHERE ProductID = ?', (product_id,))
    product = cursor.fetchone()
    
    if not product:
        flash('Product not found!', 'error')
        conn.close()
        return redirect(url_for('products.products'))
    
    if request.method == 'POST':
        quantity = int(request.form['quantity'])
        
        if quantity <= 0:
            flash('Quantity must be greater than 0!', 'error')
            conn.close()
            return redirect(url_for('orders.place_order', product_id=product_id))
        
        if quantity > product[4]:  # Check stock
            flash('Insufficient stock! Available: ' + str(product[4]), 'error')
            conn.close()
            return redirect(url_for('orders.place_order', product_id=product_id))
        
        try:
            # Create order
            cursor.execute('''
                INSERT INTO Orders (UserID, ProductID, Quantity, Status) 
                VALUES (?, ?, ?, 'Pending')
            ''', (current_user.id, product_id, quantity))
            
            # Update stock
            cursor.execute('''
                UPDATE Products SET Stock = Stock - ? WHERE ProductID = ?
            ''', (quantity, product_id))
            
            conn.commit()
            flash('Order placed successfully!', 'success')
            return redirect(url_for('orders.order_history'))
        except Exception as e:
            conn.rollback()
            flash(f'Error placing order: {str(e)}', 'error')
        finally:
            conn.close()
    else:
        conn.close()
    
    return render_template('orders/place_order.html', product=product)

@orders_bp.route('/history')
@login_required
def order_history():
    conn = sqlite3.connect('ecommerce.db')
    cursor = conn.cursor()
    
    if current_user.role == 'Admin':
        cursor.execute('''
            SELECT o.OrderID, u.Username, p.Name, p.Price, o.Quantity, 
                   (p.Price * o.Quantity) as Total, o.OrderDate, o.Status
            FROM Orders o 
            JOIN Users u ON o.UserID = u.UserID 
            JOIN Products p ON o.ProductID = p.ProductID 
            ORDER BY o.OrderDate DESC
        ''')
    else:
        cursor.execute('''
            SELECT o.OrderID, u.Username, p.Name, p.Price, o.Quantity, 
                   (p.Price * o.Quantity) as Total, o.OrderDate, o.Status
            FROM Orders o 
            JOIN Users u ON o.UserID = u.UserID 
            JOIN Products p ON o.ProductID = p.ProductID 
            WHERE o.UserID = ? 
            ORDER BY o.OrderDate DESC
        ''', (current_user.id,))
    
    orders = cursor.fetchall()
    conn.close()
    
    return render_template('orders/order_history.html', orders=orders)

@orders_bp.route('/manage')
@login_required
def manage_orders():
    if current_user.role != 'Admin':
        flash('Access denied! Admin privileges required.', 'error')
        return redirect(url_for('products.products'))
    
    conn = sqlite3.connect('ecommerce.db')
    cursor = conn.cursor()
    cursor.execute('''
        SELECT o.OrderID, u.Username, p.Name, o.Quantity, o.OrderDate, o.Status
        FROM Orders o 
        JOIN Users u ON o.UserID = u.UserID 
        JOIN Products p ON o.ProductID = p.ProductID 
        ORDER BY o.OrderDate DESC
    ''')
    orders = cursor.fetchall()
    conn.close()
    
    return render_template('orders/manage_orders.html', orders=orders)

@orders_bp.route('/update_status/<int:order_id>', methods=['POST'])
@login_required
def update_order_status(order_id):
    if current_user.role != 'Admin':
        return jsonify({'error': 'Access denied! Admin privileges required.'}), 403
    
    order = get_order_by_id(order_id)
    if not order:
        return jsonify({'error': 'Order not found!'}), 404
    
    new_status = request.json.get('status')
    valid_statuses = ['Pending', 'Processing', 'Shipped', 'Delivered', 'Cancelled']
    
    if new_status not in valid_statuses:
        return jsonify({'error': 'Invalid status!'}), 400
    
    conn = sqlite3.connect('ecommerce.db')
    cursor = conn.cursor()
    try:
        cursor.execute('''
            UPDATE Orders SET Status = ? WHERE OrderID = ?
        ''', (new_status, order_id))
        conn.commit()
        return jsonify({'success': 'Order status updated successfully!'})
    except Exception as e:
        return jsonify({'error': f'Database error: {str(e)}'}), 500
    finally:
        conn.close()

@orders_bp.route('/cancel/<int:order_id>')
@login_required
def cancel_order(order_id):
    order = get_order_by_id(order_id)
    
    if not order:
        flash('Order not found!', 'error')
        return redirect(url_for('orders.order_history'))
    
    # Check if user owns the order or is admin
    if current_user.role != 'Admin' and order[1] != current_user.id:
        flash('Access denied!', 'error')
        return redirect(url_for('orders.order_history'))
    
    if order[5] in ['Delivered', 'Cancelled']:
        flash('Cannot cancel this order!', 'error')
        return redirect(url_for('orders.order_history'))
    
    conn = sqlite3.connect('ecommerce.db')
    cursor = conn.cursor()
    try:
        # Update order status
        cursor.execute('UPDATE Orders SET Status = "Cancelled" WHERE OrderID = ?', (order_id,))
        
        # Restore stock if order was processing
        if order[5] in ['Pending', 'Processing']:
            cursor.execute('''
                UPDATE Products SET Stock = Stock + ? 
                WHERE ProductID = ?
            ''', (order[3], order[2]))
        
        conn.commit()
        flash('Order cancelled successfully!', 'success')
    except Exception as e:
        conn.rollback()
        flash(f'Error cancelling order: {str(e)}', 'error')
    finally:
        conn.close()
    
    return redirect(url_for('orders.order_history'))

@orders_bp.route('/details/<int:order_id>')
@login_required
def order_details(order_id):
    conn = sqlite3.connect('ecommerce.db')
    cursor = conn.cursor()
    
    if current_user.role == 'Admin':
        cursor.execute('''
            SELECT o.*, u.Username, u.Email, p.Name, p.Description, p.Price, p.Image
            FROM Orders o 
            JOIN Users u ON o.UserID = u.UserID 
            JOIN Products p ON o.ProductID = p.ProductID 
            WHERE o.OrderID = ?
        ''', (order_id,))
    else:
        cursor.execute('''
            SELECT o.*, u.Username, u.Email, p.Name, p.Description, p.Price, p.Image
            FROM Orders o 
            JOIN Users u ON o.UserID = u.UserID 
            JOIN Products p ON o.ProductID = p.ProductID 
            WHERE o.OrderID = ? AND o.UserID = ?
        ''', (order_id, current_user.id))
    
    order_details = cursor.fetchone()
    conn.close()
    
    if not order_details:
        flash('Order not found!', 'error')
        return redirect(url_for('orders.order_history'))
    
    return render_template('orders/order_details.html', order=order_details)