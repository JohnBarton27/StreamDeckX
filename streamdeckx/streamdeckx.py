from flask import Flask, render_template
from deck import Deck
import os

app = Flask(__name__, template_folder=os.path.abspath('static'))


@app.route('/')
def hello():
    decks = Deck.get_connected()

    return render_template('index.html', connected_decks=decks)


if __name__ == '__main__':
    app.run(port=5050)
