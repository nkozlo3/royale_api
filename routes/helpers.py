import os
import requests
import json
from flask import Blueprint, request, jsonify
from models import db, Deck, Card

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

@helper_bp.route('/generate-cards-json', methods=['POST'])
def generate_cards_json():
    cards = Card.query.all()
    cards_list = []
    for card in cards:
        cards_list.append({
            "id": card.id,
            "name": card.name,
            "rarity": card.rarity,
            "elixir": card.elixir,
            "classification": card.classification,
            "has_evolution": card.has_evolution,
            "evolution_picture_url":card.evolution_picture_url,
            "picture_url": card.picture_url 
        })
        
    output_file = os.path.join(os.getcwd(), 'cards.json')
    
    with open(output_file, 'w') as json_file:
        json.dump(cards_list, json_file, indent=4)
        
    return jsonify({"message": f"Cards saved to {output_file}"})