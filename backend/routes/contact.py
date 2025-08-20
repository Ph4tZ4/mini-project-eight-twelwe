# routes/contact.py
from flask import Blueprint, request, jsonify
from models import Contact
import re

contact = Blueprint('contact', __name__)

def validate_email(email):
    """ตรวจสอบรูปแบบ email"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

@contact.route('/contact', methods=['POST'])
def submit_contact():
    """ส่งข้อความติดต่อ"""
    try:
        data = request.get_json()
        
        # ตรวจสอบข้อมูลที่จำเป็น
        if not all(key in data for key in ['name', 'email', 'subject', 'message']):
            return jsonify({
                'success': False,
                'error': 'กรุณากรอกข้อมูลให้ครบถ้วน'
            }), 400
        
        name = data['name'].strip()
        email = data['email'].strip().lower()
        subject = data['subject'].strip()
        message = data['message'].strip()
        phone = data.get('phone', '').strip()
        
        # ตรวจสอบความยาวข้อมูล
        if len(name) < 2:
            return jsonify({
                'success': False,
                'error': 'ชื่อต้องมีความยาวอย่างน้อย 2 ตัวอักษร'
            }), 400
        
        if len(subject) < 5:
            return jsonify({
                'success': False,
                'error': 'หัวข้อต้องมีความยาวอย่างน้อย 5 ตัวอักษร'
            }), 400
        
        if len(message) < 10:
            return jsonify({
                'success': False,
                'error': 'ข้อความต้องมีความยาวอย่างน้อย 10 ตัวอักษร'
            }), 400
        
        # ตรวจสอบรูปแบบ email
        if not validate_email(email):
            return jsonify({
                'success': False,
                'error': 'รูปแบบอีเมลไม่ถูกต้อง'
            }), 400
        
        # สร้างข้อความติดต่อใหม่
        contact_message = Contact(
            name=name,
            email=email,
            subject=subject,
            message=message,
            phone=phone
        )
        contact_message.save()
        
        return jsonify({
            'success': True,
            'message': 'ส่งข้อความติดต่อสำเร็จ เราจะติดต่อกลับโดยเร็วที่สุด'
        }), 201
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': 'เกิดข้อผิดพลาดในการส่งข้อความติดต่อ'
        }), 500

@contact.route('/contact', methods=['GET'])
def get_contacts():
    """ดึงข้อมูลข้อความติดต่อทั้งหมด (สำหรับ admin)"""
    try:
        # Query parameters
        page = int(request.args.get('page', 1))
        limit = int(request.args.get('limit', 20))
        is_read = request.args.get('is_read')
        
        # Build query
        query = Contact.objects
        
        if is_read is not None:
            query = query.filter(is_read=is_read)
        
        # Sorting
        query = query.order_by('-created_at')
        
        # Pagination
        total_contacts = query.count()
        total_pages = (total_contacts + limit - 1) // limit
        offset = (page - 1) * limit
        
        contacts_list = query.skip(offset).limit(limit)
        
        # Format response
        contacts_data = []
        for contact_msg in contacts_list:
            contacts_data.append({
                'id': str(contact_msg.id),
                'name': contact_msg.name,
                'email': contact_msg.email,
                'subject': contact_msg.subject,
                'message': contact_msg.message,
                'phone': contact_msg.phone,
                'is_read': contact_msg.is_read,
                'created_at': contact_msg.created_at.isoformat()
            })
        
        return jsonify({
            'success': True,
            'contacts': contacts_data,
            'pagination': {
                'page': page,
                'limit': limit,
                'total_contacts': total_contacts,
                'total_pages': total_pages
            }
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': 'เกิดข้อผิดพลาดในการดึงข้อมูลข้อความติดต่อ'
        }), 500

@contact.route('/contact/<contact_id>', methods=['GET'])
def get_contact_by_id(contact_id):
    """ดึงข้อมูลข้อความติดต่อตาม ID"""
    try:
        contact_msg = Contact.objects(id=contact_id).first()
        
        if not contact_msg:
            return jsonify({
                'success': False,
                'error': 'ไม่พบข้อความติดต่อนี้'
            }), 404
        
        contact_data = {
            'id': str(contact_msg.id),
            'name': contact_msg.name,
            'email': contact_msg.email,
            'subject': contact_msg.subject,
            'message': contact_msg.message,
            'phone': contact_msg.phone,
            'is_read': contact_msg.is_read,
            'created_at': contact_msg.created_at.isoformat()
        }
        
        return jsonify({
            'success': True,
            'contact': contact_data
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': 'เกิดข้อผิดพลาดในการดึงข้อมูลข้อความติดต่อ'
        }), 500

@contact.route('/contact/<contact_id>/read', methods=['PUT'])
def mark_contact_as_read(contact_id):
    """ทำเครื่องหมายว่าอ่านข้อความแล้ว"""
    try:
        contact_msg = Contact.objects(id=contact_id).first()
        
        if not contact_msg:
            return jsonify({
                'success': False,
                'error': 'ไม่พบข้อความติดต่อนี้'
            }), 404
        
        contact_msg.is_read = True
        contact_msg.save()
        
        return jsonify({
            'success': True,
            'message': 'ทำเครื่องหมายว่าอ่านแล้ว'
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': 'เกิดข้อผิดพลาดในการอัปเดตสถานะ'
        }), 500
