from flask import Blueprint, jsonify, request
from flask_cors import cross_origin
from flask_jwt_extended import jwt_required, get_jwt_identity
import uuid
from datetime import datetime

checkout_bp = Blueprint('checkout', __name__)

# Mock orders and carts database
orders_db = {}
carts_db = {}

@checkout_bp.route('/checkout', methods=['POST'])
@cross_origin()
@jwt_required()
def create_order():
    try:
        current_user_email = get_jwt_identity()
        data = request.get_json()
        
        if not data:
            return jsonify({"success": False, "error": "Checkout data required"}), 400
        
        # Get cart items from request or from user's cart
        items = data.get('items', [])
        if not items and current_user_email in carts_db:
            items = carts_db[current_user_email]
        
        if not items:
            return jsonify({"success": False, "error": "No items to checkout"}), 400
        
        # Calculate total
        total = sum(item.get('price', 0) * item.get('quantity', 1) for item in items)
        
        # Create order
        order_id = f"ORD-{str(uuid.uuid4())[:8].upper()}"
        order = {
            'id': order_id,
            'userId': current_user_email,
            'items': items,
            'total': total,
            'status': 'processing',
            'shippingAddress': data.get('shippingAddress', ''),
            'paymentMethod': data.get('paymentMethod', 'credit_card'),
            'createdAt': datetime.now().isoformat()
        }
        
        # Store order
        if current_user_email not in orders_db:
            orders_db[current_user_email] = []
        orders_db[current_user_email].append(order)
        
        # Clear user's cart
        if current_user_email in carts_db:
            carts_db[current_user_email] = []
        
        return jsonify({
            "success": True,
            "data": order,
            "message": "Order created successfully"
        }), 201
        
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@checkout_bp.route('/orders', methods=['GET'])
@cross_origin()
@jwt_required()
def get_orders():
    try:
        current_user_email = get_jwt_identity()
        
        if current_user_email not in orders_db:
            orders_db[current_user_email] = []
        
        return jsonify({
            "success": True,
            "data": orders_db[current_user_email],
            "count": len(orders_db[current_user_email])
        })
        
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@checkout_bp.route('/orders/<order_id>', methods=['GET'])
@cross_origin()
@jwt_required()
def get_order(order_id):
    try:
        current_user_email = get_jwt_identity()
        
        if current_user_email not in orders_db:
            return jsonify({"success": False, "error": "No orders found"}), 404
        
        for order in orders_db[current_user_email]:
            if order['id'] == order_id:
                return jsonify({
                    "success": True,
                    "data": order
                })
        
        return jsonify({"success": False, "error": "Order not found"}), 404
        
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500
