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
    description = '''Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut 
    labore et dolore magna aliqua. Placerat orci nulla pellentesque dignissim enim sit amet. Morbi blandit cursus 
    risus at ultrices mi. Lobortis feugiat vivamus at augue eget arcu dictum.
    '''
    products_info = [
    ('Adventure Blue Backpack', 'backpacks', "Embark on a journey with our Adventure-Ready Blue Backpack. The vibrant blue hue not only adds a pop of color but also complements the sturdy and practical design, making it perfect for those who seek both style and functionality in their daily adventures.", 24.99, '../static/styles/images/backpacks/blue_bag.jpg'),
    ('Sleek Commuter Backpack', 'backpacks', "Elevate your daily commute with our Sleek Dark Gray Commuter Backpack. The deep gray shade exudes sophistication, while the streamlined design and multiple compartments provide a perfect balance of style and organization for your urban lifestyle.", 24.99, '../static/styles/images/backpacks/darkgray_bag.jpg'),
    ('Classic Gray Backpack', 'backpacks', "Meet your everyday companion – the Classic Gray Backpack. This neutral-toned accessory seamlessly fits into any wardrobe, offering timeless style and versatility. Its spacious interior and durable construction make it an essential for your daily routines.", 24.99, '../static/styles/images/backpacks/gray_bag.jpg'),
    ('Explorer Gray Backpack', 'backpacks', "Unleash your urban spirit with our Modern Gray Urban Explorer Backpack. Another shade of gray combines with a contemporary design, ensuring you stay on-trend while comfortably carrying all your essentials for city adventures.", 24.99, '../static/styles/images/backpacks/gray2_bag.jpg'),
    ('Fusion Travel Backpack', 'backpacks', "Plan your next getaway with our Gray-Blue Fusion Travel Backpack. The unique blend of gray and blue not only sets a distinctive tone but also reflects the versatility required for your travel needs. Functional compartments make packing a breeze.", 24.99, '../static/styles/images/backpacks/grayblue_bag.jpg'),
    ('Green Adventure Backpack', 'backpacks', "Connect with nature using our Nature-Inspired Green Backpack. The lively green color mirrors the vibrancy of the outdoors, while the backpack's functionality ensures it's ready to accompany you on hikes, picnics, or any outdoor escapade", 24.99, '../static/styles/images/backpacks/green_bag.jpg'),
    ('City Leather Backpack', 'backpacks', "Make a statement with our City Explorer Leather Backpack. The luxurious leather not only exudes sophistication but also ensures durability. Ideal for both work and leisure, this backpack seamlessly transitions from the office to after-hours engagements.", 24.99, '../static/styles/images/backpacks/leather_bag.jpg'),
    ('Red-Brown Warm Backpack', 'backpacks', "Embrace warmth and functionality with our Commute Companion Red-Brown Backpack. The earthy tones add a cozy touch, making it an ideal accessory for those seeking comfort and style during their daily journeys.", 24.99, '../static/styles/images/backpacks/redbrown_bag.jpg'),
    ('Cheerful Yellow Backpack', 'backpacks', "Inject a dose of cheer into your day with our Contemporary Yellow Backpack. Beyond its bold color, this backpack boasts modern design elements, ensuring you not only stand out but also carry your belongings with ease and flair.", 24.99, '../static/styles/images/backpacks/yellow_bag.jpg'),
    ('Black Everyday Tote', 'tote bags', "Make a bold statement with our versatile black tote bag. Crafted from durable and eco-friendly materials, this bag is not only a practical accessory for your everyday needs but also a sleek and timeless addition to your wardrobe. Embrace the simplicity and sophistication of black – the perfect companion for any occasion.", 19.99, '../static/styles/images/totebags/black_tote.jpg'),
    ("Coffee Lover's Tote", 'tote bags', "Express your love for coffee with our witty tote bag. Featuring a playful coffee-related quote, this bag is a must-have for every caffeine enthusiast. Carry your essentials with a dash of humor and let the world know that you take your coffee as seriously as your style.", 19.99, '../static/styles/images/totebags/coffee_tote.jpg'),
    ('Elevated Tote', 'tote bags', "Elevate your fashion game with our chic and sophisticated tote bag. The carefully curated design and premium materials make this bag a true fashion statement. Whether you're headed to a business meeting or a social event, carry your essentials in style with this elevated tote.", 19.99, '../static/styles/images/totebags/elevated_tote.jpg'),
    ('Refreshing Green Tote', 'tote bags', "Elevate your style with our refreshing green tote bag, a perfect blend of fashion and functionality. The vibrant green hue adds a pop of color to your ensemble, making it an ideal accessory for any season. Crafted with durable materials and featuring a spacious interior, this tote is designed to seamlessly transition from your daily commute to weekend adventures. Embrace the versatility and natural beauty of green with a tote that effortlessly complements your on-the-go lifestyle.", 19.99, '../static/styles/images/totebags/green_tote.jpg'),
    ("'Hasta Los Huevos' Tote", 'tote bags', "Spice up your style with our vibrant 'Hasta Los Huevos tote' bag. The bold colors and playful design make a lively statement, turning a simple accessory into a conversation starter. Embrace the fun and flair of this tote, perfect for adding a touch of personality to your day.", 19.99, '../static/styles/images/totebags/huevos_tote.jpg'),
    ('Ice Cream Tote', 'tote bags', "Indulge your sweet tooth and showcase your love for all things delicious with our ice cream tote bag. The whimsical design celebrates the joy of indulgence, making it a delightful accessory for your everyday adventures. Treat yourself to a tote that's as sweet as you are.", 19.99, '../static/styles/images/totebags/icecream_tote.jpg'),
    ('Rabbit Charm Tote', 'tote bags', "Simplicity meets charm with our Minimalist Black Rabbit Tote Bag. Crafted in sleek black, this tote is a sophisticated canvas for a subtle yet captivating rabbit design. The minimalist approach adds a touch of elegance, making it a versatile accessory for any occasion. The durable material ensures longevity, while the discreet rabbit motif adds just the right amount of character. Carry your essentials in style with this understated and chic black rabbit tote, a perfect blend of simplicity and whimsy.", 19.99, '../static/styles/images/totebags/rabbit_tote.jpg'),
    ('Urban Elegance Tote', 'tote bags', "Introducing our Urban Elegance Tote Bag, a versatile accessory that seamlessly blends style and practicality. The sleek design and neutral color palette make it an ideal companion for any occasion. The simplicity of the tote allows for effortless pairing with a variety of outfits, while the spacious interior ensures you can carry your essentials with ease. Whether you're heading to work, running errands, or enjoying a casual day out, this understated yet chic tote is the perfect addition to your everyday ensemble. Elevate your look with the timeless appeal of our Urban Elegance Tote Bag", 19.99, '../static/styles/images/totebags/rwb_tote.jpg'),
    ('Wood Brown Water Bottle', 'water bottles', 'Introducing our sleek and woody water bottle – the perfect blend of style and functionality. Crafted from durable stainless steel, this bottle keeps your beverages at the ideal temperature while embracing a rich brown hue that complements your outdoor adventures. Stay hydrated in style with this nature-inspired companion.', 12.99, '../static/styles/images/bottles/brown_bottle.jpg'),
    ('Sleek Gray Water Bottle', 'water bottles', "Elevate your hydration game with our sophisticated gray water bottle. Designed for the modern explorer, this stainless steel bottle combines durability with a timeless aesthetic. Whether you're at the gym or on a hike, the neutral gray tone adds a touch of understated elegance to your active lifestyle.", 12.99, '../static/styles/images/bottles/gray_bottle.jpg'),
    ('Eco Green Water Bottle', 'water bottles', "Go green in more ways than one with our vibrant green water bottle. Crafted from eco-friendly stainless steel, this bottle not only helps reduce single-use plastic waste but also adds a burst of freshness to your daily routine. Stay hydrated while making a positive impact on the planet with this stylish and sustainable choice.", 12.99, '../static/styles/images/bottles/green_bottle.jpg'),
    ('Chic Pink Water Bottle', 'water bottles', "Embrace a pop of color with our chic pink water bottle. This stainless steel companion is not just a hydration essential but also a fashion statement. Whether you're hitting the yoga studio or conquering your daily commute, let this bottle be your cheerful sidekick, keeping you refreshed and energized in the most stylish way possible.", 12.99, '../static/styles/images/bottles/pink_bottle.jpg'),
    ('Regal Purple Water Bottle', 'water bottles', "Unleash your adventurous spirit with our regal purple water bottle. Made from high-quality stainless steel, this bottle combines durability with a touch of royalty. The deep purple hue adds a sense of mystery and sophistication to your on-the-go lifestyle, making every sip a statement of elegance.", 12.99, '../static/styles/images/bottles/purple_bottle.jpg'),
    ('Classic White Water Bottle', 'water bottles', "Embody simplicity and purity with our classic white water bottle. Crafted from stainless steel, this bottle is a timeless accessory for any setting – from the office to the great outdoors. The clean and minimalist design ensures that you stay hydrated in style, making it a versatile and essential part of your daily routine.", 12.99, '../static/styles/images/bottles/white_bottle.jpg')
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