import unittest
from unittest.mock import patch, MagicMock

from dao.deck_dao import DeckDao


class TestDeckDao(unittest.TestCase):

    def setUp(self) -> None:
        get_conn_patch = patch('dao.deck_dao.DeckDao.get_db_conn')
        self.m_get_conn = get_conn_patch.start()
        self.addCleanup(get_conn_patch.stop)

        # Mock Connection
        self.m_conn = MagicMock()
        self.m_get_conn.return_value = self.m_conn

        # Mock Cursor
        self.m_cursor = MagicMock()
        self.m_conn.cursor.return_value = self.m_cursor

    def test_get_by_id_dne(self):
        self.m_cursor.fetchall.return_value = []

        dd = DeckDao()
        deck = dd.get_by_id('abc123')

        self.assertIsNone(deck)

        self.m_cursor.execute.assert_called_with('SELECT * FROM deck WHERE id=?;', ('abc123',))

    @patch('dao.deck_dao.DeckDao.get_obj_from_result')
    def test_get_by_id(self, m_obj_from_res):
        self.m_cursor.fetchall.return_value = [{'id': 'abc123'}]

        deck = MagicMock()
        m_obj_from_res.return_value = deck

        dd = DeckDao()
        result = dd.get_by_id('abc123')

        self.assertEqual(deck, result)

        self.m_cursor.execute.assert_called_with('SELECT * FROM deck WHERE id=?;', ('abc123',))
        m_obj_from_res.assert_called_with([{'id': 'abc123'}], include_buttons=True)


if __name__ == '__main__':
    unittest.main()
