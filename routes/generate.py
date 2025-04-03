from models import Card
import random
from flask import Blueprint, request, jsonify, render_template

generate_bp = Blueprint('generate', __name__)

"""
this route needs an optional text box and button to generate a deck.
you can input card names and it will generate a deck composed of:
    [main-condition,win-condition,damage1,damage2,defense,building,small-spell,spell]
it will include the cards you input
"""
@generate_bp.route('/', methods=['GET'])
def generate():
    return render_template('generate.html')

@generate_bp.route('/generate-deck', methods=['GET'])
def generate_deck():
    composition = ["main-condition", "win-condition", "damage1", "damage2", "defense1", "defense2", "spell", "small-spell"]
    cards = Card.query.all()
    deck = {}
    ids = set()
    
    for cond in composition:
        base_cond = cond.rstrip("12")
        filtered = [card for card in cards if base_cond in card.classification.split(",")]
        
        curr = random.choice(filtered)
        while curr.id in ids:
            curr = random.choice(filtered)
            
        deck[cond.replace('-','_')] = curr
        ids.add(curr.id)
        
    return jsonify({
        "deck" : {
            cond : {
                "picture_url": deck[cond].picture_url,
                "name": deck[cond].name,
                "id": deck[cond].id
            }
            for cond in deck
        }
    })