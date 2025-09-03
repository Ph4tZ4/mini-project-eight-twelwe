from flask import Flask
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from mongoengine import connect
from config import Config

from routes.auth import auth
from routes.products import products
from routes.contact import contact
from routes.categories import categories
from routes.home import home
from routes.about import about
from routes.cart import cart
from routes.orders import orders
from routes.shipping import shipping
from routes.admin import admin

app = Flask(__name__)
app.config.from_object(Config)

# Debug CORS origins
print("CORS Origins:", app.config['CORS_ORIGINS'])

# CORS Configuration
CORS(app,
     resources={r"/api/*": {"origins": [
         "https://eight-twelwe.loeitech.org",
         "https://api-eight-twelwe.loeitech.org",
         "http://192.168.10.118:9040"
     ]}},
     supports_credentials=True,
     allow_headers=["Content-Type", "Authorization"],
     methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"])

# JWT Configuration
jwt = JWTManager(app)

# เชื่อมต่อ MongoDB ด้วย mongoengine โดยตรง
connect(
    db=app.config["MONGODB_SETTINGS"]["db"],
    host=app.config["MONGODB_SETTINGS"]["host"],
    port=app.config["MONGODB_SETTINGS"]["port"]
)

# Register Blueprints
app.register_blueprint(auth, url_prefix="/api")
app.register_blueprint(products, url_prefix="/api")
app.register_blueprint(contact, url_prefix="/api")
app.register_blueprint(categories, url_prefix="/api")
app.register_blueprint(home, url_prefix="/api")
app.register_blueprint(about, url_prefix="/api")
app.register_blueprint(cart, url_prefix="/api")
app.register_blueprint(orders, url_prefix="/api")
app.register_blueprint(shipping, url_prefix="/api")
app.register_blueprint(admin, url_prefix="/api/admin")

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5550)