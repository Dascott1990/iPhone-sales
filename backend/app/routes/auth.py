from flask import Blueprint, jsonify, request
from flask_cors import cross_origin
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
import uuid
from datetime import timedelta
from app.models.user import User, db

auth_bp = Blueprint('auth', __name__)

# Mock users database (in production, use real database)
users_db = {}

@auth_bp.route('/login', methods=['POST'])
@cross_origin()
def login():
    try:
        data = request.get_json()
        
        if not data or not data.get('email') or not data.get('password'):
            return jsonify({"success": False, "error": "Email and password required"}), 400
        
        # Mock authentication - in production, check against database
        # For demo, accept any credentials
        access_token = create_access_token(
            identity=data['email'],
            expires_delta=timedelta(days=7)
        )
        
        # Create or get user
        user_id = str(uuid.uuid4())
        if data['email'] not in users_db:
            users_db[data['email']] = {
                'id': user_id,
                'email': data['email'],
                'name': data.get('name', 'New User'),
                'phone': data.get('phone', ''),
                'address': data.get('address', '')
            }
        
        user = users_db[data['email']]
        
        return jsonify({
            "success": True,
            "data": {
                "token": access_token,
                "user": user
            },
            "message": "Login successful"
        })
        
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@auth_bp.route('/register', methods=['POST'])
@cross_origin()
def register():
    try:
        data = request.get_json()
        
        required_fields = ['email', 'password', 'name']
        for field in required_fields:
            if not data.get(field):
                return jsonify({"success": False, "error": f"{field} is required"}), 400
        
        if data['email'] in users_db:
            return jsonify({"success": False, "error": "Email already registered"}), 400
        
        # Create new user
        user_id = str(uuid.uuid4())
        users_db[data['email']] = {
            'id': user_id,
            'email': data['email'],
            'name': data['name'],
            'phone': data.get('phone', ''),
            'address': data.get('address', '')
        }
        
        # Create access token
        access_token = create_access_token(
            identity=data['email'],
            expires_delta=timedelta(days=7)
        )
        
        return jsonify({
            "success": True,
            "data": {
                "token": access_token,
                "user": users_db[data['email']]
            },
            "message": "Registration successful"
        }), 201
        
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@auth_bp.route('/profile', methods=['GET'])
@cross_origin()
@jwt_required()
def get_profile():
    try:
        current_user_email = get_jwt_identity()
        
        if current_user_email not in users_db:
            return jsonify({"success": False, "error": "User not found"}), 404
        
        return jsonify({
            "success": True,
            "data": users_db[current_user_email]
        })
        
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@auth_bp.route('/profile', methods=['PUT'])
@cross_origin()
@jwt_required()
def update_profile():
    try:
        current_user_email = get_jwt_identity()
        data = request.get_json()
        
        if current_user_email not in users_db:
            return jsonify({"success": False, "error": "User not found"}), 404
        
        # Update user profile
        if 'name' in data:
            users_db[current_user_email]['name'] = data['name']
        if 'phone' in data:
            users_db[current_user_email]['phone'] = data['phone']
        if 'address' in data:
            users_db[current_user_email]['address'] = data['address']
        
        return jsonify({
            "success": True,
            "data": users_db[current_user_email],
            "message": "Profile updated successfully"
        })
        
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500
