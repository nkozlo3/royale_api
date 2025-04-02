from flask import Blueprint
from .cards import cards_bp
from .search import search_bp
from .generate import generate_bp
from .helpers import helper_bp

def register_routes(app):
    app.register_blueprint(cards_bp, url_prefix='/cards')
    app.register_blueprint(search_bp, url_prefix='/search')
    app.register_blueprint(generate_bp, url_prefix='/generate')
    app.register_blueprint(helper_bp, url_prefix='/helpers')
