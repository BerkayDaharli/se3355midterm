from flask import Flask, render_template, request, session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import or_
from sqlalchemy_utils import database_exists, create_database
import mockdata
app = Flask(__name__)
app.secret_key = '12345'

username = "postgres"
password = "postgres"
host = "localhost"
port = "5432"
db_name = "se3355mt_db"
app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{username}:{password}@{host}:{port}/{db_name}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class Campaign(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False, unique=True)
    description = db.Column(db.String(255), nullable=False)
    image_file_name = db.Column(db.String(255), nullable=False)
    button_name = db.Column(db.String(50), nullable=False)
    campaign_link = db.Column(db.String(255), nullable=False)


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    colors = db.relationship('ProductColor', backref='product')
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    shipped_from_id = db.Column(db.Integer, db.ForeignKey('city.id'))
    shipped_from = db.relationship('City', backref=db.backref('products', lazy=True))


class ProductColor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    color = db.Column(db.Text, nullable=False)
    price = db.Column(db.Numeric(10, 2), nullable=False)
    images = db.relationship('Image', backref='product_color')


class Image(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    image_file_name = db.Column(db.Text, nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=True)
    product_color_id = db.Column(db.Integer, db.ForeignKey('product_color.id'), nullable=True)


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    category_name = db.Column(db.String(50), nullable=False)


class City(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)


def search_products(query):
    query_obj = Product.query \
        .join(Product.colors) \
        .join(Product.shipped_from) \
        .filter(or_(
        Product.product_title.ilike(f"%{query}%"),
        Product.description.ilike(f"%{query}%"),
        ProductColor.color.ilike(f"%{query}%"),
        City.name.ilike(f"%{query}%")
    )).distinct()
    results = query_obj.all()
    return results


def setup_db():
    with app.app_context():
        db.drop_all()
        if not database_exists(db.engine.url):
            create_database(db.engine.url)
        db.create_all()

        add_cities()
        add_campaigns()
        add_categories()
        add_products_with_images()


def add_cities():
    with app.app_context():
        if City.query.count() != 81:
            initial_city = City(
                name="All Cities",
                id=0
            )
            db.session.add(initial_city)
            db.session.flush()
            db.session.commit()
            cities = mockdata.cities
            for city in cities:
                add_city = City(
                    name=city['city_name']
                )
                db.session.add(add_city)
                db.session.flush()
            db.session.commit()


def add_campaigns():
    if Campaign.query.count() == 0:
        campaigns = [
            Campaign(title='Insane discounts', description='for the most beloved electronics',
                     image_file_name='c1.png', button_name="Buy now!",
                     campaign_link='category/1'),
            Campaign(title='Amazing fashion products', description='with unbelievable prices',
                     image_file_name='c2.png', button_name="Shop now!",
                     campaign_link='category/2'),
            Campaign(title='Decorate your house', description='with these new home products',
                     image_file_name='c3.png', button_name="Purchase now",
                     campaign_link='category/3'),
            Campaign(title='Spice up your garden', description='New seeds have arrived on our shop!',
                     image_file_name='c4.png', button_name="Take a look",
                     campaign_link='category/4'),
            Campaign(title='New toys', description='Toys for kids',
                     image_file_name='c5.png', button_name="Take a look",
                     campaign_link='category/5')
        ]
        db.session.bulk_save_objects(campaigns)
        db.session.commit()


def add_categories():
    if Category.query.count() == 0:
        categories = [
            Category(category_name='Electronics'),
            Category(category_name='Fashion'),
            Category(category_name='Home'),
            Category(category_name='Gardening'),
            Category(category_name='Toys'),
        ]
        db.session.bulk_save_objects(categories)
        db.session.commit()


def add_products_with_images():
    if Product.query.count() == 0:
        product_details = mockdata.product_details
        for mock_product in product_details:
            product = Product(
                product_title=mock_product['title'],
                description=mock_product['description'],
                category_id=mock_product['category_id'],
                shipped_from_id=mock_product['shipped_from_id']
            )
            db.session.add(product)
            db.session.flush()

            for color_info in mock_product['colors']:
                product_color = ProductColor(
                    product_id=product.id,
                    color=color_info['color'],
                    price=color_info['price']
                )
                db.session.add(product_color)
                db.session.flush()

                for image_file_name in color_info['images']:
                    image = Image(
                        image_file_name=image_file_name,
                        product_color_id=product_color.id
                    )
                    db.session.add(image)

        db.session.commit()


@app.route("/")
def home():
    campaigns = Campaign.query.all()
    categories = Category.query.all()
    return render_template("index.html", campaigns=campaigns, categories=categories)


@app.route('/category/<int:category_id>', methods=['GET'])
def show_category(category_id):
    cities = City.query.all()
    category = Category.query.get_or_404(category_id)

    selected_city_id = request.args.get('city_id', default=session.get('selected_city_id', None))
    session['selected_city_id'] = selected_city_id

    doorstep_tomorrow = request.args.get('doorstep_tomorrow', 'false') == 'true'
    categories = Category.query.all()

    products = Product.query.filter_by(category_id=category_id).all()
    if selected_city_id:
        products.sort(key=lambda x: x.shipped_from_id != int(selected_city_id))
    if selected_city_id is None:
        selected_city_id = "0"
    return render_template('category.html', category=category, products=products,
                           cities=cities, selected_city_id=int(selected_city_id),
                           categories=categories, doorstep_tomorrow=doorstep_tomorrow)


@app.route('/search', methods=['GET'])
def search():
    cities = City.query.all()
    query = request.args.get('search')
    categories = Category.query.all()

    selected_city_id = request.args.get('city_id', default=session.get('selected_city_id', None))
    session['selected_city_id'] = selected_city_id  # Update session

    doorstep_tomorrow = request.args.get('doorstep_tomorrow', 'false') == 'true'
    if selected_city_id is None:
        selected_city_id = "0"
    if query:
        products = search_products(query)
        #Sort by whether the product is shipped from the same city as selected city.
        #Useful for "Yarin kapinda (by your doorstep tomorrow)" feature
        products.sort(key=lambda x: x.shipped_from_id != int(selected_city_id))
        return render_template('searchresult.html', categories=categories,
                               products=products, query=query, cities=cities,
                               selected_city_id=int(selected_city_id), doorstep_tomorrow=doorstep_tomorrow)
    else:
        return render_template('searchresult.html', categories=categories,
                               products=[], query=query, cities=cities, selected_city_id=int(selected_city_id),
                               doorstep_tomorrow=doorstep_tomorrow)


@app.route('/product/<int:product_id>')
def product_page(product_id):
    product = Product.query.get(product_id)
    colors = ProductColor.query.filter_by(product_id=product_id).all()
    categories = Category.query.all()
    if product:
        return render_template('productpage.html', product=product, colors=colors, categories=categories)
    else:
        return render_template('404productNotFound.html', categories=categories)


if __name__ == "__main__":
    setup_db()
    app.run('0.0.0.0', debug=True, port=8100, ssl_context='adhoc')
