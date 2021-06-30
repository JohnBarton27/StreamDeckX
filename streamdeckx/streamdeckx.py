from flask import Flask, render_template
from deck import Deck
import os

app = Flask(__name__, template_folder=os.path.abspath('static'))


@app.route('/')
def hello():
    decks = Deck.get_connected()
    curr_deck = decks[0]  # TODO handle selection of a different deck

    return render_template('index.html', connected_decks=decks, curr_deck_html=curr_deck.html)


if __name__ == '__main__':
    app.run(port=5050)
