import logging
import sqlite3 as sl

from button_style import ButtonStyle
from dao.action_dao import ActionDao
from dao.dao import Dao


class ButtonDao(Dao):
    action_dao = ActionDao()

    def get_by_id(self, button_id: int, deck=None):
        """
        Given a button ID, returns that button object

        Args:
            button_id (int): Database ID of the button
            deck (Deck): Deck that this button lives on [optional]. If not given, will pull from the database using a separate query.

        Returns:
            Button: button object
        """
        conn = ButtonDao.get_db_conn()

        with conn:
            conn.row_factory = sl.Row
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM button WHERE id=?;', (str(button_id),))

            result = cursor.fetchall()
            if not result:
                return None

        button = ButtonDao.get_obj_from_result(dict(result[0]), deck=deck)
        button.actions = ButtonDao.action_dao.get_for_button(button)
        return button

    def get_for_deck(self, deck):
        """
        Given a Deck object, get all Buttons that are on this Deck

        Args:
            deck (Deck): Deck object to get all the buttons for

        Returns:
            Button[]: List of Button objects
        """
        conn = ButtonDao.get_db_conn()

        with conn:
            conn.row_factory = sl.Row
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM button WHERE deck_id=?;', (str(deck.id),))

            results = cursor.fetchall()
            if not results:
                return None

        buttons = ButtonDao.get_objs_from_result(results, deck=deck)
        for button in buttons:
            db_actions = ButtonDao.action_dao.get_for_button(button)
            button.actions = db_actions if db_actions else []
        return buttons

    def create(self, button):
        """
        Creates the given Button object in the database.

        Args:
            button (Button): Button object to insert into the database

        Returns:
            None
        """
        conn = ButtonDao.get_db_conn()

        with conn:
            cursor = conn.cursor()
            cursor.execute('INSERT INTO button (deck_id, position) VALUES (?, ?);', (button.deck.id, button.position))
            conn.commit()
            button.id = cursor.lastrowid

    def update(self, button):
        """
        Updates the given Button in the database

        Args:
            button (Button): Button object that already exists in the database, but may need updating

        Returns:
            None
        """
        if not button.id:
            from button import ButtonMissingIdError
            raise ButtonMissingIdError('Must set Button ID before updating!')

        conn = ButtonDao.get_db_conn()

        with conn:
            cursor = conn.cursor()
            cursor.execute('UPDATE button SET font = ?, font_size = ?, label = ?, background_color = ?, text_color = ?, background_image = ? WHERE id = ?;',
                           (button.style.font, button.style.font_size, button.style.label, button.style.background_color, button.style.text_color, button.style.background_image, button.id))
            logging.debug(f'Updating button ({button.id}): font = {button.style.font} | font_size = {button.style.font_size} | label = {button.style.label} | background_color = {button.style.background_color} | text_color = {button.style.text_color}')
            conn.commit()

    @staticmethod
    def get_obj_from_result(result, deck=None):
        """
        Given a single SQL result containing a single button, get the Button object represented by this result.

        Args:
            result (dict): SQL result containing a single button
            deck (Deck): Deck object this Button belongs to - if not given, will use a separate DB query to populate

        Returns:
            Button: Button object represented by the SQL result
        """
        from button import Button

        position = result['position']
        btn_id = result['id']
        deck_id = result['deck_id']
        font = result['font']
        font_size = result['font_size']
        label = result['label']
        background_color = result['background_color']
        text_color = result['text_color']
        background_image = result['background_image']

        if not deck:
            from dao.deck_dao import DeckDao
            deck_dao = DeckDao()
            deck = deck_dao.get_by_id(deck_id, include_buttons=False)

        if any([font, label, background_image]):
            bs = ButtonStyle('style', font, font_size=font_size, label=label, background_color=background_color, text_color=text_color, background_image=background_image)
        else:
            bs = None

        button = Button(position, deck, style=bs, btn_id=btn_id)
        return button

    @staticmethod
    def get_objs_from_result(results, deck=None):
        """
        Given a set of SQL results (which may contain multiple rows, each corresponding to a different button on the same Deck), get the Button objects that are represented by the SQL results.

        Args:
            results (list): List of SQL rows that each contain a button, all on the same Deck
            deck (Deck): Stream Deck that all the buttons live on. If not given, will be populated.

        Returns:
            Button[]: List of Button objects
        """
        buttons = []

        for result in results:

            if not deck:
                # Setup 'deck' once
                from dao.deck_dao import DeckDao
                deck_id = result['deck_id']
                deck_dao = DeckDao()
                deck = deck_dao.get_by_id(deck_id, include_buttons=False)

            buttons.append(ButtonDao.get_obj_from_result(dict(result), deck=deck))

        return buttons
