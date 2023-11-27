import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from flaskr.db import get_db

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None

        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'

        if error is None:
            try:
                db.execute(
                    "INSERT INTO user (username, password) VALUES (?, ?)",
                    (username, generate_password_hash(password)),
                )
                db.commit()
            except db.IntegrityError:
                error = f"User {username} is already registered."
            else:
                return redirect(url_for("auth.login"))

        flash(error)

    return render_template('auth/register.html')

@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None
        user = db.execute(
            'SELECT * FROM user WHERE username = ?', (username,)
        ).fetchone()

        if user is None:
            error = 'Incorrect username.'
        elif not check_password_hash(user['password'], password):
            error = 'Incorrect password.'

        if error is None:
            session.clear()
            session['user_id'] = user['id']
            return redirect(url_for('index'))

        flash(error)

    return render_template('auth/login.html')

@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = get_db().execute(
            'SELECT * FROM user WHERE id = ?', (user_id,)
        ).fetchone()

@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

@bp.route('/add_to_cart/<int:product_id>', methods=['POST'])
def add_to_cart(product_id):
    user_id = session.get('user_id')
    if user_id:
        db = get_db()
        quantity = int(request.form.get('quantity',1))
        find_product = db.execute('SELECT * FROM cart WHERE user_id = ? AND product_id = ?', (user_id, product_id)).fetchone()
        if find_product:
            update_quantity = find_product['quantity'] + quantity
            db.execute('UPDATE cart SET quantity = ? WHERE user_id = ? AND product_id = ?', (update_quantity, user_id, product_id))
        else:
            db.execute('INSERT INTO cart (user_id, product_id, quantity) VALUES (?, ?, ?)', (user_id, product_id, quantity))
        db.commit()
        
        return redirect(url_for('auth.shopping_cart'))
    else:
        return redirect(url_for('auth.login'))
    
@bp.route('/remove_from_cart/<int:product_id>', methods=['GET', 'POST'])
def remove_from_cart(product_id):
    user_id = session.get('user_id')
    if user_id:
        db = get_db()
        db.execute('DELETE FROM cart WHERE user_id = ? AND product_id = ?', (user_id, product_id))
        db.commit()
        
        return redirect(url_for('auth.shopping_cart'))
    else:
        return redirect(url_for('auth.login'))
    
@bp.route('/checkoutConfirmation')
def checkoutConfirmation():
    user_id = session.get('user_id')
    if user_id:
        db = get_db()
        db.execute('DELETE FROM cart WHERE user_id = ?', (user_id,))
        db.commit()
        return render_template('shop/checkoutConfirmation.html')
    else:
        return redirect(url_for('auth.login'))
    
@bp.route('/shopping_cart')
def shopping_cart():
    user_id = session.get('user_id')
    if user_id is None:
        return redirect(url_for('auth.login'))
    else:
        db = get_db()
        query = '''
            SELECT 
                products.id, 
                products.name, 
                products.price, 
                products.image_path, 
                CART.quantity, 
                ROUND(products.price * cart.quantity, 2) AS subtotal 
            FROM 
                cart 
            JOIN 
                products ON cart.product_id = products.id 
            WHERE 
                user_id = ?
        '''
        cart_items = db.execute(query, (user_id,)).fetchall()
        total_price = 0
        for product in cart_items:
            total_price += product['subtotal']
        return render_template('shop/shopping_cart.html', cart_items=cart_items, total_price=total_price)

@bp.route('/checkout', methods=['GET', 'POST'])
def checkout():
    user_id = session.get('user_id')
    if user_id is None:
        return redirect(url_for('auth.login'))
    else:
        db = get_db()

        if request.method == 'POST':
            selected_shipping = request.form.get('shipping')
            if selected_shipping == 'standard':
                shipping_cost = 5
            elif selected_shipping == 'express':
                shipping_cost = 18.95
            elif selected_shipping == 'overnight':
                shipping_cost = 21.95
            else:
                shipping_cost = 5

        else:
            shipping_cost = 5
            selected_shipping = 'standard'

        query = '''
            SELECT 
                products.id, 
                products.name, 
                products.price, 
                products.image_path, 
                CART.quantity, 
                ROUND(products.price * cart.quantity, 2) AS subtotal 
            FROM 
                cart 
            JOIN 
                products ON cart.product_id = products.id 
            WHERE 
                user_id = ?
        '''
        cart_items = db.execute(query, (user_id,)).fetchall()
        total_price = 0     
        for product in cart_items:
            total_price += product['subtotal']
        return render_template('shop/checkout.html', cart_items=cart_items, total_price=total_price, shipping_cost=shipping_cost, selected_shipping=selected_shipping)
