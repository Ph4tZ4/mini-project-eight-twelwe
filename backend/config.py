# config.py
import os
from datetime import timedelta

class Config:
    # Flask Configuration
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your-super-secret-key-here'
    
    # JWT Configuration
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY') or 'your-super-secret-jwt-key-here'
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)
    
    # MongoDB Configuration
    MONGODB_SETTINGS = {
        'db': os.environ.get('MONGODB_DB') or 'eight-twelwe',
        'host': os.environ.get('MONGODB_HOST') or 'localhost',
        'port': int(os.environ.get('MONGODB_PORT') or 27017)
    }
    
    # CORS Configuration
    CORS_ORIGINS = [
    "https://eight-twelwe.loeitech.org",
    "https://api-eight-twelwe.loeitech.org",
    "http://localhost:3000"  # ถ้า dev frontend
    ]

    
    # Security Configuration
    SESSION_COOKIE_SECURE = False  # Set to True in production with HTTPS
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'