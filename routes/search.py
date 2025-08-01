import os
import re
# import fcntl
import time
import requests
from flask import Blueprint, request, jsonify, render_template
from models import db, Deck, Card
from sqlalchemy.sql.expression import func, desc
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
    toReplace = ["minipekka", "megaminion", "minions", "giantskeleton", "electrogiant", "giantsnowball", "electrowizard", "icewizard", "royalgiant", "goblingiant", "runegiant", "megaknight", "goldenknight", "bossbandit", "darkprince", "littleprince", "princess"]
    replaceWith = ["mini", "megam", "minids", "giaskele", "elecg", "gisnowball", "electrow", "icewiz", "royg", "gobant", "runeg", "megakn", "goldkn", "bossandit", "dapr", "littlepr", "firepr"]
    
    for toChange, change in zip(toReplace, replaceWith):
        cards = cards.replace(toChange, change)
    
    return cards

def formatNames(cards):
    cards = re.sub(r"[.\-\s]", "", cards).lower()
    cards = make_unique(cards)
    return cards

def add_deck(deck, tower_troop):
    cards = ""
    card_ids = ""
    cards_l = []
    cards_ids_l = []
    if not tower_troop:
        print("Error:  tower_troop is empty. Skipping this deck.")
    
    try:
        tower_troop_id = tower_troop[0]['id']
    except (IndexError, KeyError) as e:
        print(f"Error accessing tower_troop: {e}. Skipping this deck.")
        return
    
    for card in deck:
        cards_l.append(card['name'])
        cards_ids_l.append(str(card['id']))
def add_deck(deck, tower_troop):
    cards = ""
    card_ids = ""
    cards_l = []
    cards_ids_l = []
    if not tower_troop:
        print("Error:  tower_troop is empty. Skipping this deck.")
    
    try:
        tower_troop_id = tower_troop[0]['id']
    except (IndexError, KeyError) as e:
        print(f"Error accessing tower_troop: {e}. Skipping this deck.")
        return
    
    for card in deck:
        cards_l.append(card['name'])
        cards_ids_l.append(str(card['id']))

    if len(cards_l) < 8:
        print(f"Not enough cards in that deck.")
        return
    cards_l = sorted(cards_l)

    cards = ",".join(cards_l)
    cards = formatNames(cards)
    card_ids = ",".join(cards_ids_l)
    
    existing_deck = Deck.query.filter_by(cards=cards).first()
    if existing_deck:
        print(f"Deck Already Exists.")
        existing_deck.alpha = existing_deck.alpha + 1
        return
    
    currDeck = Deck(cards=cards, card_ids=card_ids, tower_troop_id=tower_troop_id, alpha=1)
    db.session.add(currDeck)
    print(f"Deck added: {currDeck.cards}")


def populate_decks(data):
    players = data['items']
    done = 0
    for player in players:
        tag = player['tag']
        tag = tag.replace("#", "%23")
        if done % 40 == 0:
            print("CHECKEd THIS MANY SIGMAS: ", done)
            db.session.commit()
            # time.sleep(3)
        api_key = os.environ.get("ROYALE_API_KEY")
        url = f"https://api.clashroyale.com/v1/players/{tag}"
        headers = {"Authorization": f"Bearer {api_key}"}
        
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            data = response.json()
            deck = data['currentDeck']
            tower_troop = data['currentDeckSupportCards']
            
            add_deck(deck, tower_troop)
        except Exception as e:
            print(f"error fetching data for player: {str(e)}")
        done += 1

    if len(cards_l) < 8:
        print(f"Not enough cards in that deck.")
        return
    
    cards = sorted(cards)
    cards = ",".join(cards_l)
    cards = formatNames(cards)
    card_ids = ",".join(cards_ids_l)
    
    existing_deck = Deck.query.filter_by(cards=cards).first()
    if existing_deck:
        print(f"Deck Already Exists.")
        existing_deck.alpha = existing_deck.alpha + 1
        return
    
    currDeck = Deck(cards=cards, card_ids=card_ids, tower_troop_id=tower_troop_id, alpha=1)
    db.session.add(currDeck)
    print(f"Deck added: {currDeck.cards}")


def populate_decks(data):
    players = data['items']
    done = 0
    for player in players:
        tag = player['tag']
        tag = tag.replace("#", "%23")
        if done % 40 == 0:
            print("CHECKEd THIS MANY SIGMAS: ", done)
            db.session.commit()
            # time.sleep(3)
        api_key = os.environ.get("ROYALE_API_KEY")
        url = f"https://api.clashroyale.com/v1/players/{tag}"
        headers = {"Authorization": f"Bearer {api_key}"}
        
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            data = response.json()
            deck = data['currentDeck']
            tower_troop = data['currentDeckSupportCards']
            
            add_deck(deck, tower_troop)
        except Exception as e:
            print(f"error fetching data for player: {str(e)}")
        done += 1



