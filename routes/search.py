import os
import re
import fcntl
import time
import requests
from flask import Blueprint, request, jsonify, render_template
from models import db, Deck, Card
from sqlalchemy.sql.expression import func
from datetime import datetime, timedelta

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

def make_unique(cards):
    toReplace = ["minipekka", "megaminion", "minions", "giantskeleton", "electrogiant", "giantsnowball", "electrowizard", "icewizard", "royalgiant", "goblingiant", "runegiant", "megaknight", "goldenknight"]
    replaceWith = ["mini", "megam", "minids", "giaskele", "elecg", "gisnowball", "electrow", "icewiz", "royg", "gobant", "runeg", "megakn", "goldkn"]
    
    for toChange, change in zip(toReplace, replaceWith):
        cards = cards.replace(toChange, change)
    
    return cards

def formatNames(cards):
    cards = re.sub(r"[.\-\s]", "", cards).lower()
    cards = make_unique(cards)
    return cards

def add_deck(deck):
    cards = ""
    card_ids = ""
    cards_l = []
    cards_ids_l = []
    for card in deck:
        cards_l.append(card['name'])
        cards_ids_l.append(str(card['id']))

    cards = sorted(cards)
    cards = ",".join(cards_l)
    cards = formatNames(cards)
    card_ids = ",".join(cards_ids_l)
    
    existing_deck = Deck.query.filter_by(cards=cards).first()
    if existing_deck:
        print(f"Deck Already Exists.")
    
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
    try:
        with open(LOCK_FILE, "w") as lock_file:
            fcntl.flock(lock_file, fcntl.LOCK_EX | fcntl.LOCK_NB)
            return update_decks()
    except BlockingIOError:
        return jsonify({
            "message": "Another process is updating the database. Please wait."
        }), 409

def get_deck_lists(decks):
    card_ids_lists = []
    card_names_lists = []
    picture_urls_lists = []
    
    for deck in decks:
        card_ids = deck.card_ids.split(',')
        card_names = deck.cards.split(',')
        picture_urls = []
        for id in card_ids:
            card = Card.query.get(id)
            picture_urls.append(card.picture_url)
        card1 = Card.query.get(card_ids[0])
        card2 = Card.query.get(card_ids[1])
        picture_urls[0] = card1.evolution_picture_url if card1.has_evolution else picture_urls[0]
        picture_urls[1] = card2.evolution_picture_url if card2.has_evolution else picture_urls[1]

        card_ids_lists.append(card_ids)
        card_names_lists.append(card_names)
        picture_urls_lists.append(picture_urls)
        
    return card_ids_lists, card_names_lists, picture_urls_lists

@search_bp.route('/fetch-meta-decks', methods=['GET'])
def generate_and_fetch_meta_deck():
    query = request.args.get('query', '').strip()
    query = formatNames(query)
    query = query.split(",")
    contains = [q for q in query if q and q[0] != '!']
    notContains = [q[1:] for q in query if q and q[0] == '!']
    
    
    two_months_ago = datetime.utcnow() - timedelta(days=60)
    cards = ["card1", "card2", "card3", "card4", "card5", "card6", "card7", "card8"]

    decks = Deck.query.filter(
        Deck.date_added >= two_months_ago,
        db.and_(*[Deck.cards.ilike(f"%{name}%") for name in contains]),
        db.and_(*[~Deck.cards.ilike(f"%{name}%") for name in notContains])
    ).distinct().order_by(func.random()).limit(8)
    deck = decks[0]
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
    if diff.days >= 30:
        update_needed = True
    card_ids_lists, card_names_lists, picture_urls_lists = get_deck_lists(decks)

    deck_names = ["deck" + str(i) for i in range(1, len(card_ids_lists) + 1)]

    return jsonify({
            "decks" : {
                deck_name : {
                    card : {
                        "picture_url": picture_urls_lists[j][i],
                        "name": card_names_lists[j][i],
                        "id": card_ids_lists[j][i]
                    }
                    for i, card in enumerate(cards)
                }
                for j, deck_name in enumerate(deck_names)
        },
            "update_needed" : update_needed
    })
