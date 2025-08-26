from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import Order, ShippingTracking, ShippingHistory, ShippingStatus, User
from mongoengine.errors import DoesNotExist, ValidationError
from datetime import datetime

shipping = Blueprint('shipping', __name__)

@shipping.route('/tracking/<tracking_number>', methods=['GET'])
def track_shipment(tracking_number):
    """Track shipment by tracking number (public endpoint)"""
    try:
        tracking = ShippingTracking.objects(tracking_number=tracking_number).first()
        if not tracking:
            return jsonify({'success': False, 'message': 'Tracking number not found'}), 404
        
        # Get shipping history
        history = ShippingHistory.objects(tracking=tracking).first()
        
        # Prepare tracking data
        tracking_data = {
            'tracking_number': tracking.tracking_number,
            'carrier': tracking.carrier,
            'current_status': tracking.current_status,
            'estimated_delivery': tracking.estimated_delivery.isoformat() if tracking.estimated_delivery else None,
            'actual_delivery': tracking.actual_delivery.isoformat() if tracking.actual_delivery else None,
            'order_info': {
                'order_number': tracking.order.order_number,
                'total_amount': tracking.order.total_amount,
                'created_at': tracking.order.created_at.isoformat()
            },
            'shipping_address': {
                'full_name': tracking.order.shipping_address.full_name,
                'city': tracking.order.shipping_address.city,
                'province': tracking.order.shipping_address.province,
                'postal_code': tracking.order.shipping_address.postal_code
            },
            'status_history': []
        }
        
        if history:
            tracking_data['status_history'] = [
                {
                    'status': status.status,
                    'description': status.description,
                    'location': status.location,
                    'timestamp': status.timestamp.isoformat()
                }
                for status in history.status_history
            ]
        
        # Add status descriptions
        status_descriptions = {
            'order_placed': 'คำสั่งซื้อได้รับการยืนยัน',
            'preparing': 'กำลังเตรียมสินค้า',
            'picked_up': 'สินค้าถูกรับเข้าระบบขนส่ง',
            'in_transit': 'สินค้าอยู่ระหว่างการขนส่ง',
            'out_for_delivery': 'สินค้าออกจัดส่งแล้ว',
            'delivered': 'จัดส่งสำเร็จ'
        }
        
        tracking_data['current_status_description'] = status_descriptions.get(
            tracking.current_status, 
            tracking.current_status
        )
        
        return jsonify({
            'success': True,
            'tracking': tracking_data
        })
        
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@shipping.route('/my-shipments', methods=['GET'])
@jwt_required()
def get_user_shipments():
    """Get all shipments for the authenticated user"""
    try:
        user_id = get_jwt_identity()
        user = User.objects(id=user_id).first()
        if not user:
            return jsonify({'success': False, 'message': 'User not found'}), 404
        
        # Get all orders for the user
        orders = Order.objects(user=user).order_by('-created_at')
        
        shipments = []
        for order in orders:
            tracking = ShippingTracking.objects(order=order).first()
            if tracking:
                shipment_data = {
                    'order_number': order.order_number,
                    'tracking_number': tracking.tracking_number,
                    'current_status': tracking.current_status,
                    'estimated_delivery': tracking.estimated_delivery.isoformat() if tracking.estimated_delivery else None,
                    'carrier': tracking.carrier,
                    'order_total': order.total_amount,
                    'created_at': order.created_at.isoformat()
                }
                shipments.append(shipment_data)
        
        return jsonify({
            'success': True,
            'shipments': shipments
        })
        
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@shipping.route('/update-status/<tracking_number>', methods=['POST'])
def update_shipping_status(tracking_number):
    """Update shipping status (for admin/shipping company use)"""
    try:
        data = request.get_json()
        if not data or 'status' not in data:
            return jsonify({'success': False, 'message': 'Status is required'}), 400
        
        tracking = ShippingTracking.objects(tracking_number=tracking_number).first()
        if not tracking:
            return jsonify({'success': False, 'message': 'Tracking number not found'}), 404
        
        new_status = data['status']
        description = data.get('description', '')
        location = data.get('location', '')
        
        # Validate status
        valid_statuses = ['order_placed', 'preparing', 'picked_up', 'in_transit', 'out_for_delivery', 'delivered']
        if new_status not in valid_statuses:
            return jsonify({'success': False, 'message': 'Invalid status'}), 400
        
        # Update tracking
        tracking.current_status = new_status
        if new_status == 'delivered':
            tracking.actual_delivery = datetime.utcnow()
            # Update order status
            tracking.order.order_status = 'delivered'
            tracking.order.delivered_at = datetime.utcnow()
            tracking.order.save()
        elif new_status == 'in_transit' and not tracking.order.shipped_at:
            tracking.order.order_status = 'shipped'
            tracking.order.shipped_at = datetime.utcnow()
            tracking.order.save()
        
        tracking.save()
        
        # Add to shipping history
        history = ShippingHistory.objects(tracking=tracking).first()
        if not history:
            history = ShippingHistory(tracking=tracking)
        
        new_status_entry = ShippingStatus(
            status=new_status,
            description=description or f'สถานะอัปเดตเป็น {new_status}',
            location=location,
            timestamp=datetime.utcnow()
        )
        
        history.status_history.append(new_status_entry)
        history.save()
        
        return jsonify({
            'success': True,
            'message': 'Shipping status updated successfully',
            'current_status': new_status
        })
        
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@shipping.route('/provinces', methods=['GET'])
def get_provinces():
    """Get list of Thai provinces for shipping address"""
    provinces = [
        'กรุงเทพมหานคร', 'กระบี่', 'กาญจนบุรี', 'กาฬสินธุ์', 'กำแพงเพชร',
        'ขอนแก่น', 'จันทบุรี', 'ฉะเชิงเทรา', 'ชลบุรี', 'ชัยนาท',
        'ชัยภูมิ', 'ชุมพร', 'เชียงราย', 'เชียงใหม่', 'ตรัง',
        'ตราด', 'ตาก', 'นครนายก', 'นครปฐม', 'นครพนม',
        'นครราชสีมา', 'นครศรีธรรมราช', 'นครสวรรค์', 'นนทบุรี', 'นราธิวาส',
        'น่าน', 'บึงกาฬ', 'บุรีรัมย์', 'ปทุมธานี', 'ประจวบคีรีขันธ์',
        'ปราจีนบุรี', 'ปัตตานี', 'พระนครศรีอยุธยา', 'พังงา', 'พัทลุง',
        'พิจิตร', 'พิษณุโลก', 'เพชรบุรี', 'เพชรบูรณ์', 'แพร่',
        'พะเยา', 'ภูเก็ต', 'มหาสารคาม', 'มุกดาหาร', 'แม่ฮ่องสอน',
        'ยะลา', 'ยโสธร', 'ร้อยเอ็ด', 'ระนอง', 'ระยอง',
        'ราชบุรี', 'ลพบุรี', 'ลำปาง', 'ลำพูน', 'เลย',
        'ศรีสะเกษ', 'สกลนคร', 'สงขลา', 'สตูล', 'สมุทรปราการ',
        'สมุทรสงคราม', 'สมุทรสาคร', 'สระแก้ว', 'สระบุรี', 'สิงห์บุรี',
        'สุโขทัย', 'สุพรรณบุรี', 'สุราษฎร์ธานี', 'สุรินทร์', 'หนองคาย',
        'หนองบัวลำภู', 'อ่างทอง', 'อุดรธานี', 'อุทัยธานี', 'อุตรดิตถ์',
        'อุบลราชธานี', 'อำนาจเจริญ'
    ]
    
    return jsonify({
        'success': True,
        'provinces': provinces
    })
