import sqlite3

import click
from flask import current_app, g


def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row

    return g.db


def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()
        
def fill_products():
    db = get_db()
    products_info = [
        ('Backpack #1', 'backpacks', 'Description', 24.99, '../static/styles/images/backpacks/blue_bag.jpg'),
        ('Backpack #2', 'backpacks', 'Description', 24.99, '../static/styles/images/backpacks/darkgray_bag.jpg'),
        ('Backpack #3', 'backpacks', 'Description', 24.99, '../static/styles/images/backpacks/gray_bag.jpg'),
        ('Backpack #4', 'backpacks', 'Description', 24.99, '../static/styles/images/backpacks/gray2_bag.jpg'),
        ('Backpack #5', 'backpacks', 'Description', 24.99, '../static/styles/images/backpacks/grayblue_bag.jpg'),
        ('Backpack #6', 'backpacks', 'Description', 24.99, '../static/styles/images/backpacks/green_bag.jpg'),
        ('Backpack #7', 'backpacks', 'Description', 24.99, '../static/styles/images/backpacks/leather_bag.jpg'),
        ('Backpack #8', 'backpacks', 'Description', 24.99, '../static/styles/images/backpacks/redbrown_bag.jpg'),
        ('Backpack #9', 'backpacks', 'Description', 24.99, '../static/styles/images/backpacks/yellow_bag.jpg'),
        ('Tote Bag #1', 'tote bags', 'Description', 19.99, '../static/styles/images/totebags/black_tote.jpg'),
        ('Tote Bag #2', 'tote bags', 'Description', 19.99, '../static/styles/images/totebags/coffee_tote.jpg'),
        ('Tote Bag #3', 'tote bags', 'Description', 19.99, '../static/styles/images/totebags/elevated_tote.jpg'),
        ('Tote Bag #4', 'tote bags', 'Description', 19.99, '../static/styles/images/totebags/green_tote.jpg'),
        ('Tote Bag #5', 'tote bags', 'Description', 19.99, '../static/styles/images/totebags/huevos_tote.jpg'),
        ('Tote Bag #6', 'tote bags', 'Description', 19.99, '../static/styles/images/totebags/icecream_tote.jpg'),
        ('Tote Bag #7', 'tote bags', 'Description', 19.99, '../static/styles/images/totebags/rabbit_tote.jpg'),
        ('Tote Bag #8', 'tote bags', 'Description', 19.99, '../static/styles/images/totebags/rwb_tote.jpg'),
        ('Water Bottle #1', 'water bottles', 'Description', 12.99, '../static/styles/images/bottles/brown_bottle.jpg'),
        ('Water Bottle #2', 'water bottles', 'Description', 12.99, '../static/styles/images/bottles/gray_bottle.jpg'),
        ('Water Bottle #3', 'water bottles', 'Description', 12.99, '../static/styles/images/bottles/green_bottle.jpg'),
        ('Water Bottle #4', 'water bottles', 'Description', 12.99, '../static/styles/images/bottles/pink_bottle.jpg'),
        ('Water Bottle #5', 'water bottles', 'Description', 12.99, '../static/styles/images/bottles/purple_bottle.jpg'),
        ('Water Bottle #6', 'water bottles', 'Description', 12.99, '../static/styles/images/bottles/white_bottle.jpg')
        
    ]
    for product in products_info:
        db.execute(
            'INSERT INTO products (name, category, description, price, image_path) VALUES (?, ?, ?, ?, ?)',
            product
        )
    db.commit()

        
def init_db():
    db = get_db()

    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))

@click.command('init-db')
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    fill_products()
    click.echo('Initialized the database.')
    
def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)