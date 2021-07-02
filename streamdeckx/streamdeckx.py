from flask import Flask, render_template, request
from deck import Deck
import os

app = Flask(__name__, template_folder=os.path.abspath('static'))


@app.route('/')
def hello():
    decks = Deck.get_connected(add_testing=True)
    curr_deck = decks[0]

    return render_template('index.html', connected_decks=decks, curr_deck_html=curr_deck.html)


@app.route('/deckHtml')
def get_deck_html():
    decks = Deck.get_connected(add_testing=True)
    deck_id = request.args.get('deckId')
    for deck in decks:
        if deck.id == deck_id:
            # This is the deck we selected
            return deck.html

    # TODO add error
    return 'Deck not found!'


if __name__ == '__main__':
    app.run(port=5050)
