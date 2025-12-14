from flask_sqlalchemy import SQLAlchemy
import json

db = SQLAlchemy()

class Order(db.Model):
    __tablename__ = 'orders'
    
    id = db.Column(db.String(50), primary_key=True)
    user_id = db.Column(db.String(50), db.ForeignKey('users.id'), nullable=False)
    items = db.Column(db.Text)  # JSON string of cart items
    total = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(20), default='processing')  # processing, shipped, delivered, cancelled
    shipping_address = db.Column(db.Text)
    payment_method = db.Column(db.String(50))
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    
    def to_dict(self):
        return {
            'id': self.id,
            'userId': self.user_id,
            'items': json.loads(self.items) if self.items else [],
            'total': self.total,
            'status': self.status,
            'shippingAddress': self.shipping_address,
            'paymentMethod': self.payment_method,
            'createdAt': self.created_at.isoformat() if self.created_at else None
        }
