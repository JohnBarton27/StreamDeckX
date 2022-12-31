import logging
import sqlite3 as sl

from button import Button
from dao.button_dao import ButtonDao
from dao.dao import Dao
from deck_types import DeckTypes


class DeckDao(Dao):

    button_dao = ButtonDao()

    def get_by_id(self, deck_id, include_buttons=True):
        conn = DeckDao.get_db_conn()

        with conn:
            conn.row_factory = sl.Row
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM deck WHERE id=?;', (deck_id,))

            results = cursor.fetchall()
            if not results:
                return None

        deck = self.get_obj_from_result(results, include_buttons=include_buttons)
        return deck

    def create(self, deck):
        conn = DeckDao.get_db_conn()

        with conn:
            cursor = conn.cursor()

            if hasattr(deck, 'rows') and hasattr(deck, 'cols'):
                cursor.execute('INSERT INTO deck (id, name, type, num_cols, num_rows) VALUES (?, ?, ?, ?, ?);',
                               (deck.id, deck.name, deck.__class__.type.name, deck.cols, deck.rows))
            else:
                cursor.execute('INSERT INTO deck (id, name, type) VALUES (?, ?, ?);',
                               (deck.id, deck.name, deck.__class__.type.name))
            conn.commit()

            # Create all buttons
            for button in deck.buttons:
                DeckDao.button_dao.create(button)

    def get_by_type(self, deck_type: DeckTypes):
        decks = []
        conn = DeckDao.get_db_conn()

        with conn:
            conn.row_factory = sl.Row
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM deck WHERE type = ?;',
                           (deck_type.name,))
            results = cursor.fetchall()
            if not results:
                return None

        for result in results:
            decks.append(self.get_obj_from_result(result, include_buttons=True))

        return decks

    def get_obj_from_result(self, results, include_buttons=True):
        from deck import XLDeck, OriginalDeck, VirtualDeck
        first_row = dict(results[0]) if isinstance(results, list) else dict(results)

        deck_id = first_row['id']
        deck_type_name = first_row['type']
        deck_type = DeckTypes.get_by_name(deck_type_name)

        deck = None
        if deck_type == DeckTypes.XL:
            deck = XLDeck(deck_id)

        if deck_type == DeckTypes.ORIGINAL:
            deck = OriginalDeck(deck_id)

        if deck_type == DeckTypes.VIRTUAL:
            rows = first_row['num_rows']
            cols = first_row['num_cols']
            deck = VirtualDeck(deck_id, rows=rows, cols=cols)

        # TODO add handling for mini

        # Get buttons
        if include_buttons:
            button_dao = ButtonDao()
            deck.buttons = button_dao.get_for_deck(deck)

        return deck
