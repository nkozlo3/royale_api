from flask import Flask, request, jsonify, render_template
from models import Card, db, Deck
from flask_migrate import Migrate
from config import Config
import requests
import os
from dotenv import load_dotenv
from routes import register_routes

load_dotenv()


app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)
migrate = Migrate(app, db)

with app.app_context():
    db.create_all()
    

register_routes(app)

@app.route('/')
def home():
    return render_template('app.html')

if __name__ == '__main__':
    app.run(debug=True)
