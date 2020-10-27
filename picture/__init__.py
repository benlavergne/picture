# -*- coding: utf-8 -*-
"""
Application Factory
-------------------
"""

import config
from flask import Flask, request, current_app
from flask_wtf.csrf import CSRFProtect

# Globally accessible libraries
csrf = CSRFProtect()


def create_app(config_class='config.DevConfig'):
    # Construct the core app object
    app = Flask(__name__, instance_relative_config=False)

    # Application Configuration
    app.config.from_object(config_class)

    # Initialize Plugins
    csrf.init_app(app)

    with app.app_context():
        # Include Packages
        from . import pic
        from . import site

        # Register Blueprints
        app.register_blueprint(pic.bp)
        app.register_blueprint(site.bp)
        app.add_url_rule('/', endpoint='index')

        return app
