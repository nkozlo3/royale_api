from models import db
from flask import Blueprint, render_template

war_decks_bp = Blueprint('war_decks', __name__)

@war_decks_bp.route('/', methods=['GET'])
def war_decks():
    return render_template('war_decks.html')
