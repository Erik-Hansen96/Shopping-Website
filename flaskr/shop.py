from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from flaskr.auth import login_required
from flaskr.db import get_db

bp = Blueprint('shop', __name__)

@bp.route('/')
def index():
    db = get_db()
    posts = db.execute(
        'SELECT p.id, title, body, created, author_id, username'
        ' FROM post p JOIN user u ON p.author_id = u.id'
        ' ORDER BY created DESC'
    ).fetchall()
    return render_template('base.html', posts=posts)

"""@bp.route('/shopping_cart')
def shopping_cart():
    if g.user is None:
        return redirect(url_for('auth.login'))
    user_id = g.get('user_id')
    db = get_db()
    cart_items = db.execute('SELECT products.name, products.price, CART.quantity FROM cart JOIN products ON cart.product_id = products.id WHERE user_id = ?', (user_id,)).fetchall()
    for item in cart_items:
            print("Product name:", item['name'])
    return render_template('shop/shopping_cart.html', cart_items=cart_items)"""



@bp.route('/product_detail/<int:product_id>')
def product_detail(product_id):
    with get_db() as db:
        product = db.execute('SELECT * FROM products WHERE id = ?', (product_id,)).fetchone()
        
    return render_template('shop/product_detail.html', product=product)

@bp.route('/products_list/<category>')
def list(category):
    with get_db() as db:
        #products = db.execute('SELECT * FROM products WHERE category = ?', (category,)).fetchall()
        print("Category:", category)
        query = 'SELECT * FROM products WHERE category = ?'
        products = db.execute(query, (category,)).fetchall()
        for product in products:
            print("Product name:", product['name'])
    return render_template('shop/products_list.html', products=products, category=category)
    