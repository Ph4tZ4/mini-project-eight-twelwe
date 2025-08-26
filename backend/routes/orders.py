from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import Order, OrderItem, Payment, ShippingAddress, ShippingTracking, ShippingHistory, ShippingStatus, Cart, Product, User
from mongoengine.errors import DoesNotExist, ValidationError
from datetime import datetime, timedelta
import random
import string

orders = Blueprint('orders', __name__)

@orders.route('/checkout', methods=['POST'])
@jwt_required()
def create_order():
    """Create a new order from cart"""
    try:
        user_id = get_jwt_identity()
        user = User.objects(id=user_id).first()
        if not user:
            return jsonify({'success': False, 'message': 'User not found'}), 404
        
        data = request.get_json()
        if not data:
            return jsonify({'success': False, 'message': 'No data provided'}), 400
        
        # Get user's cart
        cart = Cart.objects(user=user).first()
        if not cart or not cart.items:
            return jsonify({'success': False, 'message': 'Cart is empty'}), 400
        
        # Validate required fields
        required_fields = ['shipping_address', 'payment_method']
        for field in required_fields:
            if field not in data:
                return jsonify({'success': False, 'message': f'{field} is required'}), 400
        
        # Validate shipping address
        shipping_data = data['shipping_address']
        required_address_fields = ['full_name', 'phone', 'address_line_1', 'city', 'province', 'postal_code']
        for field in required_address_fields:
            if field not in shipping_data:
                return jsonify({'success': False, 'message': f'Shipping address {field} is required'}), 400
        
        # Create shipping address
        shipping_address = ShippingAddress(
            full_name=shipping_data['full_name'],
            phone=shipping_data['phone'],
            address_line_1=shipping_data['address_line_1'],
            address_line_2=shipping_data.get('address_line_2', ''),
            city=shipping_data['city'],
            province=shipping_data['province'],
            postal_code=shipping_data['postal_code'],
            country=shipping_data.get('country', 'Thailand')
        )
        
        # Calculate totals
        subtotal = 0
        order_items = []
        
        for cart_item in cart.items:
            if not cart_item.product:
                continue
            
            # Check stock availability
            if cart_item.quantity > cart_item.product.stock_quantity:
                return jsonify({
                    'success': False, 
                    'message': f'Insufficient stock for {cart_item.product.name}. Available: {cart_item.product.stock_quantity}'
                }), 400
            
            item_total = cart_item.product.price * cart_item.quantity
            subtotal += item_total
            
            order_item = OrderItem(
                product=cart_item.product,
                quantity=cart_item.quantity,
                price_at_order=cart_item.product.price,
                total_price=item_total
            )
            order_items.append(order_item)
        
        # Calculate shipping and tax
        shipping_fee = 50.0 if subtotal < 1000 else 0.0  # Free shipping over 1000 THB
        tax_rate = 0.07  # 7% VAT
        tax = subtotal * tax_rate
        total_amount = subtotal + shipping_fee + tax
        
        # Create payment record
        payment = Payment(
            payment_method=data['payment_method'],
            amount=total_amount,
            payment_status='pending'
        )
        payment.save()
        
        # Create order
        order = Order(
            user=user,
            items=order_items,
            shipping_address=shipping_address,
            payment=payment,
            subtotal=subtotal,
            shipping_fee=shipping_fee,
            tax=tax,
            total_amount=total_amount,
            notes=data.get('notes', '')
        )
        order.save()
        
        # Create shipping tracking
        estimated_delivery = datetime.utcnow() + timedelta(days=3)
        tracking = ShippingTracking(
            order=order,
            estimated_delivery=estimated_delivery
        )
        tracking.save()
        
        # Create initial shipping history
        shipping_history = ShippingHistory(
            tracking=tracking,
            status_history=[
                ShippingStatus(
                    status='order_placed',
                    description='คำสั่งซื้อได้รับการยืนยันแล้ว',
                    location='ShopHub Warehouse',
                    timestamp=datetime.utcnow()
                )
            ]
        )
        shipping_history.save()
        
        # Update product stock
        for cart_item in cart.items:
            if cart_item.product:
                cart_item.product.stock_quantity -= cart_item.quantity
                cart_item.product.save()
        
        # Clear cart
        cart.items = []
        cart.save()
        
        # Process payment if it's cash on delivery
        if data['payment_method'] == 'cash_on_delivery':
            payment.payment_status = 'paid'
            payment.payment_date = datetime.utcnow()
            payment.save()
            
            order.order_status = 'confirmed'
            order.confirmed_at = datetime.utcnow()
            order.save()
        
        return jsonify({
            'success': True,
            'message': 'Order created successfully',
            'order': {
                'order_number': order.order_number,
                'total_amount': order.total_amount,
                'payment_method': payment.payment_method,
                'tracking_number': tracking.tracking_number,
                'estimated_delivery': estimated_delivery.isoformat()
            }
        })
        
    except ValidationError as e:
        return jsonify({'success': False, 'message': f'Validation error: {str(e)}'}), 400
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@orders.route('/orders', methods=['GET'])
@jwt_required()
def get_user_orders():
    """Get user's order history"""
    try:
        user_id = get_jwt_identity()
        user = User.objects(id=user_id).first()
        if not user:
            return jsonify({'success': False, 'message': 'User not found'}), 404
        
        orders_list = Order.objects(user=user).order_by('-created_at')
        
        orders_data = []
        for order in orders_list:
            # Get tracking info
            tracking = ShippingTracking.objects(order=order).first()
            
            order_data = {
                'id': str(order.id),
                'order_number': order.order_number,
                'order_status': order.order_status,
                'subtotal': order.subtotal,
                'shipping_fee': order.shipping_fee,
                'tax': order.tax,
                'total_amount': order.total_amount,
                'payment_method': order.payment.payment_method,
                'payment_status': order.payment.payment_status,
                'created_at': order.created_at.isoformat(),
                'tracking_number': tracking.tracking_number if tracking else None,
                'items': [
                    {
                        'product_name': item.product.name if item.product else 'Product not found',
                        'quantity': item.quantity,
                        'price_at_order': item.price_at_order,
                        'total_price': item.total_price
                    }
                    for item in order.items
                ]
            }
            orders_data.append(order_data)
        
        return jsonify({
            'success': True,
            'orders': orders_data
        })
        
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@orders.route('/orders/<order_id>', methods=['GET'])
@jwt_required()
def get_order_details(order_id):
    """Get detailed order information"""
    try:
        user_id = get_jwt_identity()
        user = User.objects(id=user_id).first()
        if not user:
            return jsonify({'success': False, 'message': 'User not found'}), 404
        
        order = Order.objects(id=order_id, user=user).first()
        if not order:
            return jsonify({'success': False, 'message': 'Order not found'}), 404
        
        # Get tracking info
        tracking = ShippingTracking.objects(order=order).first()
        
        order_data = {
            'id': str(order.id),
            'order_number': order.order_number,
            'order_status': order.order_status,
            'subtotal': order.subtotal,
            'shipping_fee': order.shipping_fee,
            'tax': order.tax,
            'total_amount': order.total_amount,
            'payment': {
                'method': order.payment.payment_method,
                'status': order.payment.payment_status,
                'transaction_id': order.payment.transaction_id,
                'payment_date': order.payment.payment_date.isoformat() if order.payment.payment_date else None
            },
            'shipping_address': {
                'full_name': order.shipping_address.full_name,
                'phone': order.shipping_address.phone,
                'address_line_1': order.shipping_address.address_line_1,
                'address_line_2': order.shipping_address.address_line_2,
                'city': order.shipping_address.city,
                'province': order.shipping_address.province,
                'postal_code': order.shipping_address.postal_code,
                'country': order.shipping_address.country
            },
            'items': [
                {
                    'product': {
                        'id': str(item.product.id) if item.product else None,
                        'name': item.product.name if item.product else 'Product not found',
                        'images': item.product.images if item.product else []
                    },
                    'quantity': item.quantity,
                    'price_at_order': item.price_at_order,
                    'total_price': item.total_price
                }
                for item in order.items
            ],
            'tracking': {
                'tracking_number': tracking.tracking_number,
                'carrier': tracking.carrier,
                'current_status': tracking.current_status,
                'estimated_delivery': tracking.estimated_delivery.isoformat() if tracking.estimated_delivery else None,
                'actual_delivery': tracking.actual_delivery.isoformat() if tracking.actual_delivery else None
            } if tracking else None,
            'created_at': order.created_at.isoformat(),
            'confirmed_at': order.confirmed_at.isoformat() if order.confirmed_at else None,
            'shipped_at': order.shipped_at.isoformat() if order.shipped_at else None,
            'delivered_at': order.delivered_at.isoformat() if order.delivered_at else None,
            'notes': order.notes
        }
        
        return jsonify({
            'success': True,
            'order': order_data
        })
        
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500
