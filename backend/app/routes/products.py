from flask import Blueprint, jsonify
from flask_cors import cross_origin

products_bp = Blueprint('products', __name__)

# Each iPhone now has a UNIQUE image from Unsplash
iphones_data = [
    {
        "id": "iphone-16-pro",
        "name": "iPhone 16 Pro",
        "model": "16 Pro",
        "price": 999.00,
        "description": "The ultimate iPhone experience with A18 Pro chip, titanium design, and revolutionary camera system.",
        "colors": ["Space Black", "Silver", "Gold", "Deep Purple"],
        "storage": [128, 256, 512, 1024],
        "imageUrl": "https://images.unsplash.com/photo-1592921870789-04563d55041c?auto=format&fit=crop&w=800&q=80",  # UNIQUE
        "inStock": True,
        "stockQuantity": 50,
        "specs": {
            "display": "6.7-inch Super Retina XDR",
            "chip": "A18 Pro",
            "camera": "48MP Main + 12MP Ultra Wide + 12MP Telephoto",
            "battery": "Up to 29 hours video playback",
            "connectivity": "5G, Wi-Fi 6E, Bluetooth 5.3"
        }
    },
    {
        "id": "iphone-16",
        "name": "iPhone 16",
        "model": "16",
        "price": 799.00,
        "description": "Advanced dual-camera system with Photonic Engine. All-day battery life.",
        "colors": ["Blue", "Pink", "Yellow", "Green", "Black"],
        "storage": [128, 256, 512],
        "imageUrl": "https://images.unsplash.com/photo-1511707171634-5f897ff02aa9?auto=format&fit=crop&w=800&q=80",  # UNIQUE
        "inStock": True,
        "stockQuantity": 100,
        "specs": {
            "display": "6.1-inch Super Retina XDR",
            "chip": "A17 Bionic",
            "camera": "48MP Main + 12MP Ultra Wide",
            "battery": "Up to 20 hours video playback",
            "connectivity": "5G, Wi-Fi 6, Bluetooth 5.3"
        }
    },
    {
        "id": "iphone-15-pro",
        "name": "iPhone 15 Pro",
        "model": "15 Pro",
        "price": 899.00,
        "description": "Forged in titanium and featuring the groundbreaking A17 Pro chip.",
        "colors": ["Black Titanium", "White Titanium", "Blue Titanium", "Natural Titanium"],
        "storage": [128, 256, 512],
        "imageUrl": "https://images.unsplash.com/photo-1605236453806-6ff36851218e?auto=format&fit=crop&w=800&q=80",  # UNIQUE
        "inStock": True,
        "stockQuantity": 25,
        "specs": {
            "display": "6.1-inch Super Retina XDR",
            "chip": "A17 Pro",
            "camera": "48MP Main + 12MP Ultra Wide + 12MP 3x Telephoto",
            "battery": "Up to 23 hours video playback",
            "connectivity": "5G, Wi-Fi 6E, Bluetooth 5.3"
        }
    },
    {
        "id": "iphone-15",
        "name": "iPhone 15",
        "model": "15",
        "price": 699.00,
        "description": "Dynamic Island. 48MP Main camera. USB-C.",
        "colors": ["Blue", "Pink", "Yellow", "Green", "Black"],
        "storage": [128, 256],
        "imageUrl": "https://images.unsplash.com/photo-1592750475338-74b7b21085ab?auto=format&fit=crop&w=800&q=80",  # UNIQUE
        "inStock": True,
        "stockQuantity": 75,
        "specs": {
            "display": "6.1-inch Super Retina XDR",
            "chip": "A16 Bionic",
            "camera": "48MP Main + 12MP Ultra Wide",
            "battery": "Up to 20 hours video playback",
            "connectivity": "5G, Wi-Fi 6, Bluetooth 5.3"
        }
    }
]

@products_bp.route('/products', methods=['GET'])
@cross_origin()
def get_products():
    return jsonify({
        "success": True,
        "data": iphones_data,
        "count": len(iphones_data)
    })

@products_bp.route('/products/<product_id>', methods=['GET'])
@cross_origin()
def get_product(product_id):
    product = next((p for p in iphones_data if p['id'] == product_id), None)
    if product:
        return jsonify({"success": True, "data": product})
    return jsonify({"success": False, "error": "Product not found"}), 404
