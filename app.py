from flask import Flask, render_template, request, session
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import or_
from sqlalchemy_utils import database_exists, create_database

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
migrate = Migrate(app, db)


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
    images = db.relationship('Image', backref='product')  # One-to-many relationship for images


class ProductColor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    color = db.Column(db.Text, nullable=False)
    price = db.Column(db.Numeric(10, 2), nullable=False)
    images = db.relationship('Image', backref='product_color')  # One-to-many relationship for images


class Image(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    image_file_name = db.Column(db.Text, nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=True)
    product_color_id = db.Column(db.Integer, db.ForeignKey('product_color.id'), nullable=True)
    # You can also add more fields if needed, such as image_type or upload_date


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

    # Print the actual SQL query
    print(
        query_obj)  # Or use print(str(query_obj.statement.compile(compile_kwargs={"literal_binds": True}))) for the full query
    results = query_obj.all()
    print(results)
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
            cities = [
                {'city_name': 'Adana'},
                {'city_name': 'Adıyaman'},
                {'city_name': 'Afyon'},
                {'city_name': 'Ağrı'},
                {'city_name': 'Aksaray'},
                {'city_name': 'Amasya'},
                {'city_name': 'Ankara'},
                {'city_name': 'Antalya'},
                {'city_name': 'Ardahan'},
                {'city_name': 'Artvin'},
                {'city_name': 'Aydın'},
                {'city_name': 'Balıkesir'},
                {'city_name': 'Bartın'},
                {'city_name': 'Batman'},
                {'city_name': 'Bayburt'},
                {'city_name': 'Bilecik'},
                {'city_name': 'Bingöl'},
                {'city_name': 'Bitlis'},
                {'city_name': 'Bolu'},
                {'city_name': 'Burdur'},
                {'city_name': 'Bursa'},
                {'city_name': 'Çanakkale'},
                {'city_name': 'Çankırı'},
                {'city_name': 'Çorum'},
                {'city_name': 'Denizli'},
                {'city_name': 'Diyarbakır'},
                {'city_name': 'Düzce'},
                {'city_name': 'Edirne'},
                {'city_name': 'Elazığ'},
                {'city_name': 'Erzincan'},
                {'city_name': 'Erzurum'},
                {'city_name': 'Eskişehir'},
                {'city_name': 'Gaziantep'},
                {'city_name': 'Giresun'},
                {'city_name': 'Gümüşhane'},
                {'city_name': 'Hakkari'},
                {'city_name': 'Hatay'},
                {'city_name': 'Iğdır'},
                {'city_name': 'Isparta'},
                {'city_name': 'İstanbul'},
                {'city_name': 'İzmir'},
                {'city_name': 'Kahramanmaraş'},
                {'city_name': 'Karabük'},
                {'city_name': 'Karaman'},
                {'city_name': 'Kars'},
                {'city_name': 'Kastamonu'},
                {'city_name': 'Kayseri'},
                {'city_name': 'Kilis'},
                {'city_name': 'Kırıkkale'},
                {'city_name': 'Kırklareli'},
                {'city_name': 'Kırşehir'},
                {'city_name': 'Kocaeli'},
                {'city_name': 'Konya'},
                {'city_name': 'Kütahya'},
                {'city_name': 'Malatya'},
                {'city_name': 'Manisa'},
                {'city_name': 'Mardin'},
                {'city_name': 'Mersin'},
                {'city_name': 'Muğla'},
                {'city_name': 'Muş'},
                {'city_name': 'Nevşehir'},
                {'city_name': 'Niğde'},
                {'city_name': 'Ordu'},
                {'city_name': 'Osmaniye'},
                {'city_name': 'Rize'},
                {'city_name': 'Sakarya'},
                {'city_name': 'Samsun'},
                {'city_name': 'Şanlıurfa'},
                {'city_name': 'Siirt'},
                {'city_name': 'Sinop'},
                {'city_name': 'Şırnak'},
                {'city_name': 'Sivas'},
                {'city_name': 'Tekirdağ'},
                {'city_name': 'Tokat'},
                {'city_name': 'Trabzon'},
                {'city_name': 'Tunceli'},
                {'city_name': 'Uşak'},
                {'city_name': 'Van'},
                {'city_name': 'Yalova'},
                {'city_name': 'Yozgat'},
                {'city_name': 'Zonguldak'}
            ]
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
            Campaign(title='Sevilen elektronik ürünlerde', description='kaçırılmayacak fırsatlar',
                     image_file_name='c1.png', button_name="Hemen al!",
                     campaign_link='category/1'),
            Campaign(title='İstediğin yemek için', description='indirimli malzemeler',
                     image_file_name='c2.png', button_name="Bu fırsatı kaçırma!",
                     campaign_link='#'),
            Campaign(title='Spring Collection', description='Fresh looks for spring!',
                     image_file_name='c3.png', button_name="Alışverişe başla",
                     campaign_link='#'),
            Campaign(title='Autumn Arrivals', description='Get ready for the cool autumn breeze.',
                     image_file_name='c4.png', button_name="Acele et kaçırma",
                     campaign_link='#'),
            Campaign(title='Back to School', description='Everything you need for school.',
                     image_file_name='c5.png', button_name="Acele et kaçırma",
                     campaign_link='#')
        ]
        db.session.bulk_save_objects(campaigns)
        db.session.commit()


