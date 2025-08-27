# Admin System Guide

## Overview

This document describes the admin system that has been added to the ShopHub e-commerce platform. The admin system provides administrative functionality for managing users, orders, products, and contact messages.

## Features

### ✅ Completed Features
- **Admin Authentication**: Secure login system for administrators
- **Admin Dashboard**: Comprehensive dashboard with system statistics
- **User Management**: View and manage user accounts with admin privilege controls
- **Role-based Access Control**: Admin middleware to protect admin-only routes
- **Admin Navigation**: Dedicated admin interface with navigation between admin pages
- **System Statistics**: Real-time dashboard showing:
  - User statistics (total, new today, new this month)
  - Product statistics (total, active, featured, out of stock)
  - Order statistics (total, by status, today, this month)
  - Revenue statistics (total, today, this month)
  - Contact message statistics
  - Active shopping carts

### 🚧 In Development
- **Order Management**: Full order management interface (placeholder created)
- **Product Management**: Complete CRUD operations for products (placeholder created)
- **Contact Management**: Interface for viewing and responding to contact messages (placeholder created)

## System Architecture

### Backend Components

#### Models (`backend/models.py`)
- **Enhanced User Model**: Added `is_admin` field to distinguish admin users from regular users

#### Admin Routes (`backend/routes/admin.py`)
- **Admin Authentication**:
  - `POST /api/admin/login` - Admin-specific login endpoint
- **Dashboard Data**:
  - `GET /api/admin/dashboard/stats` - Comprehensive system statistics
- **User Management**:
  - `GET /api/admin/users` - List all users with pagination and search
  - `PUT /api/admin/users/{user_id}/toggle-admin` - Toggle admin status for users
- **Order Management**:
  - `GET /api/admin/orders` - List orders with filtering and pagination
  - `PUT /api/admin/orders/{order_id}/status` - Update order status
- **Contact Management**:
  - `GET /api/admin/contacts` - List contact messages
  - `PUT /api/admin/contacts/{contact_id}/mark-read` - Mark messages as read

#### Middleware
- **`@admin_required` decorator**: Ensures only admin users can access protected routes

### Frontend Components

#### Pages
- **`/admin/login`**: Admin login page with separate authentication
- **`/admin/dashboard`**: Main admin dashboard with statistics and navigation
- **`/admin/users`**: Complete user management interface
- **`/admin/orders`**: Order management (placeholder)
- **`/admin/products`**: Product management (placeholder)
- **`/admin/contacts`**: Contact message management (placeholder)

#### Middleware
- **`admin-auth.js`**: Protects admin routes, ensures user is logged in and has admin privileges
- **`guest.js`**: Handles redirects for already authenticated users

#### Components
- **Enhanced ProfileDropdown**: Added admin dashboard link for admin users

## Getting Started

### 1. Create Admin User

Run the admin creation script to create the initial admin user:

```bash
cd backend
source venv/bin/activate
python create_admin.py
```

**Default Admin Credentials:**
- Username: `admin`
- Password: `admin123`

⚠️ **Important**: Change these credentials after first login for security.

### 2. Start the Servers

**Backend:**
```bash
cd backend
source venv/bin/activate
python app.py
```

**Frontend:**
```bash
cd frontend
npm run dev
```

### 3. Access Admin System

1. **Regular User Login**: Go to `/login` for normal user authentication
2. **Admin Login**: Go to `/admin/login` for administrator authentication
3. **Admin Dashboard**: After admin login, access `/admin/dashboard`

## Navigation Flow

### For Regular Users
1. Login at `/login`
2. If user has admin privileges, they see "ระบบผู้ดูแล" (Admin System) in profile dropdown
3. Clicking admin link redirects to `/admin/dashboard`

### For Admins
1. Direct login at `/admin/login`
2. Access to full admin dashboard and management pages
3. Can switch between admin system and regular user interface

## API Endpoints

### Authentication
```
POST /api/admin/login
```

### Dashboard
```
GET /api/admin/dashboard/stats
```

### User Management
```
GET /api/admin/users?page=1&limit=20&search=username
PUT /api/admin/users/{user_id}/toggle-admin
```

### Order Management
```
GET /api/admin/orders?page=1&limit=20&status=pending
PUT /api/admin/orders/{order_id}/status
```

### Contact Management
```
GET /api/admin/contacts?page=1&limit=20&unread_only=true
PUT /api/admin/contacts/{contact_id}/mark-read
```

## Security Features

### Authentication & Authorization
- **JWT-based authentication**: Secure token-based authentication
- **Role-based access control**: Admin middleware checks user privileges
- **Separate admin login**: Isolated authentication flow for administrators
- **Protected routes**: All admin routes require valid admin authentication

### Data Protection
- **Input validation**: All admin endpoints validate input data
- **Error handling**: Proper error messages without exposing system details
- **CORS configuration**: Secure cross-origin resource sharing settings

## Dashboard Statistics

The admin dashboard provides real-time statistics including:

### User Metrics
- Total registered users
- New users today
- New users this month

### Product Metrics
- Total products in catalog
- Active products
- Featured products
- Out-of-stock items

### Order Metrics
- Total orders
- Orders by status (pending, confirmed, shipped, delivered)
- Orders today
- Orders this month

### Revenue Metrics
- Total revenue from delivered orders
- Revenue today
- Revenue this month

### System Metrics
- Total contact messages
- Unread contact messages
- Active shopping carts

## Future Enhancements

### Planned Features
1. **Complete Order Management**:
   - View order details
   - Update shipping information
   - Print invoices
   - Bulk status updates

2. **Advanced Product Management**:
   - Add/edit/delete products
   - Manage categories
   - Inventory management
   - Product image uploads

3. **Enhanced Contact System**:
   - Reply to customer messages
   - Message status tracking
   - Auto-responses

4. **Analytics & Reporting**:
   - Sales reports
   - User growth analytics
   - Product performance metrics
   - Export capabilities

5. **Admin User Management**:
   - Create multiple admin users
   - Admin role permissions
   - Activity logging

## Troubleshooting

### Common Issues

1. **Admin login not working**:
   - Ensure admin user exists (run `create_admin.py`)
   - Check if user has `is_admin=True` in database
   - Verify backend server is running

2. **Dashboard stats not loading**:
   - Check MongoDB connection
   - Verify admin authentication token
   - Check browser console for API errors

3. **Navigation issues**:
   - Clear browser cookies/localStorage
   - Ensure middleware is properly configured
   - Check route definitions

### Support

For technical issues or feature requests, refer to the main project documentation or contact the development team.
