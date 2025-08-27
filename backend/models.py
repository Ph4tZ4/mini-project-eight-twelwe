# models.py
from mongoengine import Document, EmbeddedDocument, StringField, DateTimeField, IntField, FloatField, ReferenceField, ListField, BooleanField, EmbeddedDocumentField
from datetime import datetime
import re
import base64

def generate_profile_picture_url(username):
    """Generate profile picture URL from username initials"""
    if not username:
        return None
    
    # Clean username and split into words
    words = re.findall(r'[A-Z][a-z]*|[a-z]+', username)
    
    if not words:
        # If no words found, use first character
        initials = username[0].upper() if username else 'U'
    else:
        # Get initials from first letters of each word
        initials = ''.join(word[0].upper() for word in words[:2])
    
    # Generate a simple SVG-based profile picture URL
    # This will be a data URL containing an SVG with the initials
    svg_content = f'''<svg width="100" height="100" xmlns="http://www.w3.org/2000/svg">
        <rect width="100" height="100" fill="#000000"/>
        <text x="50" y="65" font-family="Arial, sans-serif" font-size="40" font-weight="bold" text-anchor="middle" fill="white">{initials}</text>
    </svg>'''
    
    # Properly encode the SVG as base64
    svg_bytes = svg_content.encode('utf-8')
    svg_base64 = base64.b64encode(svg_bytes).decode('utf-8')
    
    return f"data:image/svg+xml;base64,{svg_base64}"

class User(Document):
    username = StringField(required=True, unique=True, max_length=50)
    first_name = StringField(max_length=50, default='')
    last_name = StringField(max_length=50, default='')
    password = StringField(required=True, min_length=6)
    profile_picture = StringField(max_length=1000, default=None)
    is_admin = BooleanField(default=False)
    created_at = DateTimeField(default=datetime.utcnow)
    updated_at = DateTimeField(default=datetime.utcnow)
    
    meta = {
        'collection': 'users',
        'indexes': ['username']
    }
    
    def save(self, *args, **kwargs):
        # Always regenerate profile picture to ensure it matches current username
        self.profile_picture = generate_profile_picture_url(self.username)
        super().save(*args, **kwargs)

class Category(Document):
    name = StringField(required=True, max_length=100)
    description = StringField(max_length=500)
    image_url = StringField(max_length=500)
    slug = StringField(required=True, unique=True, max_length=100)
    is_active = BooleanField(default=True)
    created_at = DateTimeField(default=datetime.utcnow)
    updated_at = DateTimeField(default=datetime.utcnow)
    
    meta = {
        'collection': 'categories',
        'indexes': ['name', 'slug']
    }

class Product(Document):
    name = StringField(required=True, max_length=200)
    description = StringField(max_length=2000)
    price = FloatField(required=True, min_value=0)
    original_price = FloatField(min_value=0)
    category = ReferenceField(Category, required=True)
    images = ListField(StringField(max_length=500))
    stock_quantity = IntField(required=True, min_value=0, default=0)
    sku = StringField(required=True, unique=True, max_length=100)
    brand = StringField(max_length=100)
    tags = ListField(StringField(max_length=50))
    is_featured = BooleanField(default=False)
    is_active = BooleanField(default=True)
    rating = FloatField(min_value=0, max_value=5, default=0)
    review_count = IntField(min_value=0, default=0)
    created_at = DateTimeField(default=datetime.utcnow)
    updated_at = DateTimeField(default=datetime.utcnow)
    
    meta = {
        'collection': 'products',
        'indexes': ['name', 'sku', 'category', 'is_featured', 'is_active']
    }

class CartItem(EmbeddedDocument):
    product = ReferenceField(Product, required=True)
    quantity = IntField(required=True, min_value=1, default=1)
    price_at_add = FloatField(required=True, min_value=0)
    added_at = DateTimeField(default=datetime.utcnow)

class Cart(Document):
    user = ReferenceField(User, required=True, unique=True)
    items = ListField(EmbeddedDocumentField(CartItem), default=list)
    updated_at = DateTimeField(default=datetime.utcnow)
    created_at = DateTimeField(default=datetime.utcnow)

    meta = {
        'collection': 'carts',
        'indexes': ['user']
    }

    def calculate_totals(self):
        subtotal = 0.0
        total_quantity = 0
        for item in self.items:
            if item and item.product and item.quantity:
                subtotal += (item.price_at_add or 0) * item.quantity
                total_quantity += item.quantity
        return {
            'subtotal': round(subtotal, 2),
            'total_quantity': total_quantity
        }

class Contact(Document):
    name = StringField(required=True, max_length=100)
    email = StringField(required=True, max_length=100)
    subject = StringField(required=True, max_length=200)
    message = StringField(required=True, max_length=2000)
    phone = StringField(max_length=20)
    is_read = BooleanField(default=False)
    created_at = DateTimeField(default=datetime.utcnow)
    
    meta = {
        'collection': 'contacts',
        'indexes': ['email', 'is_read', 'created_at']
    }

