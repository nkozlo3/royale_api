from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Card(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)
    rarity = db.Column(db.String(100))
    elixir = db.Column(db.Integer)
    classification = db.Column(db.String(100)) # comma seperated types (damage, tank, win-condition, small spell, medium spell, large spell, building-defensive, spawner)
    has_evolution = db.Column(db.Boolean, default=False)
    evolution_picture_url = db.Column(db.String(255))
    picture_url = db.Column(db.String(255))

class Deck(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cards = db.Column(db.String(255)) # comma seperated names of cards
    card_ids = db.Column(db.String(100)) # comma seperated card ids
    date_added = db.Column(db.DateTime, default=datetime.utcnow)
