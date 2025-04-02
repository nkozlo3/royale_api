import os
import time
import requests
from flask import Blueprint, request, jsonify, render_template
from models import db, Deck
from datetime import datetime
import math

search_bp = Blueprint('search', __name__)

"""
this route needs a text box and button to submit your search
you can search for a card or cards in a comma seperated list and it will
return a list of decks from top players OR the database, containing those cards.
as you search, it will save decks not yet seen in our database
"""
@search_bp.route('/', methods=['GET'])
def search():
    return render_template('search.html')

def add_deck(deck):
    cards = ""
    card_ids = ""
    for card in deck:
        cards += card['name'] + ","
        card_ids += str(card['id']) + ","
    cards = cards[:len(cards)-1]
    card_ids = card_ids[:len(card_ids)-1]
    currDeck = Deck(cards=cards, card_ids=card_ids)
    db.session.add(currDeck)
    db.session.commit()
    print(f"Deck added: {currDeck.cards}")


def populate_decks(data):
    players = data['items']
    done = 0
    for player in players:
        tag = player['tag']
        tag = tag.replace("#", "%23")
        time.sleep(1)
        api_key = os.environ.get("ROYALE_API_KEY")
        url = f"https://api.clashroyale.com/v1/players/{tag}"
        headers = {"Authorization": f"Bearer {api_key}"}
        
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            data = response.json()
            deck = data['currentDeck']
            
            add_deck(deck)
        except requests.exceptions.RequestException as e:
            print(f"error fetching data for player: {str(e)}")
        done += 1


        

def update_decks():
    api_key = os.environ.get("ROYALE_API_KEY")
    location = 57000249
    url = f"https://api.clashroyale.com/v1/locations/{location}/pathoflegend/players"
    headers = {"Authorization": f"Bearer {api_key}"}
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()

        populate_decks(data)
        return jsonify({"message":"Decks populated succesfully"}), 201
    except requests.exceptions.RequestException as e:
        print("error: ", str(e))
        return jsonify({"error": str(e)}), 500

@search_bp.route('/update-meta-decks', methods=['POST'])
def update_meta_decks():
    return update_decks()

@search_bp.route('/fetch-meta-decks', methods=['GET'])
def generate_and_fetch_meta_deck():
    decks = Deck.query.order_by(Deck.date_added.desc()).limit(5).all()
    
    update_needed = False
    if decks:
        deck = decks[0]
        diff = datetime.utcnow() - deck.date_added
        if diff.days >= 30:
            update_needed = True
    if not decks:
        return jsonify({
            "message": "No decks found. Updating database. Please try again in a few minutes.",
            "update_needed": "URGENT"
        }), 200
    # print("retard")
    # print(decks)
    