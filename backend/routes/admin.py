# routes/admin.py
from flask import Blueprint, request, jsonify
from models import User, Product, Category, Order, Contact, Cart
from flask_jwt_extended import jwt_required, get_jwt_identity, create_access_token
from werkzeug.security import check_password_hash
from functools import wraps
from datetime import datetime, timedelta
import mongoengine

admin = Blueprint('admin', __name__)

def admin_required(f):
    """Decorator to require admin access"""
    @wraps(f)
    @jwt_required()
    def decorated_function(*args, **kwargs):
        user_id = get_jwt_identity()
        user = User.objects(id=user_id).first()
        
        if not user or not user.is_admin:
            return jsonify({"error": "Admin access required"}), 403
        
        return f(*args, **kwargs)
    return decorated_function

@admin.route('/login', methods=['POST'])
def admin_login():
    """Admin login endpoint"""
    try:
        data = request.get_json()
        
        if not all(key in data for key in ['username', 'password']):
            return jsonify({"error": "กรุณากรอกชื่อผู้ใช้และรหัสผ่าน"}), 400
        
        username = data['username'].strip()
        password = data['password']
        
        # Find user
        user = User.objects(username=username).first()
        
        if not user:
            return jsonify({"error": "ชื่อผู้ใช้หรือรหัสผ่านไม่ถูกต้อง"}), 401
        
        # Check if user is admin
        if not user.is_admin:
            return jsonify({"error": "คุณไม่มีสิทธิ์เข้าถึงระบบผู้ดูแล"}), 403
        
        # Check password
        if not check_password_hash(user.password, password):
            return jsonify({"error": "ชื่อผู้ใช้หรือรหัสผ่านไม่ถูกต้อง"}), 401
        
        # Create JWT token
        token = create_access_token(identity=str(user.id))
        
        return jsonify({
            "message": "เข้าสู่ระบบผู้ดูแลสำเร็จ",
            "access_token": token,
            "user": {
                "id": str(user.id),
                "username": user.username,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "profile_picture": user.profile_picture,
                "is_admin": user.is_admin
            }
        }), 200
        
    except Exception as e:
        return jsonify({"error": "เกิดข้อผิดพลาดในระบบ"}), 500

@admin.route('/dashboard/stats', methods=['GET'])
@admin_required
def dashboard_stats():
    """Get dashboard statistics"""
    try:
        # Calculate date ranges
        today = datetime.utcnow().date()
        yesterday = today - timedelta(days=1)
        this_month_start = today.replace(day=1)
        last_month_start = (this_month_start - timedelta(days=1)).replace(day=1)
        
        # User statistics
        total_users = User.objects.count()
        new_users_today = User.objects(created_at__gte=datetime.combine(today, datetime.min.time())).count()
        new_users_this_month = User.objects(created_at__gte=datetime.combine(this_month_start, datetime.min.time())).count()
        
        # Product statistics
        total_products = Product.objects.count()
        active_products = Product.objects(is_active=True).count()
        featured_products = Product.objects(is_featured=True).count()
        out_of_stock = Product.objects(stock_quantity=0).count()
        
        # Order statistics
        total_orders = Order.objects.count()
        pending_orders = Order.objects(order_status='pending').count()
        confirmed_orders = Order.objects(order_status='confirmed').count()
        shipped_orders = Order.objects(order_status='shipped').count()
        delivered_orders = Order.objects(order_status='delivered').count()
        
        orders_today = Order.objects(created_at__gte=datetime.combine(today, datetime.min.time())).count()
        orders_this_month = Order.objects(created_at__gte=datetime.combine(this_month_start, datetime.min.time())).count()
        
        # Revenue calculation
        total_revenue = 0
        revenue_today = 0
        revenue_this_month = 0
        
        try:
            # Calculate total revenue from all delivered orders
            delivered_order_aggregation = Order.objects(order_status='delivered').aggregate([
                {"$group": {"_id": None, "total": {"$sum": "$total_amount"}}}
            ])
            total_revenue = next(delivered_order_aggregation, {}).get('total', 0) or 0
            
            # Revenue today
            today_orders_aggregation = Order.objects(
                order_status='delivered',
                delivered_at__gte=datetime.combine(today, datetime.min.time())
            ).aggregate([
                {"$group": {"_id": None, "total": {"$sum": "$total_amount"}}}
            ])
            revenue_today = next(today_orders_aggregation, {}).get('total', 0) or 0
            
            # Revenue this month
            month_orders_aggregation = Order.objects(
                order_status='delivered',
                delivered_at__gte=datetime.combine(this_month_start, datetime.min.time())
            ).aggregate([
                {"$group": {"_id": None, "total": {"$sum": "$total_amount"}}}
            ])
            revenue_this_month = next(month_orders_aggregation, {}).get('total', 0) or 0
            
        except Exception as e:
            print(f"Revenue calculation error: {e}")
            # Fallback to simple calculation
            delivered_orders = Order.objects(order_status='delivered')
            total_revenue = sum(order.total_amount for order in delivered_orders)
            
            today_delivered = Order.objects(
                order_status='delivered',
                delivered_at__gte=datetime.combine(today, datetime.min.time())
            )
            revenue_today = sum(order.total_amount for order in today_delivered)
            
            month_delivered = Order.objects(
                order_status='delivered',
                delivered_at__gte=datetime.combine(this_month_start, datetime.min.time())
            )
            revenue_this_month = sum(order.total_amount for order in month_delivered)
        
        # Category statistics
        total_categories = Category.objects.count()
        active_categories = Category.objects(is_active=True).count()
        
        # Contact messages
        total_contacts = Contact.objects.count()
        unread_contacts = Contact.objects(is_read=False).count()
        
        # Active carts
        active_carts = Cart.objects(items__exists=True, items__not__size=0).count()
        
        return jsonify({
            "users": {
                "total": total_users,
                "new_today": new_users_today,
                "new_this_month": new_users_this_month
            },
            "products": {
                "total": total_products,
                "active": active_products,
                "featured": featured_products,
                "out_of_stock": out_of_stock
            },
            "orders": {
                "total": total_orders,
                "pending": pending_orders,
                "confirmed": confirmed_orders,
                "shipped": shipped_orders,
                "delivered": delivered_orders,
                "today": orders_today,
                "this_month": orders_this_month
            },
            "revenue": {
                "total": round(total_revenue, 2),
                "today": round(revenue_today, 2),
                "this_month": round(revenue_this_month, 2)
            },
            "categories": {
                "total": total_categories,
                "active": active_categories
            },
            "contacts": {
                "total": total_contacts,
                "unread": unread_contacts
            },
            "carts": {
                "active": active_carts
            }
        }), 200
        
    except Exception as e:
        print(f"Dashboard stats error: {e}")
        return jsonify({"error": "เกิดข้อผิดพลาดในการดึงข้อมูลสถิติ"}), 500

