from flask import Blueprint, jsonify, request
from flask_cors import cross_origin
from flask_jwt_extended import jwt_required, get_jwt_identity
import uuid

cart_bp = Blueprint('cart', __name__)

# In-memory cart storage (in production, use database or Redis)
carts_db = {}

@cart_bp.route('/cart', methods=['GET'])
@cross_origin()
@jwt_required()
def get_cart():
    try:
        current_user_email = get_jwt_identity()
        
        if current_user_email not in carts_db:
            carts_db[current_user_email] = []
        
        return jsonify({
            "success": True,
            "data": carts_db[current_user_email],
            "count": len(carts_db[current_user_email])
        })
        
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@cart_bp.route('/cart', methods=['POST'])
@cross_origin()
@jwt_required()
def add_to_cart():
    try:
        current_user_email = get_jwt_identity()
        data = request.get_json()
        
        if not data or not data.get('product'):
            return jsonify({"success": False, "error": "Product data required"}), 400
        
        if current_user_email not in carts_db:
            carts_db[current_user_email] = []
        
        cart_item = {
            'id': str(uuid.uuid4()),
            'product': data['product'],
            'color': data.get('color', ''),
            'storage': data.get('storage', 0),
            'quantity': data.get('quantity', 1),
            'price': data['product']['price']
        }
        
        carts_db[current_user_email].append(cart_item)
        
        return jsonify({
            "success": True,
            "data": cart_item,
            "message": "Item added to cart"
        }), 201
        
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@cart_bp.route('/cart/<item_id>', methods=['PUT'])
@cross_origin()
@jwt_required()
def update_cart_item(item_id):
    try:
        current_user_email = get_jwt_identity()
        data = request.get_json()
        
        if current_user_email not in carts_db:
            return jsonify({"success": False, "error": "Cart not found"}), 404
        
        for item in carts_db[current_user_email]:
            if item['id'] == item_id:
                if 'quantity' in data:
                    item['quantity'] = data['quantity']
                if 'color' in data:
                    item['color'] = data['color']
                if 'storage' in data:
                    item['storage'] = data['storage']
                
                return jsonify({
                    "success": True,
                    "data": item,
                    "message": "Cart item updated"
                })
        
        return jsonify({"success": False, "error": "Item not found in cart"}), 404
        
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@cart_bp.route('/cart/<item_id>', methods=['DELETE'])
@cross_origin()
@jwt_required()
def remove_from_cart(item_id):
    try:
        current_user_email = get_jwt_identity()
        
        if current_user_email not in carts_db:
            return jsonify({"success": False, "error": "Cart not found"}), 404
        
        for i, item in enumerate(carts_db[current_user_email]):
            if item['id'] == item_id:
                removed_item = carts_db[current_user_email].pop(i)
                return jsonify({
                    "success": True,
                    "data": removed_item,
                    "message": "Item removed from cart"
                })
        
        return jsonify({"success": False, "error": "Item not found in cart"}), 404
        
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@cart_bp.route('/cart/clear', methods=['DELETE'])
@cross_origin()
@jwt_required()
def clear_cart():
    try:
        current_user_email = get_jwt_identity()
        
        if current_user_email in carts_db:
            carts_db[current_user_email] = []
        
        return jsonify({
            "success": True,
            "message": "Cart cleared"
        })
        
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500