class OrderItem(EmbeddedDocument):
    product = ReferenceField(Product, required=True)
    quantity = IntField(required=True, min_value=1)
    price_at_order = FloatField(required=True, min_value=0)
    total_price = FloatField(required=True, min_value=0)

class ShippingAddress(EmbeddedDocument):
    full_name = StringField(required=True, max_length=100)
    phone = StringField(required=True, max_length=20)
    address_line_1 = StringField(required=True, max_length=200)
    address_line_2 = StringField(max_length=200)
    city = StringField(required=True, max_length=100)
    province = StringField(required=True, max_length=100)
    postal_code = StringField(required=True, max_length=10)
    country = StringField(required=True, max_length=100, default='Thailand')

class Payment(Document):
    payment_method = StringField(required=True, choices=['credit_card', 'bank_transfer', 'cash_on_delivery'], default='cash_on_delivery')
    payment_status = StringField(required=True, choices=['pending', 'paid', 'failed', 'refunded'], default='pending')
    amount = FloatField(required=True, min_value=0)
    transaction_id = StringField(max_length=100)
    payment_date = DateTimeField()
    created_at = DateTimeField(default=datetime.utcnow)
    updated_at = DateTimeField(default=datetime.utcnow)
    
    meta = {
        'collection': 'payments',
        'indexes': ['payment_status', 'created_at']
    }

class Order(Document):
    order_number = StringField(required=True, unique=True, max_length=20)
    user = ReferenceField(User, required=True)
    items = ListField(EmbeddedDocumentField(OrderItem), required=True)
    shipping_address = EmbeddedDocumentField(ShippingAddress, required=True)
    payment = ReferenceField(Payment, required=True)
    
    # Order status
    order_status = StringField(
        required=True, 
        choices=['pending', 'confirmed', 'processing', 'shipped', 'delivered', 'cancelled'], 
        default='pending'
    )
    
    # Pricing
    subtotal = FloatField(required=True, min_value=0)
    shipping_fee = FloatField(required=True, min_value=0, default=0)
    tax = FloatField(required=True, min_value=0, default=0)
    total_amount = FloatField(required=True, min_value=0)
    
    # Timestamps
    created_at = DateTimeField(default=datetime.utcnow)
    updated_at = DateTimeField(default=datetime.utcnow)
    confirmed_at = DateTimeField()
    shipped_at = DateTimeField()
    delivered_at = DateTimeField()
    
    # Notes
    notes = StringField(max_length=500)
    
    meta = {
        'collection': 'orders',
        'indexes': ['order_number', 'user', 'order_status', 'created_at']
    }
    
    def save(self, *args, **kwargs):
        # Generate order number if not exists
        if not self.order_number:
            import random
            import string
            timestamp = datetime.utcnow().strftime('%y%m%d')
            random_part = ''.join(random.choices(string.digits, k=4))
            self.order_number = f'ORD{timestamp}{random_part}'
        
        # Update timestamps
        self.updated_at = datetime.utcnow()
        super().save(*args, **kwargs)

class ShippingTracking(Document):
    order = ReferenceField(Order, required=True, unique=True)
    tracking_number = StringField(required=True, unique=True, max_length=50)
    carrier = StringField(required=True, max_length=100, default='ShopHub Express')
    current_status = StringField(
        required=True,
        choices=['order_placed', 'preparing', 'picked_up', 'in_transit', 'out_for_delivery', 'delivered'],
        default='order_placed'
    )
    estimated_delivery = DateTimeField()
    actual_delivery = DateTimeField()
    created_at = DateTimeField(default=datetime.utcnow)
    updated_at = DateTimeField(default=datetime.utcnow)
    
    meta = {
        'collection': 'shipping_tracking',
        'indexes': ['tracking_number', 'order', 'current_status']
    }
    
    def save(self, *args, **kwargs):
        # Generate tracking number if not exists
        if not self.tracking_number:
            import random
            import string
            random_part = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
            self.tracking_number = f'TH{random_part}'
        
        self.updated_at = datetime.utcnow()
        super().save(*args, **kwargs)

class ShippingStatus(EmbeddedDocument):
    status = StringField(required=True)
    description = StringField(required=True)
    location = StringField(max_length=200)
    timestamp = DateTimeField(required=True, default=datetime.utcnow)

class ShippingHistory(Document):
    tracking = ReferenceField(ShippingTracking, required=True)
    status_history = ListField(EmbeddedDocumentField(ShippingStatus), default=list)
    created_at = DateTimeField(default=datetime.utcnow)
    updated_at = DateTimeField(default=datetime.utcnow)
    
    meta = {
        'collection': 'shipping_history',
        'indexes': ['tracking']
    }