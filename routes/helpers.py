import os
import requests
import json
from flask import Blueprint, request, jsonify
from models import db, Deck

helper_bp = Blueprint('helpers', __name__)

@helper_bp.route('/generate-decks-json', methods=['POST'])
def generate_decks_json():
    decks = Deck.query.all()
    decks_list = []
    for deck in decks:
        decks_list.append({
            "id":deck.id,
            "cards": deck.cards,
            "card_ids": deck.card_ids,
            "date_added": deck.date_added.strftime('%Y-%m-%d %H:%M:%S')
        })
        
    output_file = os.path.join(os.getcwd(), 'decks.json')
    
    with open(output_file, 'w') as json_file:
        json.dump(decks_list, json_file, indent=4)
        
    return jsonify({"message": f"Decks saved to {output_file}"})