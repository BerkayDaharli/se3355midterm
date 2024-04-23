from flask_sqlalchemy import SQLAlchemy
from flask import Flask, redirect, render_template, request, url_for
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
    category = db.Column(db.Text, nullable=False)
    colors = db.relationship('ProductColor', backref='product')


class ProductColor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    color = db.Column(db.Text, nullable=False)
    price = db.Column(db.Numeric(10, 2), nullable=False)
    image_url = db.Column(db.Text, nullable=False)


def setup_db():
    with app.app_context():
        if not database_exists(db.engine.url):
            create_database(db.engine.url)
        db.create_all()

        if Campaign.query.count() == 0:
            campaigns = [
                Campaign(title='Summer Sale', description='Up to 50% off on summer items!', image_url=''),
                Campaign(title='Winter Wonders', description='Explore cozy winter gear!', image_url=''),
                Campaign(title='Spring Collection', description='Fresh looks for spring!', image_url=''),
                Campaign(title='Autumn Arrivals', description='Get ready for the cool autumn breeze.', image_url=''),
                Campaign(title='Back to School', description='Everything you need for school.', image_url='')
            ]
            db.session.add_all(campaigns)
            db.session.commit()


@app.route("/")
def home():
    return render_template("index.html")


if __name__ == "__main__":
    setup_db()
    app.run(debug=True)
