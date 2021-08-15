import logging
import sqlite3 as sl

from dao.dao import Dao


class DeckDao(Dao):

    def get_by_id(self, obj_id):
        conn = DeckDao.get_db_conn()

        with conn:
            conn.row_factory = sl.Row
            cursor = conn.cursor()
            cursor.execute(f"""
                SELECT * FROM deck WHERE id='{obj_id}';
            """)

            result = cursor.fetchall()
            if not result:
                return None

        deck = self.get_obj_from_result(dict(result[0]))
        return deck

    def create(self, obj):
        conn = DeckDao.get_db_conn()

        with conn:
            cursor = conn.cursor()
            cursor.execute(f"""
                INSERT INTO deck (id, name) VALUES (?, ?);
            """, (obj.id, obj.name))
            conn.commit()

    def get_obj_from_result(self, cursor):
        from deck import XLDeck, OriginalDeck
        deck_id = cursor['id']
        name = cursor['name']

        if name == 'Stream Deck XL':
            return XLDeck(deck_id)

        if name == 'Stream Deck (Original)':
            return OriginalDeck(deck_id)


