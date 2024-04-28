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
                     campaign_link='category/4')
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
        product_details = [
            {
                'title': 'Razer Blade 14',
                'description': """
AMD Ryzen™ 9 8945HS
Windows 11 Home
14" 240Hz QHD+
GeForce RTX 4060
16GB 5600MHz RAM, 1TB SSD""",
                'category_id': 1,
                'shipped_from_id': 34,
                'images': ['product_overview.jpg'],  # General images for the product
                'colors': [
                    {
                        'color': 'Black',
                        'price': 75864.00,
                        'images': ['razer_black_1.png', 'razer_black_2.png',
                                   'razer_black_3.png', 'razer_black_4.png',
                                   'razer_black_5.png']
                    },
                    {
                        'color': 'Mercury',
                        'price': 77000.00,
                        'images': ['razer_mercury_1.png', 'razer_mercury_2.png',
                                   'razer_mercury_3.png', 'razer_mercury_4.png',
                                   'razer_mercury_5.png']
                    }
                ]
            },
            {
                'title': 'Samsung Galaxy S24 Ultra',
                'description': """
Samsung Galaxy S24 Ultra 512 GB 12 GB Ram (Samsung Türkiye Guarantee)
""",
                'category_id': 1,
                'shipped_from_id': 75,
                'images': ['product_overview.jpg'],  # General images for the product
                'colors': [
                    {
                        'color': 'Black',
                        'price': 69999.00,
                        'images': ['samsung_s24_black_1.png', 'samsung_s24_black_2.png',
                                   'samsung_s24_black_3.png', 'samsung_s24_black_4.png',
                                   'samsung_s24_black_5.png']
                    },
                    {
                        'color': 'Blue',
                        'price': 73999.00,
                        'images': ['samsung_s24_blue_1.png', 'samsung_s24_blue_2.png',
                                   'samsung_s24_blue_3.png', 'samsung_s24_blue_4.png',
                                   'samsung_s24_blue_5.png']
                    },
                    {
                        'color': 'Gray',
                        'price': 69949.00,
                        'images': ['samsung_s24_gray_1.png', 'samsung_s24_gray_2.png',
                                   'samsung_s24_gray_3.png', 'samsung_s24_gray_4.png',
                                   'samsung_s24_gray_5.png']
                    },
                    {
                        'color': 'Green',
                        'price': 71999.00,
                        'images': ['samsung_s24_green_1.png', 'samsung_s24_green_2.png']
                    },
                    {
                        'color': 'Orange',
                        'price': 71999.00,
                        'images': ['samsung_s24_orange_1.png', 'samsung_s24_orange_2.png']
                    },
                    {
                        'color': 'Purple',
                        'price': 69999.00,
                        'images': ['samsung_s24_purple_1.png', 'samsung_s24_purple_2.png',
                                   'samsung_s24_purple_3.png', 'samsung_s24_purple_4.png',
                                   'samsung_s24_purple_5.png', ]
                    },
                    {
                        'color': 'Yellow',
                        'price': 67199.00,
                        'images': ['samsung_s24_yellow_1.png', 'samsung_s24_yellow_2.png',
                                   'samsung_s24_yellow_3.png', 'samsung_s24_yellow_4.png',
                                   'samsung_s24_yellow_5.png', ]
                    },
                ]
            },
            {
                'title': 'T-Shirt',
                'description': """
        Avva Erkek Yeşil %100 Pamuk Serin Tutan Regular Fit Polo
        """,
                'category_id': 2,
                'shipped_from_id': 14,
                'images': ['product_overview.jpg'],  # General images for the product
                'colors': [
                    {
                        'color': 'Black',
                        'price': 504.99,
                        'images': ['tshirt_black_1.png', 'tshirt_black_2.png',
                                   'tshirt_black_3.png']
                    },
                    {
                        'color': 'Red',
                        'price': 504.99,
                        'images': ['tshirt_burgundy_1.png', 'tshirt_burgundy_2.png',
                                   'tshirt_burgundy_3.png', 'tshirt_burgundy_4.png']
                    },
                    {
                        'color': 'Gray',
                        'price': 504.99,
                        'images': ['tshirt_gray_1.png', 'tshirt_gray_2.png',
                                   'tshirt_gray_3.png']
                    },
                    {
                        'color': 'Green',
                        'price': 504.99,
                        'images': ['tshirt_green_1.png', 'tshirt_green_2.png',
                                   'tshirt_green_3.png']
                    },
                    {
                        'color': 'White',
                        'price': 504.99,
                        'images': ['tshirt_white_1.png', 'tshirt_white_2.png',
                                   'tshirt_white_3.png']
                    },
                ]
            },
            {
                'title': 'Jeans',
                'description': """
Colins 760 DIANA Yüksek Bel Dar Paça Super Slim Fit Siyah Kadın Jean Pantolon
        """,
                'category_id': 2,
                'shipped_from_id': 35,
                'images': ['product_overview.jpg'],  # General images for the product
                'colors': [
                    {
                        'color': 'Black',
                        'price': 349.99,
                        'images': ['jean_black_1.png', 'jean_black_2.png',
                                   'jean_black_3.png', 'jean_black_4.png',
                                   'jean_black_5.png']
                    },
                ]
            },
            {
                'title': 'Sofa',
                'description': """
        Ipek Mobilya Doremi 2 Li Koltuk ( Gri )
                """,
                'category_id': 3,
                'shipped_from_id': 56,
                'images': ['product_overview.jpg'],  # General images for the product
                'colors': [
                    {
                        'color': 'Gray',
                        'price': 9850.99,
                        'images': ['sofa_gray_1.png', 'sofa_gray_2.png',
                                   'sofa_gray_3.png', 'sofa_gray_4.png']
                    },
                ]
            },
            {
                'title': 'Curtain',
                'description': """
Vagonik 150x230 cm Blackout Fon Perde Korniş tokaları 
pliseli kullanıma uygun olacak şekilde her 9 cm de bir hazır 
dikilidir. Tak & kullan kullanımınıza uygundur. Yıkanabilir, 
güneşte solmaz, leke barındırmaz, ithal Pietra kumaştan üretilmiştir. 
Paket İçeriği: 1 adet Tek Kanat 150x230 cm Fon Perde
                """,
                'category_id': 3,
                'shipped_from_id': 45,
                'images': ['product_overview.jpg'],  # General images for the product
                'colors': [
                    {
                        'color': 'Blue',
                        'price': 349.00,
                        'images': ['curtain_blue_1.png']
                    },
                    {
                        'color': 'Red',
                        'price': 349.00,
                        'images': ['curtain_red_1.png']
                    },
                    {
                        'color': 'White',
                        'price': 349.00,
                        'images': ['curtain_white_1.png']
                    },
                ]
            },
            {
                'title': 'Cucumber Seed',
                'description': """

Ata Tohumculuk 25 Adet Tohum Badem Salatalık Köy Salatalığı Tohumu Yerli Tohum Bol Verimli
25 ADET TOHUM ORJİNAL TOHUM YERLİ BADEM SALATALIK KÖY SALATALIĞI TOHUMU 
                """,
                'category_id': 4,
                'shipped_from_id': 80,
                'images': ['product_overview.jpg'],  # General images for the product
                'colors': [
                    {
                        'color': 'Default',
                        'price': 16.99,
                        'images': ['cucumber_seed_1.png', 'cucumber_seed_2.png',
                                   'cucumber_seed_3.png']
                    },
                ]
            },
            {
                'title': 'Chainsaw',
                'description': """
Teknik Özellikler
Diş22
Ağırlık3,2 kg
Güç1,2 hp - 0,9 kW
                        """,
                'category_id': 4,
                'shipped_from_id': 4,
                'images': ['product_overview.jpg'],  # General images for the product
                'colors': [
                    {
                        'color': 'Red',
                        'price': 3035.12,
                        'images': ['chainsaw_1.png']
                    },
                ]
            },
            {
                'title': 'Scooter',
                'description': """

Direksiyon Kullanım Esnasında Çocuğun Verdiği Ağırlık Yönüne Göre Sağa Ve Sola Yatmaktadır.
* Kademeli Yükseklik Ayarı Yapılabilir.
* Yumuşak Silikon Işıklı Tekerlerlidir.
* Kolay Montajlıdır.
* Kolay Çıkartılıp Takılabilir Direksiyona Sahiptir.
* Gelişmiş Fren Performansına Sahiptir.
* Yüksek Manevra Kabiliyetine Sahiptir.
* Türkiye'de Üretilmiştir.
                                """,
                'category_id': 5,
                'shipped_from_id': 24,
                'images': ['product_overview.jpg'],  # General images for the product
                'colors': [
                    {
                        'color': 'Blue',
                        'price': 749.90,
                        'images': ['scooter_blue_1.png', 'scooter_blue_2.png']
                    },
                    {
                        'color': 'Pink',
                        'price': 730.00,
                        'images': ['scooter_pink_1.png', 'scooter_pink_2.png']
                    },
                    {
                        'color': 'Yellow',
                        'price': 749.90,
                        'images': ['scooter_yellow_1.png', 'scooter_yellow_2.png']
                    },
                    {
                        'color': 'Orange',
                        'price': 730.00,
                        'images': ['scooter_orange_1.png', 'scooter_orange_2.png']
                    },
                ]
            },
            {
                'title': 'Bathroom Crab Toy',
                'description': """

        Direksiyon Kullanım Esnasında Çocuğun Verdiği Ağırlık Yönüne Göre Sağa Ve Sola Yatmaktadır.
        * Kademeli Yükseklik Ayarı Yapılabilir.
        * Yumuşak Silikon Işıklı Tekerlerlidir.
        * Kolay Montajlıdır.
        * Kolay Çıkartılıp Takılabilir Direksiyona Sahiptir.
        * Gelişmiş Fren Performansına Sahiptir.
        * Yüksek Manevra Kabiliyetine Sahiptir.
        * Türkiye'de Üretilmiştir.
                                        """,
                'category_id': 5,
                'shipped_from_id': 34,
                'images': ['product_overview.jpg'],  # General images for the product
                'colors': [
                    {
                        'color': 'Default',
                        'price': 257.00,
                        'images': ['bathroom_crab_toy_1.png']
                    },
                ]
            },

        ]

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
                color_info = dict(color_info)
                print(color_info)
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
