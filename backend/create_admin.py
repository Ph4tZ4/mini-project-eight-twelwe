#!/usr/bin/env python3
"""
Script to create an admin user for the system
"""

from mongoengine import connect
from models import User
from werkzeug.security import generate_password_hash
from config import Config
import sys

def create_admin_user():
    # Connect to MongoDB
    try:
        connect(
            db=Config.MONGODB_SETTINGS["db"],
            host=Config.MONGODB_SETTINGS["host"],
            port=Config.MONGODB_SETTINGS["port"]
        )
        print("Connected to MongoDB successfully")
    except Exception as e:
        print(f"Failed to connect to MongoDB: {e}")
        return False

    # Admin credentials
    admin_username = "admin"
    admin_password = "admin123"
    
    try:
        # Check if admin user already exists
        existing_admin = User.objects(username=admin_username).first()
        
        if existing_admin:
            # Update existing user to be admin
            existing_admin.is_admin = True
            existing_admin.save()
            print(f"Updated existing user '{admin_username}' to admin status")
        else:
            # Create new admin user
            admin_user = User(
                username=admin_username,
                first_name="System",
                last_name="Administrator",
                password=generate_password_hash(admin_password),
                is_admin=True
            )
            admin_user.save()
            print(f"Created new admin user: {admin_username}")
        
        print(f"Admin credentials:")
        print(f"Username: {admin_username}")
        print(f"Password: {admin_password}")
        print("\nAdmin user setup completed successfully!")
        return True
        
    except Exception as e:
        print(f"Error creating admin user: {e}")
        return False

if __name__ == "__main__":
    success = create_admin_user()
    sys.exit(0 if success else 1)
