from flask import Blueprint, jsonify, request
from flask_cors import cross_origin

orders_bp = Blueprint('orders', __name__)

# Mock orders data
orders = []

@orders_bp.route('/orders', methods=['GET'])
@cross_origin()
def get_orders():
    return jsonify({
        "success": True,
        "data": orders,
        "count": len(orders)
    })

@orders_bp.route('/orders', methods=['POST'])
@cross_origin()
def create_order():
    data = request.get_json()
    
    if not data:
        return jsonify({"success": False, "error": "No data provided"}), 400
    
    # Create a simple order object
    order = {
        "id": f"order_{len(orders) + 1}",
        "items": data.get('items', []),
        "total": data.get('total', 0),
        "status": "processing",
        "createdAt": "2024-01-01T00:00:00Z"
    }
    
    orders.append(order)
    
    return jsonify({
        "success": True,
        "data": order,
        "message": "Order created successfully"
    }), 201
