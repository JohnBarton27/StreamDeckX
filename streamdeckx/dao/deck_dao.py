import logging

from dao.dao import Dao


class DeckDao(Dao):

    def get_by_id(self, obj_id):
        conn = DeckDao.get_db_conn()

        with conn:
            cursor = conn.cursor()
            cursor.execute(f"""
                SELECT * FROM deck WHERE id='{obj_id}';
            """)

            result = cursor.fetchone()
            logging.info(f'RESULT: {result}')

        deck = self.get_obj_from_result(result)
        return deck

    def create(self, obj):
        conn = DeckDao.get_db_conn()

        with conn:
            cursor = conn.cursor()
            cursor.execute(f"""
                INSERT INTO deck (id, name) VALUES (?, ?);
            """, (obj.id, obj.name))
            conn.commit()

    def get_obj_from_result(self, result):

