from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import Cart, CartItem, Product, User
from mongoengine.errors import DoesNotExist, ValidationError
from bson import ObjectId

cart = Blueprint('cart', __name__)

@cart.route('/cart', methods=['GET'])
@jwt_required()
def get_cart():
    """Get user's cart"""
    try:
        user_id = get_jwt_identity()
        user = User.objects(id=user_id).first()
        if not user:
            return jsonify({'success': False, 'message': 'User not found'}), 404
        
        # Get or create cart
        cart_obj = Cart.objects(user=user).first()
        if not cart_obj:
            cart_obj = Cart(user=user, items=[])
            cart_obj.save()
        
        # Build response data
        cart_data = {
            'items': [],
            'totals': cart_obj.calculate_totals()
        }
        
        for item in cart_obj.items:
            if item.product:  # Make sure product still exists
                cart_data['items'].append({
                    'product': {
                        'id': str(item.product.id),
                        'name': item.product.name,
                        'price': item.product.price,
                        'images': item.product.images,
                        'stock_quantity': item.product.stock_quantity
                    },
                    'quantity': item.quantity,
                    'price_at_add': item.price_at_add,
                    'added_at': item.added_at.isoformat() if item.added_at else None
                })
        
        return jsonify({
            'success': True,
            'cart': cart_data
        })
        
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@cart.route('/cart/add', methods=['POST'])
@jwt_required()
def add_to_cart():
    """Add item to cart"""
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        
        if not data or 'product_id' not in data:
            return jsonify({'success': False, 'message': 'Product ID required'}), 400
        
        user = User.objects(id=user_id).first()
        if not user:
            return jsonify({'success': False, 'message': 'User not found'}), 404
        
        # Get product
        try:
            product = Product.objects(id=data['product_id']).first()
            if not product:
                return jsonify({'success': False, 'message': 'Product not found'}), 404
        except:
            return jsonify({'success': False, 'message': 'Invalid product ID'}), 400
        
        # Check if product is active and in stock
        if not product.is_active:
            return jsonify({'success': False, 'message': 'Product is not available'}), 400
        
        quantity = int(data.get('quantity', 1))
        if quantity <= 0:
            return jsonify({'success': False, 'message': 'Quantity must be positive'}), 400
        
        if quantity > product.stock_quantity:
            return jsonify({'success': False, 'message': f'Only {product.stock_quantity} items available'}), 400
        
        # Get or create cart
        cart_obj = Cart.objects(user=user).first()
        if not cart_obj:
            cart_obj = Cart(user=user, items=[])
        
        # Check if item already exists in cart
        existing_item = None
        for item in cart_obj.items:
            if str(item.product.id) == str(product.id):
                existing_item = item
                break
        
        if existing_item:
            # Update quantity
            new_quantity = existing_item.quantity + quantity
            if new_quantity > product.stock_quantity:
                return jsonify({'success': False, 'message': f'Cannot add more items. Only {product.stock_quantity} available'}), 400
            existing_item.quantity = new_quantity
        else:
            # Add new item
            cart_item = CartItem(
                product=product,
                quantity=quantity,
                price_at_add=product.price
            )
            cart_obj.items.append(cart_item)
        
        cart_obj.save()
        
        return jsonify({
            'success': True,
            'message': 'Item added to cart',
            'cart': {
                'items': len(cart_obj.items),
                'totals': cart_obj.calculate_totals()
            }
        })
        
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@cart.route('/cart/update', methods=['PUT'])
@jwt_required()
def update_cart_item():
    """Update item quantity in cart"""
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        
        if not data or 'product_id' not in data or 'quantity' not in data:
            return jsonify({'success': False, 'message': 'Product ID and quantity required'}), 400
        
        user = User.objects(id=user_id).first()
        if not user:
            return jsonify({'success': False, 'message': 'User not found'}), 404
        
        cart_obj = Cart.objects(user=user).first()
        if not cart_obj:
            return jsonify({'success': False, 'message': 'Cart not found'}), 404
        
        quantity = int(data['quantity'])
        if quantity <= 0:
            return jsonify({'success': False, 'message': 'Quantity must be positive'}), 400
        
        # Find item in cart
        item_found = False
        for item in cart_obj.items:
            if str(item.product.id) == str(data['product_id']):
                # Check stock
                if quantity > item.product.stock_quantity:
                    return jsonify({'success': False, 'message': f'Only {item.product.stock_quantity} items available'}), 400
                
                item.quantity = quantity
                item_found = True
                break
        
        if not item_found:
            return jsonify({'success': False, 'message': 'Item not found in cart'}), 404
        
        cart_obj.save()
        
        return jsonify({
            'success': True,
            'message': 'Cart updated',
            'cart': {
                'items': len(cart_obj.items),
                'totals': cart_obj.calculate_totals()
            }
        })
        
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@cart.route('/cart/remove', methods=['DELETE'])
@jwt_required()
def remove_from_cart():
    """Remove item from cart"""
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        
        if not data or 'product_id' not in data:
            return jsonify({'success': False, 'message': 'Product ID required'}), 400
        
        user = User.objects(id=user_id).first()
        if not user:
            return jsonify({'success': False, 'message': 'User not found'}), 404
        
        cart_obj = Cart.objects(user=user).first()
        if not cart_obj:
            return jsonify({'success': False, 'message': 'Cart not found'}), 404
        
        # Remove item from cart
        original_length = len(cart_obj.items)
        cart_obj.items = [item for item in cart_obj.items if str(item.product.id) != str(data['product_id'])]
        
        if len(cart_obj.items) == original_length:
            return jsonify({'success': False, 'message': 'Item not found in cart'}), 404
        
        cart_obj.save()
        
        return jsonify({
            'success': True,
            'message': 'Item removed from cart',
            'cart': {
                'items': len(cart_obj.items),
                'totals': cart_obj.calculate_totals()
            }
        })
        
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@cart.route('/cart/clear', methods=['POST'])
@jwt_required()
def clear_cart():
    """Clear all items from cart"""
    try:
        user_id = get_jwt_identity()
        user = User.objects(id=user_id).first()
        if not user:
            return jsonify({'success': False, 'message': 'User not found'}), 404
        
        cart_obj = Cart.objects(user=user).first()
        if cart_obj:
            cart_obj.items = []
            cart_obj.save()
        
        return jsonify({
            'success': True,
            'message': 'Cart cleared',
            'cart': {
                'items': 0,
                'totals': {'subtotal': 0, 'total_quantity': 0}
            }
        })
        
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@cart.route('/cart/count', methods=['GET'])
@jwt_required()
def get_cart_count():
    """Get cart item count"""
    try:
        user_id = get_jwt_identity()
        user = User.objects(id=user_id).first()
        if not user:
            return jsonify({'success': False, 'message': 'User not found'}), 404
        
        cart_obj = Cart.objects(user=user).first()
        if not cart_obj:
            count = 0
        else:
            count = sum(item.quantity for item in cart_obj.items)
        
        return jsonify({
            'success': True,
            'count': count
        })
        
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500
