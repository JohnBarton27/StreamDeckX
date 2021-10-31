import logging
import os
import sqlite3 as sl
from urllib.request import pathname2url

from flask import Flask, render_template, request


class StreamDeckX(Flask):
    def run(self, host=None, port=None, debug=None, load_dotenv=True, **options):
        super(StreamDeckX, self).run(host=host, port=port, debug=debug, load_dotenv=load_dotenv, **options)


app = StreamDeckX(__name__, template_folder=os.path.abspath('static'))


def _get_connected_decks():
    from deck import Deck
    return Deck.get_connected()


def _get_deck_by_id(deck_id, raise_exception=True):
    decks = _get_connected_decks()
    for deck in decks:
        if deck.id == deck_id:
            # This is the deck we selected
            return deck

    if raise_exception:
        from deck import NoSuchDeckException
        raise NoSuchDeckException(f'Could not find deck with {deck_id=}')
    else:
        logging.warning(f'Could not find deck with {deck_id=}')


@app.route('/')
def index():
    decks = _get_connected_decks()
    if decks:
        curr_deck = decks[0]
        return render_template('index.html', connected_decks=decks, curr_deck_html=curr_deck.html)

    # No decks found
    return render_template('index.html', connected_decks=[], curr_deck_html='<p>No Stream Decks connected!</p>')


@app.route('/deckHtml')
def get_deck_html():
    deck_id = request.args.get('deckId')
    deck = _get_deck_by_id(deck_id)

    if not deck:
        # TODO add error
        return 'Deck not found!'

    return deck.html


@app.route('/configHtml')
def get_config_html():
    deck_id = request.args.get('deckId')
    button_position = int(request.args.get('button'))

    deck = _get_deck_by_id(deck_id)

    button = deck.buttons[button_position]

    return render_template('configuration.html', button=button)


@app.route('/setButtonConfig', methods=['POST'])
def set_button_config():
    # TODO add error handling for missing form parameters
    deck_id = request.form['deckId']
    button_position = int(request.form['button'])
    button_text = request.form['buttonText']

    logging.info(f'Setting {button_position} on {deck_id} to {button_text}')

    deck = _get_deck_by_id(deck_id)

    button = deck.buttons[button_position]
    button.set_text(button_text)

    return button.image_bytes.decode("utf-8")


@app.route('/setButtonAction', methods=['POST'])
def set_button_action():
    from action import TextAction

    from dao.action_dao import ActionDao

    deck_id = request.form['deckId']
    button_position = int(request.form['button'])
    action = request.form['action_text']

    deck = _get_deck_by_id(deck_id)

    button = deck.buttons[button_position]
    action = TextAction(action, button, 0)

    action_dao = ActionDao()
    action_dao.create(action)
    button.actions.append(action)

    return 'Success!'


@app.route('/setButtonAction', methods=['DELETE'])
def delete_button_action():
    from dao.action_dao import ActionDao

    deck_id = request.form['deckId']
    button_position = int(request.form['button'])
    action_id = int(request.form['action'])

    action_dao = ActionDao()

    deck = _get_deck_by_id(deck_id)

    button = deck.buttons[button_position]
    for action in button.actions:
        if action.id == action_id:
            action_dao.delete(action)
            button.actions.remove(action)

    return render_template('configuration.html', button=button)


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

    connected_decks = Deck.get_connected(update_images=True)

    for conn_deck in connected_decks:
        conn_deck.open()
        conn_deck.set_callbacks()
