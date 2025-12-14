from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from config import Config

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    CORS(app, resources={r"/api/*": {"origins": "*"}})
    
    # Initialize JWT
    jwt = JWTManager(app)
    
    # Register blueprints
    from app.routes.products import products_bp
    from app.routes.auth import auth_bp
    from app.routes.cart import cart_bp
    from app.routes.checkout import checkout_bp
    from app.routes.orders import orders_bp
    
    app.register_blueprint(products_bp, url_prefix='/api')
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(cart_bp, url_prefix='/api')
    app.register_blueprint(checkout_bp, url_prefix='/api')
    app.register_blueprint(orders_bp, url_prefix='/api')
    
    return app
