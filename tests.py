import unittest
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from models import db, Deck, Card
from config import Config


class TestDeckModel(unittest.TestCase):
    def setUp(self):
        # Set up a Flask app and configure an in-memory SQLite database
        self.app = Flask(__name__)
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        db.init_app(self.app)

        # Create the database and tables
        with self.app.app_context():
            db.create_all()

    def tearDown(self):
        # Drop the database tables after each test
        with self.app.app_context():
            db.session.remove()
            db.drop_all()
            
    def test_add_card(self):
        with self.app.app_context():
            card = Card(id=1, name="fireball", rarity="rare", elixir="4", classification="medium-spell")
            db.session.add(card)
            db.session.commit()
            
            added_card = Card.query.filter_by(id=1).first()
            
            self.assertIsNotNone(added_card)
            self.assertEqual(added_card.name, "fireball")
            self.assertEqual(added_card.rarity, "rare")
            self.assertEqual(added_card.elixir, 4)
            self.assertEqual(added_card.classification, "medium-spell")
            


if __name__ == '__main__':
    unittest.main()