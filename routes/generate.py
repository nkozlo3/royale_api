from flask import Blueprint, request, jsonify, render_template

generate_bp = Blueprint('generate', __name__)

"""
this route needs an optional text box and button to generate a deck.
you can input card names and it will generate a deck composed of:
    [main-condition,win-condition,damage1,damage2,defense,building,small-spell,spell]
it will include the cards you input
"""
@generate_bp.route('/', methods=['GET'])
def generate():
    return render_template('generate.html')