def add_categories():
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
        db.session.bulk_save_objects(categories)
        db.session.commit()


def add_products_with_images():
    if Product.query.count() == 0:
        product_details = [{
            'title': 'Smartphone',
            'description': 'High-performance smartphone with advanced camera features.',
            'category_id': 1,
            'shipped_from_id': 1,
            'images': ['product_overview.jpg'],  # General images for the product
            'colors': [
                {
                    'color': 'Black',
                    'price': 999.99,
                    'images': ['c3.png', 'c4.png']
                },
                {
                    'color': 'White',
                    'price': 1000.99,
                    'images': ['c1.png', 'c2.png']
                }
            ]
        }]

        # Create and add products, their colors, and images to the database
        for mock_product in product_details:
            product = Product(
                product_title=mock_product['title'],
                description=mock_product['description'],
                category_id=mock_product['category_id'],
                shipped_from_id=mock_product['shipped_from_id']
            )
            db.session.add(product)
            db.session.flush()

            # Add general product images
            for image_file_name in mock_product['images']:
                image = Image(
                    image_file_name=image_file_name,
                    product_id=product.id  # Linking the image directly to the product
                )
                db.session.add(image)

            # Add product colors and their specific images
            for color_info in mock_product['colors']:
                product_color = ProductColor(
                    product_id=product.id,
                    color=color_info['color'],
                    price=color_info['price']
                )
                db.session.add(product_color)
                db.session.flush()

                # Add images specific to this color variant
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

    # Retrieve city_id from request or session
    selected_city_id = request.args.get('city_id', default=session.get('selected_city_id', None))
    session['selected_city_id'] = selected_city_id  # Update session

    doorstep_tomorrow = request.args.get('doorstep_tomorrow', 'false') == 'true'
    categories = Category.query.all()

    # Fetch all products but sort them based on the shipping city
    products = Product.query.filter_by(category_id=category_id).all()
    if selected_city_id:
        products.sort(key=lambda x: x.shipped_from_id != int(selected_city_id))

    return render_template('category.html', category=category, products=products,
                           cities=cities, selected_city_id=int(selected_city_id),
                           categories=categories, doorstep_tomorrow=doorstep_tomorrow)


@app.route('/search', methods=['GET'])
def search():
    cities = City.query.all()
    query = request.args.get('search')
    categories = Category.query.all()

    # Retrieve city_id from request or session
    selected_city_id = request.args.get('city_id', default=session.get('selected_city_id', None))
    session['selected_city_id'] = selected_city_id  # Update session

    doorstep_tomorrow = request.args.get('doorstep_tomorrow', 'false') == 'true'

    if query:
        products = search_products(query)
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
    # Fetch product details from database based on product_id
    product = Product.query.get(product_id)
    colors = ProductColor.query.filter_by(product_id=product_id).all()
    categories = Category.query.all()
    # Assume each color has an 'images' attribute that is a list of Image instances

    # You can adjust the query based on your actual database structure
    if product:
        return render_template('productpage.html', product=product, colors=colors, categories=categories)
    else:
        return render_template('404productNotFound.html', categories=categories)

if __name__ == "__main__":
    setup_db()
    app.run(debug=True)
