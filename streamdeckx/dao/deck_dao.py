import logging
import sqlite3 as sl

from button import Button
from dao.button_dao import ButtonDao
from dao.dao import Dao
from deck_types import DeckTypes


class DeckDao(Dao):

    button_dao = ButtonDao()

    def get_by_id(self, deck_id):
        conn = DeckDao.get_db_conn()

        with conn:
            conn.row_factory = sl.Row
            cursor = conn.cursor()
            cursor.execute(f"""
                SELECT * FROM deck WHERE id='{deck_id}';
            """)

            result = cursor.fetchall()
            if not result:
                return None

        deck = self.get_obj_from_result(dict(result[0]))
        return deck

    def create(self, deck):
        conn = DeckDao.get_db_conn()

        with conn:
            cursor = conn.cursor()
            cursor.execute(f"""
                INSERT INTO deck (id, name, type) VALUES (?, ?, ?);
            """, (deck.id, deck.name, deck.__class__.type.name))
            conn.commit()

            # Create all buttons
            for button in deck.buttons:
                DeckDao.button_dao.create(button)

    def get_obj_from_result(self, result):
        from deck import XLDeck, OriginalDeck
        deck_id = result['id']
        deck_type_name = result['type']
        deck_type = DeckTypes.get_by_name(deck_type_name)

        if deck_type == DeckTypes.XL:
            return XLDeck(deck_id)

        if deck_type == DeckTypes.ORIGINAL:
            return OriginalDeck(deck_id)

        # TODO add handling for mini
