import os
import re
import requests
from flask import Blueprint, request, jsonify
from models import db, Card

cards_bp = Blueprint('cards', __name__)

def make_unique(cards):
    toReplace = ["minipekka", "megaminion", "minions", "giantskeleton", "electrogiant", "giantsnowball", "electrowizard", "icewizard", "royalgiant", "goblingiant", "runegiant", "megaknight", "goldenknight", "bossbandit"]
    replaceWith = ["mini", "megam", "minids", "giaskele", "elecg", "gisnowball", "electrow", "icewiz", "royg", "gobant", "runeg", "megakn", "goldkn", "bossandit"]
    
    for toChange, change in zip(toReplace, replaceWith):
        cards = cards.replace(toChange, change)
    
    return cards

def formatNames(cards):
    cards = re.sub(r"[.\-\s]", "", cards).lower()
    cards = make_unique(cards)
    return cards

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
        filteredName = formatNames(card['name'])
        print(filteredName)
        exists = Card.query.filter_by(name=filteredName).first()
        if exists:
            print("This card is already in your database")
            continue
        curr = Card(id=card['id'],name=filteredName,rarity=card['rarity'],elixir=elixirCost,picture_url=picUrl)
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

@cards_bp.route('/update', methods=['PUT'])
def update():
    api_key = os.environ.get("ROYALE_API_KEY")
    url = "https://api.clashroyale.com/v1/cards"
    headers = {"Authorization": f"Bearer {api_key}"}
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()
        cards = data['items']
        for card in cards:
            curr_id = card['id']
            hasEvolution = 0
            try:
                hasEvolution = card['maxEvolutionLevel']
            except KeyError:
                hasEvolution = 0
                
            if hasEvolution:
                db_card = Card.query.get(curr_id)
                db_card.has_evolution = True
                icons = card['iconUrls']
                db_card.evolution_picture_url = icons['evolutionMedium']
                db.session.commit()
        return jsonify({"message": "Cards updated successfully"}), 200
    
    except requests.exceptions.RequestException as e:
        return jsonify({"error": str(e)}), 500
