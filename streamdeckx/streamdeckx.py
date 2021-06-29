from flask import Flask
from deck import Deck

app = Flask(__name__)


@app.route('/')
def hello():
    decks = Deck.get_connected()
    html = ''

    for deck in decks:
        html += f'<p>{deck.__class__.generic_name}</p>'

    return html


if __name__ == '__main__':
    app.run(port=5050)
