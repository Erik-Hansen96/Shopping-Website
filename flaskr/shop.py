from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort


from flaskr.db import get_db

bp = Blueprint('shop', __name__)

@bp.route('/')
def index():
    return render_template('base.html')

@bp.route('/product_detail/<int:product_id>')
def product_detail(product_id):
    with get_db() as db:
        product = db.execute('SELECT * FROM products WHERE id = ?', (product_id,)).fetchone()
        
    return render_template('shop/product_detail.html', product=product)

@bp.route('/products_list/<category>')
@bp.route('/products_list/')
def list(category=None):
    with get_db() as db:
        if category:
            query = 'SELECT * FROM products WHERE category = ?'
            products = db.execute(query, (category,)).fetchall()
        else:
            query = 'SELECT * FROM products'
            products = db.execute(query).fetchall()
    return render_template('shop/products_list.html', products=products, category=category)
    


@bp.route('/submit', methods=['POST'])
def submit():
    return render_template('shop/contactSuccess.html')

