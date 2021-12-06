import base64
import logging
import os
import sqlite3 as sl
from urllib.request import pathname2url

from flask import Flask, render_template, request

from input.key import KeyGroup


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
    background_color = request.form['backgroundColor']
    text_color = request.form['textColor']
    font_size = int(request.form['fontSize'])

    logging.info(f'Setting {button_position} on {deck_id} to {button_text}')

    deck = _get_deck_by_id(deck_id)
    button = deck.buttons[button_position]

    if len(request.files) > 0:
        # Handle Background Image Uploads
        background_image = request.files['backgroundImage']

        if background_image.filename != '':
            if not os.path.exists('temp_images'):
                os.mkdir('temp_images')

            extension = background_image.filename.split('.')[-1]
            temp_name = f'temp_image.{extension}'
            background_image.save(f'temp_images/{temp_name}')

            with open(f"temp_images/{temp_name}", "rb") as image_file:
                img_string = base64.b64encode(image_file.read())
                button.set_background_image(img_string)

            # Delete temporary file
            os.remove(f"temp_images/{temp_name}")

    button.set_text(button_text)
    button.set_colors(text_color, background_color)
    button.set_font_size(font_size)

    return button.button_image.image_bytes.decode("utf-8")


@app.route('/setButtonAction', methods=['POST'])
def set_button_action():
    from action.action import MultiKeyPressAction, DelayAction
    from action.text_action import TextAction

    from dao.action_dao import ActionDao

    deck_id = request.form['deckId']
    button_position = int(request.form['button'])
    action = request.form['action_text']
    action_type = request.form['type']

    deck = _get_deck_by_id(deck_id)

    button = deck.buttons[button_position]

    if action_type == 'TEXT':
        action = TextAction(action, button, 0)
    elif action_type == 'MULTIKEY':
        action = MultiKeyPressAction(action, button, 0)
    elif action_type == 'DELAY':
        action = DelayAction(action, button, 0)
    else:
        raise Exception(f'Unknown action type: {action_type}')

    action_dao = ActionDao()
    action_dao.create(action)
    button.add_action(action)

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


# API
@app.route('/api/v1/keys', methods=['GET'])
def get_all_keys():
    json = {
        'groups': []
    }
    for key_group in KeyGroup.get_all():
        json['groups'].append(key_group.json())

    return json


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
                    font TEXT,
                    font_size INTEGER DEFAULT 16,
                    label TEXT,
                    background_color TEXT DEFAULT '#000000',
                    text_color TEXT DEFAULT '#ffffff',
                    background_image TEXT
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
