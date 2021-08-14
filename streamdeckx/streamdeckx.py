from flask import Flask, render_template, request
import logging
import os


class StreamDeckX(Flask):
    def run(self, host=None, port=None, debug=None, load_dotenv=True, **options):
        if not self.debug or os.getenv('WERKZEUG_RUN_MAIN') == 'true':
            with self.app_context():
                sdx_startup()
        super(StreamDeckX, self).run(host=host, port=port, debug=debug, load_dotenv=load_dotenv, **options)


app = StreamDeckX(__name__, template_folder=os.path.abspath('static'))


def sdx_startup():
    pass


@app.route('/')
def hello():
    from deck import Deck
    decks = Deck.get_connected()
    curr_deck = decks[0]

    return render_template('index.html', connected_decks=decks, curr_deck_html=curr_deck.html)


@app.route('/deckHtml')
def get_deck_html():
    from deck import Deck
    decks = Deck.get_connected()
    deck_id = request.args.get('deckId')
    for deck in decks:
        if deck.id == deck_id:
            # This is the deck we selected
            return deck.html

    # TODO add error
    return 'Deck not found!'


@app.route('/configHtml')
def get_config_html():
    from deck import Deck
    deck_id = request.args.get('deckId')
    button_position = int(request.args.get('button'))

    decks = Deck.get_connected()

    for deck in decks:
        if deck.id == deck_id:
            # This is the deck we selected
            button = deck.buttons[button_position]

            return render_template('configuration.html', button=button.position)

    # TODO add error
    return 'Deck not found!'


@app.route('/setButtonText')
def set_button_text():
    deck_id = request.args.get('deckId')
    button_num = request.args.get('button')


if __name__ == '__main__':
    # Setup Logging
    logging.basicConfig(format='%(levelname)s [%(asctime)s]: %(message)s', level=logging.INFO)
    logging.info('Starting StreamDeckX...')

    app.run(port=5050)
