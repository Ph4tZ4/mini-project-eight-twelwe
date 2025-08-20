# routes/categories.py
from flask import Blueprint, request, jsonify
from models import Category
from bson import ObjectId

categories = Blueprint('categories', __name__)

@categories.route('/categories', methods=['GET'])
def get_categories():
    """Get all active categories"""
    try:
        categories = Category.objects(is_active=True).order_by('name')
        category_list = []
        
        for category in categories:
            category_list.append({
                'id': str(category.id),
                'name': category.name,
                'description': category.description,
                'image_url': category.image_url,
                'slug': category.slug,
                'is_active': category.is_active,
                'created_at': category.created_at.isoformat() if category.created_at else None,
                'updated_at': category.updated_at.isoformat() if category.updated_at else None
            })
        
        return jsonify({
            'success': True,
            'categories': category_list
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': 'เกิดข้อผิดพลาดในการดึงข้อมูลหมวดหมู่'
        }), 500

@categories.route('/categories/<slug>', methods=['GET'])
def get_category_by_slug(slug):
    """Get category by slug"""
    try:
        category = Category.objects(slug=slug, is_active=True).first()
        
        if not category:
            return jsonify({
                'success': False,
                'error': 'ไม่พบหมวดหมู่นี้'
            }), 404
        
        category_data = {
            'id': str(category.id),
            'name': category.name,
            'description': category.description,
            'image_url': category.image_url,
            'slug': category.slug,
            'is_active': category.is_active,
            'created_at': category.created_at.isoformat() if category.created_at else None,
            'updated_at': category.updated_at.isoformat() if category.updated_at else None
        }
        
        return jsonify({
            'success': True,
            'category': category_data
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': 'เกิดข้อผิดพลาดในการดึงข้อมูลหมวดหมู่'
        }), 500

@categories.route('/categories/<slug>/products', methods=['GET'])
def get_products_by_category(slug):
    """Get products by category slug"""
    try:
        from models import Product
        
        category = Category.objects(slug=slug, is_active=True).first()
        
        if not category:
            return jsonify({
                'success': False,
                'error': 'ไม่พบหมวดหมู่นี้'
            }), 404
        
        # Get products in this category
        products = Product.objects(category=category, is_active=True).order_by('-created_at')
        product_list = []
        
        for product in products:
            product_list.append({
                'id': str(product.id),
                'name': product.name,
                'description': product.description,
                'price': product.price,
                'original_price': product.original_price,
                'images': product.images,
                'stock_quantity': product.stock_quantity,
                'sku': product.sku,
                'brand': product.brand,
                'tags': product.tags,
                'is_featured': product.is_featured,
                'rating': product.rating,
                'review_count': product.review_count,
                'created_at': product.created_at.isoformat() if product.created_at else None
            })
        
        return jsonify({
            'success': True,
            'category': {
                'id': str(category.id),
                'name': category.name,
                'slug': category.slug
            },
            'products': product_list
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': 'เกิดข้อผิดพลาดในการดึงข้อมูลสินค้า'
        }), 500
