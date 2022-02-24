from flask import Flask
from flask_cors import CORS
from .api.extensions import jwt


def create_app(debug=False):
    """Create an application."""
    app = Flask(__name__)
    
    cors = CORS(app, resources={r"/*": {"origins": "*"}})
    app.config['CORS_HEADERS'] = 'Content-Type'
        
    app.config['JWT_SECRET_KEY'] = 'gjr39dkjn344_!67#'
    
    app.debug = debug
    app.config['SECRET_KEY'] = 'gjr39dkjn344_!67#'  
    
    jwt.init_app(app)
    
    from .api.auth import authAPI
    app.register_blueprint(authAPI)

    from .api.services import securityguideAPI
    app.register_blueprint(securityguideAPI)

    return app