@admin.route('/users', methods=['GET'])
@admin_required
def get_users():
    """Get all users with pagination"""
    try:
        page = int(request.args.get('page', 1))
        limit = int(request.args.get('limit', 20))
        search = request.args.get('search', '')
        
        # Build query
        query = {}
        if search:
            query['username__icontains'] = search
        
        # Calculate pagination
        offset = (page - 1) * limit
        
        # Get users
        users_query = User.objects(**query)
        total_users = users_query.count()
        users = users_query.skip(offset).limit(limit)
        
        users_data = []
        for user in users:
            users_data.append({
                "id": str(user.id),
                "username": user.username,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "is_admin": user.is_admin,
                "created_at": user.created_at.isoformat() if user.created_at else None,
                "updated_at": user.updated_at.isoformat() if user.updated_at else None
            })
        
        return jsonify({
            "users": users_data,
            "pagination": {
                "page": page,
                "limit": limit,
                "total": total_users,
                "pages": (total_users + limit - 1) // limit
            }
        }), 200
        
    except Exception as e:
        return jsonify({"error": "เกิดข้อผิดพลาดในการดึงข้อมูลผู้ใช้"}), 500

@admin.route('/users/<user_id>/toggle-admin', methods=['PUT'])
@admin_required
def toggle_admin_status(user_id):
    """Toggle admin status of a user"""
    try:
        user = User.objects(id=user_id).first()
        
        if not user:
            return jsonify({"error": "ไม่พบผู้ใช้"}), 404
        
        # Toggle admin status
        user.is_admin = not user.is_admin
        user.updated_at = datetime.utcnow()
        user.save()
        
        return jsonify({
            "message": f"เปลี่ยนสถานะผู้ดูแลของ {user.username} สำเร็จ",
            "user": {
                "id": str(user.id),
                "username": user.username,
                "is_admin": user.is_admin
            }
        }), 200
        
    except Exception as e:
        return jsonify({"error": "เกิดข้อผิดพลาดในการเปลี่ยนสถานะผู้ดูแล"}), 500

