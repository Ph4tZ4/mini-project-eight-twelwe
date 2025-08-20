# routes/products.py
from flask import Blueprint, request, jsonify
from models import Product, Category
from mongoengine.errors import DoesNotExist, ValidationError

products = Blueprint('products', __name__)

@products.route('/categories', methods=['GET'])
def get_categories():
    """ดึงข้อมูลหมวดหมู่ทั้งหมด"""
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
                'product_count': Product.objects(category=category, is_active=True).count()
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

@products.route('/categories/<slug>', methods=['GET'])
def get_category_by_slug(slug):
    """ดึงข้อมูลหมวดหมู่ตาม slug"""
    try:
        category = Category.objects(slug=slug, is_active=True).first()
        
        if not category:
            return jsonify({
                'success': False,
                'error': 'ไม่พบหมวดหมู่นี้'
            }), 404
        
        # ดึงสินค้าในหมวดหมู่นี้
        products_in_category = Product.objects(category=category, is_active=True).order_by('-created_at')
        product_list = []
        
        for product in products_in_category:
            product_list.append({
                'id': str(product.id),
                'name': product.name,
                'description': product.description,
                'price': product.price,
                'original_price': product.original_price,
                'images': product.images,
                'stock_quantity': product.stock_quantity,
                'brand': product.brand,
                'rating': product.rating,
                'review_count': product.review_count,
                'is_featured': product.is_featured
            })
        
        return jsonify({
            'success': True,
            'category': {
                'id': str(category.id),
                'name': category.name,
                'description': category.description,
                'image_url': category.image_url,
                'slug': category.slug
            },
            'products': product_list,
            'total_products': len(product_list)
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': 'เกิดข้อผิดพลาดในการดึงข้อมูลหมวดหมู่'
        }), 500

@products.route('/products', methods=['GET'])
def get_products():
    """ดึงข้อมูลสินค้าทั้งหมด"""
    try:
        # Query parameters
        page = int(request.args.get('page', 1))
        limit = int(request.args.get('limit', 12))
        category_id = request.args.get('category')
        search = request.args.get('search')
        sort_by = request.args.get('sort_by', 'created_at')
        sort_order = request.args.get('sort_order', 'desc')
        
        # Build query
        query = Product.objects(is_active=True)
        
        if category_id:
            query = query.filter(category=category_id)
        
        if search:
            query = query.filter(name__icontains=search)
        
        # Sorting
        if sort_order == 'desc':
            query = query.order_by(f'-{sort_by}')
        else:
            query = query.order_by(sort_by)
        
        # Pagination
        total_products = query.count()
        total_pages = (total_products + limit - 1) // limit
        offset = (page - 1) * limit
        
        products_list = query.skip(offset).limit(limit)
        
        # Format response
        products_data = []
        for product in products_list:
            category = product.category
            products_data.append({
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
                'category': {
                    'id': str(category.id),
                    'name': category.name,
                    'slug': category.slug
                } if category else None
            })
        
        return jsonify({
            'success': True,
            'products': products_data,
            'pagination': {
                'page': page,
                'limit': limit,
                'total_products': total_products,
                'total_pages': total_pages
            }
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': 'เกิดข้อผิดพลาดในการดึงข้อมูลสินค้า'
        }), 500

@products.route('/products/<product_id>', methods=['GET'])
def get_product_by_id(product_id):
    """ดึงข้อมูลสินค้าตาม ID"""
    try:
        product = Product.objects(id=product_id, is_active=True).first()
        
        if not product:
            return jsonify({
                'success': False,
                'error': 'ไม่พบสินค้านี้'
            }), 404
        
        category = product.category
        product_data = {
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
            'created_at': product.created_at.isoformat(),
            'category': {
                'id': str(category.id),
                'name': category.name,
                'slug': category.slug
            } if category else None
        }
        
        return jsonify({
            'success': True,
            'product': product_data
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': 'เกิดข้อผิดพลาดในการดึงข้อมูลสินค้า'
        }), 500

@products.route('/products/featured', methods=['GET'])
def get_featured_products():
    """ดึงข้อมูลสินค้าแนะนำ"""
    try:
        featured_products = Product.objects(is_featured=True, is_active=True).limit(8)
        products_data = []
        
        for product in featured_products:
            category = product.category
            products_data.append({
                'id': str(product.id),
                'name': product.name,
                'description': product.description,
                'price': product.price,
                'original_price': product.original_price,
                'images': product.images,
                'stock_quantity': product.stock_quantity,
                'brand': product.brand,
                'rating': product.rating,
                'review_count': product.review_count,
                'category': {
                    'id': str(category.id),
                    'name': category.name,
                    'slug': category.slug
                } if category else None
            })
        
        return jsonify({
            'success': True,
            'products': products_data
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': 'เกิดข้อผิดพลาดในการดึงข้อมูลสินค้าแนะนำ'
        }), 500
