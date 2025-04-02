from flask import Blueprint, request, jsonify, render_template

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
