from flask_sqlalchemy import SQLAlchemy
from flask import Flask, redirect, render_template, request, url_for
from flask_migrate import Migrate
from sqlalchemy_utils import database_exists, create_database

app = Flask(__name__)

username = "postgres"
password = "postgres"
host = "localhost"
port = "5432"
db_name = "se3355mt_db"
app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{username}:{password}@{host}:{port}/{db_name}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)

class Campaign(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False, unique=True)
    description = db.Column(db.String(255), nullable=False)
    image_url = db.Column(db.String(255), nullable=False)

    def __repr__(self):
        return f'<Campaign {self.title}>'


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    colors = db.relationship('ProductColor', backref='product')
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))


class ProductColor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    color = db.Column(db.Text, nullable=False)
    price = db.Column(db.Numeric(10, 2), nullable=False)
    image_url = db.Column(db.Text, nullable=False)


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    category_name = db.Column(db.String(50), nullable=False)


def setup_db():
    with app.app_context():
        db.drop_all()
        if not database_exists(db.engine.url):
            create_database(db.engine.url)
        db.create_all()

        db.session.query(Campaign).delete()
        db.session.query(Product).delete()
        db.session.query(ProductColor).delete()
        db.session.query(Category).delete()
        db.session.commit()

        if Campaign.query.count() == 0:
            campaigns = [
                Campaign(title='Summer Sale', description='Up to 50% off on summer items!', image_url='static/c1.png'),
                Campaign(title='Winter Wonders', description='Explore cozy winter gear!', image_url='static/c2.png'),
                Campaign(title='Spring Collection', description='Fresh looks for spring!', image_url='static/c3.png'),
                Campaign(title='Autumn Arrivals', description='Get ready for the cool autumn breeze.', image_url='static/c4.png'),
                Campaign(title='Back to School', description='Everything you need for school.', image_url='static/c5.png')
            ]
            db.session.add_all(campaigns)
            db.session.commit()
        if Category.query.count() == 0:
            categories = [
                Category(category_name='Laptops'),
                Category(category_name='Desktops'),
                Category(category_name='Monitors'),
                Category(category_name='Keyboards'),
                Category(category_name='Mouses'),
                Category(category_name='CPUs'),
                Category(category_name='GPUs'),
                Category(category_name='RAM Modules')
            ]
            db.session.add_all(categories)
            db.session.commit()


@app.route("/")
def home():
    campaigns = Campaign.query.all()
    categories = Category.query.all()
    return render_template("index.html", campaigns=campaigns, categories=categories)


@app.route('/category/<int:category_id>')
def show_category(category_id):
    category = Category.query.get_or_404(category_id)
    products = Product.query.filter_by(category_id=category_id).all()
    categories = Category.query.all()
    return render_template('category.html', category=category, products=products, categories=categories)


if __name__ == "__main__":
    setup_db()
    app.run(debug=True)