@admin.route('/orders', methods=['GET'])
@admin_required
def get_orders():
    """Get all orders with pagination and filtering"""
    try:
        page = int(request.args.get('page', 1))
        limit = int(request.args.get('limit', 20))
        status = request.args.get('status', '')
        
        # Build query
        query = {}
        if status:
            query['order_status'] = status
        
        # Calculate pagination
        offset = (page - 1) * limit
        
        # Get orders
        orders_query = Order.objects(**query).order_by('-created_at')
        total_orders = orders_query.count()
        orders = orders_query.skip(offset).limit(limit)
        
        orders_data = []
        for order in orders:
            orders_data.append({
                "id": str(order.id),
                "order_number": order.order_number,
                "user": {
                    "id": str(order.user.id),
                    "username": order.user.username
                } if order.user else None,
                "total_amount": order.total_amount,
                "order_status": order.order_status,
                "created_at": order.created_at.isoformat() if order.created_at else None,
                "items_count": len(order.items) if order.items else 0
            })
        
        return jsonify({
            "orders": orders_data,
            "pagination": {
                "page": page,
                "limit": limit,
                "total": total_orders,
                "pages": (total_orders + limit - 1) // limit
            }
        }), 200
        
    except Exception as e:
        return jsonify({"error": "เกิดข้อผิดพลาดในการดึงข้อมูลคำสั่งซื้อ"}), 500

@admin.route('/orders/<order_id>/status', methods=['PUT'])
@admin_required
def update_order_status(order_id):
    """Update order status"""
    try:
        data = request.get_json()
        new_status = data.get('status')
        
        if not new_status:
            return jsonify({"error": "กรุณาระบุสถานะใหม่"}), 400
        
        valid_statuses = ['pending', 'confirmed', 'processing', 'shipped', 'delivered', 'cancelled']
        if new_status not in valid_statuses:
            return jsonify({"error": "สถานะไม่ถูกต้อง"}), 400
        
        order = Order.objects(id=order_id).first()
        
        if not order:
            return jsonify({"error": "ไม่พบคำสั่งซื้อ"}), 404
        
        # Update status and relevant timestamps
        order.order_status = new_status
        order.updated_at = datetime.utcnow()
        
        if new_status == 'confirmed' and not order.confirmed_at:
            order.confirmed_at = datetime.utcnow()
        elif new_status == 'shipped' and not order.shipped_at:
            order.shipped_at = datetime.utcnow()
        elif new_status == 'delivered' and not order.delivered_at:
            order.delivered_at = datetime.utcnow()
        
        order.save()
        
        return jsonify({
            "message": f"อัปเดตสถานะคำสั่งซื้อ {order.order_number} เป็น {new_status} สำเร็จ",
            "order": {
                "id": str(order.id),
                "order_number": order.order_number,
                "order_status": order.order_status
            }
        }), 200
        
    except Exception as e:
        return jsonify({"error": "เกิดข้อผิดพลาดในการอัปเดตสถานะคำสั่งซื้อ"}), 500

@admin.route('/contacts', methods=['GET'])
@admin_required
def get_contacts():
    """Get contact messages with pagination"""
    try:
        page = int(request.args.get('page', 1))
        limit = int(request.args.get('limit', 20))
        unread_only = request.args.get('unread_only', 'false').lower() == 'true'
        
        # Build query
        query = {}
        if unread_only:
            query['is_read'] = False
        
        # Calculate pagination
        offset = (page - 1) * limit
        
        # Get contacts
        contacts_query = Contact.objects(**query).order_by('-created_at')
        total_contacts = contacts_query.count()
        contacts = contacts_query.skip(offset).limit(limit)
        
        contacts_data = []
        for contact in contacts:
            contacts_data.append({
                "id": str(contact.id),
                "name": contact.name,
                "email": contact.email,
                "subject": contact.subject,
                "message": contact.message,
                "phone": contact.phone,
                "is_read": contact.is_read,
                "created_at": contact.created_at.isoformat() if contact.created_at else None
            })
        
        return jsonify({
            "contacts": contacts_data,
            "pagination": {
                "page": page,
                "limit": limit,
                "total": total_contacts,
                "pages": (total_contacts + limit - 1) // limit
            }
        }), 200
        
    except Exception as e:
        return jsonify({"error": "เกิดข้อผิดพลาดในการดึงข้อมูลข้อความติดต่อ"}), 500

@admin.route('/contacts/<contact_id>/mark-read', methods=['PUT'])
@admin_required
def mark_contact_read(contact_id):
    """Mark contact message as read"""
    try:
        contact = Contact.objects(id=contact_id).first()
        
        if not contact:
            return jsonify({"error": "ไม่พบข้อความติดต่อ"}), 404
        
        contact.is_read = True
        contact.save()
        
        return jsonify({
            "message": "ทำเครื่องหมายข้อความเป็นอ่านแล้วสำเร็จ",
            "contact": {
                "id": str(contact.id),
                "is_read": contact.is_read
            }
        }), 200
        
    except Exception as e:
        return jsonify({"error": "เกิดข้อผิดพลาดในการทำเครื่องหมายข้อความ"}), 500
