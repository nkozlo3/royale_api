import os
import re
import fcntl
import time
import requests
from flask import Blueprint, request, jsonify, render_template
from models import db, Deck, Card
from sqlalchemy.sql.expression import func
from datetime import datetime, timedelta
import math

LOCK_FILE = "/tmp/update_meta_decks.lock"

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
        if done % 10 == 0:
            time.sleep(2)
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
    lock_acquired = False
    try:
        with open(LOCK_FILE, "w") as lock_file:
            fcntl.flock(lock_file, fcntl.LOCK_EX | fcntl.LOCK_NB)
            lock_acquired = True
            return update_decks()
    except BlockingIOError:
        return jsonify({
            "message": "Another process is updating the database. Please wait."
        }), 409
    
    finally:
        if lock_acquired:
            fcntl.flock(lock_file, fcntl.LOCK_UN)

@search_bp.route('/fetch-meta-decks', methods=['GET'])
def generate_and_fetch_meta_deck():
    query = request.args.get('query', '').strip()
    query = re.sub(r"[.\-\s]", "", query).lower()
    query = query.replace("minipekka", "mini")
    query = query.replace("megaminion", "megam")
    query = query.replace("minions", "minids")
    query = query.split(",")
    
    two_months_ago = datetime.utcnow() - timedelta(days=60)

    cards = ["card1", "card2", "card3", "card4", "card5", "card6", "card7", "card8"]

    deck = Deck.query.filter(
        Deck.date_added >= two_months_ago,
        db.and_(*[Deck.cards.ilike(f"%{name}%") for name in query])
    ).order_by(func.random()).first()
    
    update_needed = False
    if not deck:
        deck = Deck.query.filter(Deck.date_added >= two_months_ago).first()
        if deck:
            return jsonify({
                "message": "No meta decks found that contain all your input. Please try again with different cards or make sure you don't have spelling mistakes.",
                "update_needed":"BAD_USER_INPUT"
            }), 200

    if not deck:
        return jsonify({
            "message": "No decks found. Updating database. Please try again in a 10 minutes.",
            "update_needed": "URGENT"
        }), 200
    
    diff = datetime.utcnow() - deck.date_added
    if diff.days >= 60:
        update_needed = True
    
    card_ids = deck.card_ids.split(',')
    card_names = deck.cards.split(',')
    picture_urls = []
    for id in card_ids:
        card = Card.query.get(id)
        picture_urls.append(card.picture_url)

    return jsonify({
        "deck" : {
            card : {
                "picture_url": picture_urls[i],
                "name": card_names[i],
                "id": card_ids[i]
            }
            for i, card in enumerate(cards)
        },
        "update_needed" : update_needed
    })
