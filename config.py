# -*- coding: utf-8 -*-
"""
Application Configuration
-------------------------
"""

class Config:
    # Flask Key
    FLASK_APP = 'wsgi.py'
    SECRET_KEY = '1234567890'

    # CSRF Key
    WTF_CSRF_SECRET_KEY = '0987654321'

    # Paths
    UPLOAD_FOLDER = 'uploads'
    STATIC_FOLDER = 'static'
    TEMPLATES_FOLDER = 'templates'


class DevConfig(Config):
    FLASK_ENV = 'development'
    DEBUG = True
    TESTING = False
