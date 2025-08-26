# routes/auth.py
from flask import Blueprint, request, jsonify
from models import User
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from werkzeug.security import generate_password_hash, check_password_hash
import re
from datetime import datetime

auth = Blueprint('auth', __name__)

def validate_email(email):
    """ตรวจสอบรูปแบบ email"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def validate_password(password):
    """ตรวจสอบความแข็งแกร่งของรหัสผ่าน"""
    if len(password) < 6:
        return False, "รหัสผ่านต้องมีความยาวอย่างน้อย 6 ตัวอักษร"
    return True, ""

@auth.route('/register', methods=['POST'])
def register():
    try:
        data = request.get_json()
        
        # ตรวจสอบข้อมูลที่จำเป็น
        if not all(key in data for key in ['username', 'password']):
            return jsonify({"error": "กรุณากรอกข้อมูลให้ครบถ้วน"}), 400
        
        username = data['username'].strip()
        password = data['password']
        first_name = data.get('first_name', '').strip()
        last_name = data.get('last_name', '').strip()
        
        # ตรวจสอบความยาว username
        if len(username) < 3:
            return jsonify({"error": "ชื่อผู้ใช้ต้องมีความยาวอย่างน้อย 3 ตัวอักษร"}), 400
        
        # ตรวจสอบความแข็งแกร่งของรหัสผ่าน
        is_valid, error_msg = validate_password(password)
        if not is_valid:
            return jsonify({"error": error_msg}), 400
        
        # ตรวจสอบว่ามี username ซ้ำหรือไม่
        if User.objects(username=username).first():
            return jsonify({"error": "ชื่อผู้ใช้นี้มีอยู่ในระบบแล้ว"}), 400
        
        # สร้างผู้ใช้ใหม่
        hashed_password = generate_password_hash(password)
        user = User(
            username=username,
            first_name=first_name,
            last_name=last_name,
            password=hashed_password
        )
        user.save()
        
        return jsonify({
            "message": "ลงทะเบียนสำเร็จ",
            "user": {
                "id": str(user.id),
                "username": user.username,
                "profile_picture": user.profile_picture
            }
        }), 201
        
    except Exception as e:
        return jsonify({"error": "เกิดข้อผิดพลาดในระบบ"}), 500

@auth.route('/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        
        # ตรวจสอบข้อมูลที่จำเป็น
        if not all(key in data for key in ['username', 'password']):
            return jsonify({"error": "กรุณากรอกชื่อผู้ใช้และรหัสผ่าน"}), 400
        
        username = data['username'].strip()
        password = data['password']
        
        # ค้นหาผู้ใช้
        user = User.objects(username=username).first()
        
        # ตรวจสอบว่ามีผู้ใช้นี้หรือไม่
        if not user:
            return jsonify({"error": "ชื่อผู้ใช้หรือรหัสผ่านไม่ถูกต้อง"}), 401
        
        # ตรวจสอบรหัสผ่าน
        if not check_password_hash(user.password, password):
            return jsonify({"error": "ชื่อผู้ใช้หรือรหัสผ่านไม่ถูกต้อง"}), 401
        
        # สร้าง JWT token
        token = create_access_token(identity=str(user.id))
        
        return jsonify({
            "message": "เข้าสู่ระบบสำเร็จ",
            "access_token": token,
            "user": {
                "id": str(user.id),
                "username": user.username,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "profile_picture": user.profile_picture
            }
        }), 200
        
    except Exception as e:
        return jsonify({"error": "เกิดข้อผิดพลาดในระบบ"}), 500

@auth.route('/profile', methods=['GET'])
@jwt_required()
def get_profile():
    try:
        user_id = get_jwt_identity()
        user = User.objects(id=user_id).first()
        
        if not user:
            return jsonify({"error": "ไม่พบผู้ใช้"}), 404
        
        return jsonify({
            "user": {
                "id": str(user.id),
                "username": user.username,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "profile_picture": user.profile_picture,
                "created_at": user.created_at.isoformat() if user.created_at else None
            }
        }), 200
        
    except Exception as e:
        return jsonify({"error": "เกิดข้อผิดพลาดในระบบ"}), 500

@auth.route('/profile/update', methods=['PUT'])
@jwt_required()
def update_profile():
    try:
        user_id = get_jwt_identity()
        user = User.objects(id=user_id).first()
        
        if not user:
            return jsonify({"error": "ไม่พบผู้ใช้"}), 404
        
        data = request.get_json()
        
        # ตรวจสอบว่ามีข้อมูลที่ต้องการอัปเดตหรือไม่
        if not data or (not data.get('username') and not data.get('password') and not data.get('first_name') and not data.get('last_name')):
            return jsonify({"error": "กรุณาระบุข้อมูลที่ต้องการอัปเดต"}), 400
        
        # อัปเดต username
        if data.get('username'):
            new_username = data['username'].strip()
            
            # ตรวจสอบความยาว username
            if len(new_username) < 3:
                return jsonify({"error": "ชื่อผู้ใช้ต้องมีความยาวอย่างน้อย 3 ตัวอักษร"}), 400
            
            # ตรวจสอบว่ามี username ซ้ำหรือไม่ (ยกเว้นผู้ใช้ปัจจุบัน)
            existing_user = User.objects(username=new_username).first()
            if existing_user and str(existing_user.id) != user_id:
                return jsonify({"error": "ชื่อผู้ใช้นี้มีอยู่ในระบบแล้ว"}), 400
            
            user.username = new_username
        
        # อัปเดต first_name
        if data.get('first_name') is not None:
            user.first_name = data['first_name'].strip()
        
        # อัปเดต last_name
        if data.get('last_name') is not None:
            user.last_name = data['last_name'].strip()
        
        # อัปเดตรหัสผ่าน
        if data.get('password'):
            new_password = data['password']
            
            # ตรวจสอบความแข็งแกร่งของรหัสผ่าน
            is_valid, error_msg = validate_password(new_password)
            if not is_valid:
                return jsonify({"error": error_msg}), 400
            
            user.password = generate_password_hash(new_password)
        
        # อัปเดตเวลาที่แก้ไข
        user.updated_at = datetime.utcnow()
        user.save()
        
        return jsonify({
            "message": "อัปเดตข้อมูลสำเร็จ",
            "user": {
                "id": str(user.id),
                "username": user.username,
                "profile_picture": user.profile_picture
            }
        }), 200
        
    except Exception as e:
        return jsonify({"error": "เกิดข้อผิดพลาดในระบบ"}), 500

@auth.route('/profile/change-password', methods=['PUT'])
@jwt_required()
def change_password():
    try:
        user_id = get_jwt_identity()
        user = User.objects(id=user_id).first()
        
        if not user:
            return jsonify({"error": "ไม่พบผู้ใช้"}), 404
        
        data = request.get_json()
        
        # ตรวจสอบข้อมูลที่จำเป็น
        if not all(key in data for key in ['current_password', 'new_password']):
            return jsonify({"error": "กรุณากรอกข้อมูลให้ครบถ้วน"}), 400
        
        current_password = data['current_password']
        new_password = data['new_password']
        
        # ตรวจสอบรหัสผ่านปัจจุบัน
        if not check_password_hash(user.password, current_password):
            return jsonify({"error": "รหัสผ่านปัจจุบันไม่ถูกต้อง"}), 401
        
        # ตรวจสอบความแข็งแกร่งของรหัสผ่านใหม่
        is_valid, error_msg = validate_password(new_password)
        if not is_valid:
            return jsonify({"error": error_msg}), 400
        
        # อัปเดตรหัสผ่านใหม่
        user.password = generate_password_hash(new_password)
        user.updated_at = datetime.utcnow()
        user.save()
        
        return jsonify({
            "message": "เปลี่ยนรหัสผ่านสำเร็จ"
        }), 200
        
    except Exception as e:
        return jsonify({"error": "เกิดข้อผิดพลาดในระบบ"}), 500
