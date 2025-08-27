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
        "http://localhost:3330",  # Nuxt.js development & Docker frontend
        "http://127.0.0.1:3330",
        "http://localhost:3000",  # Production frontend
        "http://127.0.0.1:3000",
        "http://localhost:8080",  # Additional fallback
        "http://127.0.0.1:8080"
    ]
    
    # Security Configuration
    SESSION_COOKIE_SECURE = False  # Set to True in production with HTTPS
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'