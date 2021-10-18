import logging
import os
import sqlite3 as sl
from urllib.request import pathname2url

from flask import Flask, render_template, request


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


@app.route('/setButtonConfig', methods=['POST'])
def set_button_text():
    from deck import Deck

    deck_id = request.form['deckId']
    button_position = int(request.form['button'])
    button_text = request.form['buttonText']

    logging.info(f'Setting {button_position} on {deck_id} to {button_text}')

    decks = Deck.get_connected()

    for deck in decks:
        if deck.id == deck_id:
            # This is the deck we selected
            button = deck.buttons[button_position]
            button.set_text(button_text)

            return button.image_bytes.decode("utf-8")

    return 'Failed to find deck!'


@app.route('/setButtonAction', methods=['POST'])
def set_button_action():
    from action import TextAction
    from deck import Deck

    from dao.action_dao import ActionDao

    deck_id = request.form['deckId']
    button_position = int(request.form['button'])
    action = request.form['action_text']

    decks = Deck.get_connected()

    for deck in decks:
        if deck.id == deck_id:
            # This is the deck we selected
            button = deck.buttons[button_position]
            action = TextAction(action, button, 0)

            action_dao = ActionDao()
            action_dao.create(action)

            return 'Success!'

    return 'Failed to find deck!'


def connect_to_database():
    db_name = 'sdx_db.db'
    try:
        dburi = 'file:{}?mode=rw'.format(pathname2url(db_name))
        conn = sl.connect(dburi, uri=True)
        logging.info('Found existing database.')
    except sl.OperationalError:
        # handle missing database case
        logging.warning('Could not find database - will initialize an empty one!')
        conn = sl.connect(db_name)

        # DECK
        with conn:
            conn.execute("""
                CREATE TABLE deck (
                    id TEXT NOT NULL PRIMARY KEY,
                    name TEXT,
                    type TEXT
                );                
            """)

        # BUTTON
        with conn:
            conn.execute("""
                CREATE TABLE button (
                    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                    deck_id TEXT NOT NULL REFERENCES deck(id) ON DELETE CASCADE,
                    position INTEGER NOT NULL,
                    icon TEXT,
                    font TEXT,
                    label TEXT
                );
            """)

        # ACTION
        with conn:
            conn.execute("""
                CREATE TABLE action (
                    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                    type TEXT NOT NULL,
                    button_id INTEGER NOT NULL REFERENCES button(id) ON DELETE CASCADE,
                    action_order INTEGER NOT NULL,
                    parameter TEXT 
                );
            """)


if __name__ == '__main__':
    # Setup Logging
    logging.basicConfig(format='%(levelname)s [%(asctime)s]: %(message)s', level=logging.INFO)
    logging.info('Starting StreamDeckX...')

    # Connect to database
    logging.info(os.getcwd())
    logging.info('About to connect to database...')
    connect_to_database()
    logging.info('Successfully connected to database.')

    import threading

    threading.Thread(target=lambda: app.run(port=5050, debug=False, use_reloader=False), name='FlaskThread').start()

    from deck import Deck

    decks = Deck.get_connected(update_images=True)

    for deck in decks:
        deck.open()
        deck.set_callbacks()
