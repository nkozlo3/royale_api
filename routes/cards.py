import os
import requests
from flask import Blueprint, request, jsonify
from models import db, Card

cards_bp = Blueprint('cards', __name__)

"""
This populates our cards
"""
def populate_cards(data):
    cards = data['items']
    for card in cards:
        elixirCost = -1
        if card['name'] != "Mirror":
            elixirCost=card['elixirCost']

        icons = card['iconUrls']
        picUrl = icons['medium']
        print(card['name'])
        classifications = input("Please input the classifications for this card, CSV, from (damage, main-condition, win-condition, small-spell, spell, building, spawner, defense): ")
        curr = Card(id=card['id'],name=card['name'],rarity=card['rarity'],elixir=elixirCost,classification=classifications,picture_url=picUrl)
        db.session.add(curr)
        db.session.commit()
        
    return "cards added"
        

"""
This route displays our list of cards by name
"""
@cards_bp.route('/', methods=['GET'])
def get_cards():
    cards = Card.query.all()
    cards_list = [
        {
            "id": card.id,
            "name": card.name,
            "rarity": card.rarity,
            "elixir": card.elixir,
            "classification": card.classification,
            "picture_url": card.picture_url,
        }
        for card in cards
    ]
    return jsonify(cards_list), 200

@cards_bp.route('/populate', methods=['POST'])
def fetch_and_populate_cards():
    api_key = os.environ.get("ROYALE_API_KEY")
    url = "https://api.clashroyale.com/v1/cards"
    headers = {"Authorization": f"Bearer {api_key}"}
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()

        populate_cards(data)
        
        return jsonify({"message": "Cards populated successfully"}), 201
    except requests.exceptions.RequestException as e:
        return jsonify({"error": str(e)}), 500