def update_decks():
    api_key = os.environ.get("ROYALE_API_KEY")
    locations = [57000122, 57000249]
    for location in locations:
        url = f"https://api.clashroyale.com/v1/locations/{location}/pathoflegend/players"
        headers = {"Authorization": f"Bearer {api_key}"}
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            data = response.json()
            populate_decks(data)
        except requests.exceptions.RequestException as e:
            print("error: ", str(e))
            return jsonify({"error": str(e)}), 500
        
    return jsonify({"message":"Decks populated succesfully"}), 201

@search_bp.route('/update-meta-decks', methods=['POST'])
def update_meta_decks():
    try:
        # with open(LOCK_FILE, "w") as lock_file:
            # fcntl.flock(lock_file, fcntl.LOCK_EX | fcntl.LOCK_NB)
            return update_decks()
    except BlockingIOError:
        return jsonify({
            "message": "Another process is updating the database. Please wait."
        }), 409

def get_deck_lists(decks, amount):
    amount = int(amount)
    card_ids_lists = []
    tower_troops_ids_lists = []
    card_names_lists = []
    picture_urls_lists = []
    
    for i in range(amount, -1, -1):
        try:
            deck = decks[i]
        except Exception as e:
            continue
        card_ids = deck.card_ids.split(',')
        card_names = deck.cards.split(',')
        tower_troop_id = deck.tower_troop_id
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
        tower_troops_ids_lists.append(tower_troop_id)
        
    return card_ids_lists, card_names_lists, tower_troops_ids_lists, picture_urls_lists

@search_bp.route('/fetch-meta-decks', methods=['GET'])
def generate_and_fetch_meta_deck():
    query = request.args.get('query', '').strip()
    alphaFilter = query[len(query)-1]
    query = query[:len(query)-2]
    amount = query[len(query)-2:] if query[len(query) - 2].isnumeric() else query[len(query)-1]
    query = query[:len(query)-2] if query[len(query) - 2].isnumeric() else query[:len(query)-1]
    query = formatNames(query)
    query = query.split(",")
    contains = [q for q in query if q and q[0] != '!']
    notContains = [q[1:] for q in query if q and q[0] == '!']
    
    one_months_ago = datetime.utcnow() - timedelta(days=30)
    cards = ["card1", "card2", "card3", "card4", "card5", "card6", "card7", "card8"]
    toCheck = Deck.query.filter(
        Deck.date_added >= one_months_ago,
        db.and_(*[Deck.cards.ilike(f"%{name}%") for name in contains]),
        db.and_(*[~Deck.cards.ilike(f"%{name}%") for name in notContains])
    ).distinct().order_by(func.random()).first()
    decks = "i exist :)"
    if (alphaFilter == '0'):
        decks = Deck.query.filter(
            Deck.date_added >= one_months_ago,
            db.and_(*[Deck.cards.ilike(f"%{name}%") for name in contains]),
            db.and_(*[~Deck.cards.ilike(f"%{name}%") for name in notContains])
        ).distinct().order_by(func.random()).limit(amount)
    else:
        decks = Deck.query.filter(
            Deck.date_added >= one_months_ago,
            db.and_(*[Deck.cards.ilike(f"%{name}%") for name in contains]),
            db.and_(*[~Deck.cards.ilike(f"%{name}%") for name in notContains])
        ).distinct().order_by(desc(Deck.alpha)).limit(amount)

    update_needed = False
    if not toCheck:
        toCheck = Deck.query.filter(Deck.date_added >= one_months_ago).first()
        if toCheck:
            return jsonify({
                "message": "No meta decks found that contain all your input. Please try again with different cards or make sure you don't have spelling mistakes.",
                "update_needed":"BAD_USER_INPUT"
            }), 200

    if not toCheck:
        return jsonify({
            "message": "No decks found. Updating database. Please try again in a 10 minutes.",
            "update_needed": "URGENT"
        }), 200

    diff = datetime.utcnow() - toCheck.date_added
    if diff.days >= 30:
        update_needed = True
    card_ids_lists, card_names_lists, tower_troop_ids_lists, picture_urls_lists = get_deck_lists(decks, amount)
    deck_names = ["deck" + str(i) for i in range(1, len(card_ids_lists) + 1)]

    return jsonify({
            "decks" : {
                deck_name : {
                    card : {
                        "picture_url": picture_urls_lists[j][i],
                        "name": card_names_lists[j][i],
                        "id": card_ids_lists[j][i],
                        "tower_troop": tower_troop_ids_lists[j]
                    }
                    for i, card in enumerate(cards)
                }
                for j, deck_name in enumerate(deck_names)
        },
            "update_needed" : update_needed
    })
