import logging
import sqlite3 as sl

from dao.dao import Dao
from button_style import ButtonStyle


class ButtonDao(Dao):

    def get_by_id(self, button_id):
        """
        Given a button ID, returns that button object

        Args:
            button_id (int): Database ID of the button

        Returns:
            Button: button object
        """
        conn = ButtonDao.get_db_conn()

        with conn:
            conn.row_factory = sl.Row
            cursor = conn.cursor()
            cursor.execute("""
                SELECT * FROM button WHERE id=?;
            """, (str(button_id),))

            result = cursor.fetchall()
            if not result:
                return None

        button = ButtonDao.get_obj_from_result(dict(result[0]))
        return button

    def get_for_deck(self, deck):
        conn = ButtonDao.get_db_conn()

        with conn:
            conn.row_factory = sl.Row
            cursor = conn.cursor()
            cursor.execute("""
                SELECT * FROM button WHERE deck_id=?;
            """, (str(deck.id),))

            results = cursor.fetchall()
            if not results:
                return None

        buttons = ButtonDao.get_objs_from_result(results, deck=deck)
        return buttons

    def create(self, button):
        conn = ButtonDao.get_db_conn()

        with conn:
            cursor = conn.cursor()
            cursor.execute(f"""
                INSERT into button (deck_id, position) VALUES (?, ?);
            """, (button.deck.id, button.position))
            conn.commit()

    def update(self, button):
        conn = ButtonDao.get_db_conn()

        with conn:
            cursor = conn.cursor()
            cursor.execute(f"""
                UPDATE button SET icon = ?, font = ?, label = ? WHERE id = ?;
            """, (button.style.icon, button.style.font, button.style.label, button.id))
            logging.info(f'Updating button ({button.id}): icon = {button.style.icon} | font = {button.style.font} | label = {button.style.label}')
            conn.commit()

    @staticmethod
    def get_obj_from_result(result, deck=None):
        from button import Button

        position = result['position']
        btn_id = result['id']
        deck_id = result['deck_id']
        icon = result['icon']
        font = result['font']
        label = result['label']

        if not deck:
            from dao.deck_dao import DeckDao
            deck_dao - DeckDao()
            deck = deck_dao.get_by_id(deck_id, include_buttons=False)

        if icon or font or label:
            bs = ButtonStyle('style', icon, font, label)
        else:
            bs = None

        logging.info(f'Returning button {btn_id}')

        button = Button(position, deck, style=bs, btn_id=btn_id)
        return button

    @staticmethod
    def get_objs_from_result(results, deck):
        buttons = []

        deck.open()
        for result in results:
            buttons.append(ButtonDao.get_obj_from_result(dict(result), deck=deck))
        deck.close()

        return buttons
