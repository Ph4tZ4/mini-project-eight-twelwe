# routes/home.py
from flask import Blueprint, request, jsonify
from models import Product, Category

home = Blueprint('home', __name__)

@home.route('/home', methods=['GET'])
def get_home_data():
    """Get home page data including featured products and categories"""
    try:
        # Get featured products
        featured_products = Product.objects(is_featured=True, is_active=True).limit(8)
        featured_list = []
        
        for product in featured_products:
            featured_list.append({
                'id': str(product.id),
                'name': product.name,
                'description': product.description,
                'price': product.price,
                'original_price': product.original_price,
                'images': product.images,
                'rating': product.rating,
                'review_count': product.review_count,
                'category': {
                    'id': str(product.category.id),
                    'name': product.category.name,
                    'slug': product.category.slug
                } if product.category else None
            })
        
        # Get main categories
        main_categories = Category.objects(is_active=True).limit(6)
        categories_list = []
        
        for category in main_categories:
            categories_list.append({
                'id': str(category.id),
                'name': category.name,
                'description': category.description,
                'image_url': category.image_url,
                'slug': category.slug
            })
        
        # Get latest products
        latest_products = Product.objects(is_active=True).order_by('-created_at').limit(6)
        latest_list = []
        
        for product in latest_products:
            latest_list.append({
                'id': str(product.id),
                'name': product.name,
                'description': product.description,
                'price': product.price,
                'original_price': product.original_price,
                'images': product.images,
                'rating': product.rating,
                'review_count': product.review_count,
                'category': {
                    'id': str(product.category.id),
                    'name': product.category.name,
                    'slug': product.category.slug
                } if product.category else None
            })
        
        return jsonify({
            'success': True,
            'featured_products': featured_list,
            'main_categories': categories_list,
            'latest_products': latest_list
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': 'เกิดข้อผิดพลาดในการดึงข้อมูลหน้าแรก'
        }), 500

@home.route('/home/stats', methods=['GET'])
def get_home_stats():
    """Get home page statistics"""
    try:
        # Count total products
        total_products = Product.objects(is_active=True).count()
        
        # Count total categories
        total_categories = Category.objects(is_active=True).count()
        
        # Count featured products
        featured_count = Product.objects(is_featured=True, is_active=True).count()
        
        return jsonify({
            'success': True,
            'stats': {
                'total_products': total_products,
                'total_categories': total_categories,
                'featured_products': featured_count
            }
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': 'เกิดข้อผิดพลาดในการดึงข้อมูลสถิติ'
        }), 500
