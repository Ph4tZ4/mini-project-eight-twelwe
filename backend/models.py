# models.py
from mongoengine import Document, StringField, DateTimeField, IntField, FloatField, ReferenceField, ListField
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
    password = StringField(required=True, min_length=6)
    profile_picture = StringField(max_length=1000, default=None)
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
    is_active = StringField(default=True)
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
    is_featured = StringField(default=False)
    is_active = StringField(default=True)
    rating = FloatField(min_value=0, max_value=5, default=0)
    review_count = IntField(min_value=0, default=0)
    created_at = DateTimeField(default=datetime.utcnow)
    updated_at = DateTimeField(default=datetime.utcnow)
    
    meta = {
        'collection': 'products',
        'indexes': ['name', 'sku', 'category', 'is_featured', 'is_active']
    }

class Contact(Document):
    name = StringField(required=True, max_length=100)
    email = StringField(required=True, max_length=100)
    subject = StringField(required=True, max_length=200)
    message = StringField(required=True, max_length=2000)
    phone = StringField(max_length=20)
    is_read = StringField(default=False)
    created_at = DateTimeField(default=datetime.utcnow)
    
    meta = {
        'collection': 'contacts',
        'indexes': ['email', 'is_read', 'created_at']
    }