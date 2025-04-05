from flask import Blueprint
from .cards import cards_bp
from .search import search_bp
from .helpers import helper_bp
from .war_decks import war_decks_bp

def register_routes(app):
    app.register_blueprint(cards_bp, url_prefix='/cards')
    app.register_blueprint(search_bp, url_prefix='/search')
    app.register_blueprint(war_decks_bp, url_prefix='/war_decks')
    app.register_blueprint(helper_bp, url_prefix='/helpers')
