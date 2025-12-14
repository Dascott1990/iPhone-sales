from flask_sqlalchemy import SQLAlchemy
import json

db = SQLAlchemy()

class Product(db.Model):
    __tablename__ = 'products'
    
    id = db.Column(db.String(50), primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    model = db.Column(db.String(50), nullable=False)
    price = db.Column(db.Float, nullable=False)
    description = db.Column(db.Text)
    colors = db.Column(db.JSON)
    storage_options = db.Column(db.JSON)
    image_url = db.Column(db.String(500))
    in_stock = db.Column(db.Boolean, default=True)
    stock_quantity = db.Column(db.Integer, default=100)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'model': self.model,
            'price': self.price,
            'description': self.description,
            'colors': self.colors if self.colors else [],
            'storage': self.storage_options if self.storage_options else [],
            'imageUrl': self.image_url,
            'inStock': self.in_stock,
            'stockQuantity': self.stock_quantity
        }
