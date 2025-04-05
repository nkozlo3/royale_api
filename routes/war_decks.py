from models import db, Card, Deck
import random
from flask import Blueprint, jsonify, render_template

war_decks_bp = Blueprint('war_decks', __name__)

@war_decks_bp.route('/', methods=['GET'])
def war_decks():
    return render_template('war_decks.html')
