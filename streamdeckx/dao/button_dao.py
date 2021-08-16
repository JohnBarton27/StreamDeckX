import sqlite3 as sl

from dao.dao import Dao


class ButtonDao(Dao):

    def get_by_id(self, button_id):
        conn = ButtonDao.get_db_conn()

        with conn:
            conn.row_factory = sl.Row
            cursor = conn.cursor()
            cursor.execute("""
                SELECT * FROM button WHERE id=?;
            """, button_id)

            result = cursor.fetchall()
            if not result:
                return None

        button = self.get_obj_from_result(dict(result[0]))
        return button

    def create(self, button):
        conn = ButtonDao.get_db_conn()

        with conn:
            cursor = conn.cursor()
            cursor.execute(f"""
                INSERT into button (deck_id, position) VALUES (?, ?);
            """, button.deck.id, button.position)

    def get_obj_from_result(self, result):
        from button import Button

        position = result['position']
        btn_id = result['id']

        # TODO add button styling to retrieval

        button = Button(position, None, btn_id=btn_id)
        return button
