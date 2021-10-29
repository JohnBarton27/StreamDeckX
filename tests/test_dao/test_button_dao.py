import unittest
from unittest.mock import MagicMock, patch

from dao.button_dao import ButtonDao


class TestButtonDao(unittest.TestCase):

    def setUp(self) -> None:
        get_conn_patch = patch('dao.button_dao.ButtonDao.get_db_conn')
        self.m_get_conn = get_conn_patch.start()
        self.addCleanup(get_conn_patch.stop)

        # Mock Connection
        self.m_conn = MagicMock()
        self.m_get_conn.return_value = self.m_conn

        # Mock Cursor
        self.m_cursor = MagicMock()
        self.m_conn.cursor.return_value = self.m_cursor

        # Action Dao
        actions_for_btn_patch = patch('dao.action_dao.ActionDao.get_for_button')
        self.m_actions_for_btn = actions_for_btn_patch.start()
        self.addCleanup(actions_for_btn_patch.stop)

        # Logging
        log_debug_patch = patch('dao.button_dao.logging.debug')
        self.m_log_debug = log_debug_patch.start()
        self.addCleanup(log_debug_patch.stop)

    def test_get_by_id_dne(self):
        self.m_cursor.fetchall.return_value = []

        bd = ButtonDao()
        result = bd.get_by_id(123)
        self.m_cursor.execute.assert_called_with('SELECT * FROM button WHERE id=?;', ('123',))

        self.assertIsNone(result)

    @patch('dao.button_dao.ButtonDao.get_obj_from_result')
    def test_get_by_id_no_deck(self, m_obj_from_res):
        self.m_cursor.fetchall.return_value = [{'id': 123}]

        action1 = MagicMock()
        action2 = MagicMock()
        self.m_actions_for_btn.return_value = [action1, action2]

        button = MagicMock()
        m_obj_from_res.return_value = button

        bd = ButtonDao()
        result = bd.get_by_id(123)

        self.assertEqual(result, button)
        self.assertEqual(result.actions, [action1, action2])

        m_obj_from_res.assert_called_with({'id': 123}, deck=None)
        self.m_actions_for_btn.assert_called_with(button)

    @patch('dao.button_dao.ButtonDao.get_obj_from_result')
    def test_get_by_id_with_deck(self, m_obj_from_res):
        self.m_cursor.fetchall.return_value = [{'id': 123}]

        action1 = MagicMock()
        action2 = MagicMock()
        self.m_actions_for_btn.return_value = [action1, action2]

        deck = MagicMock()

        button = MagicMock()
        m_obj_from_res.return_value = button

        bd = ButtonDao()
        result = bd.get_by_id(123, deck=deck)

        self.assertEqual(result, button)
        self.assertEqual(result.actions, [action1, action2])

        m_obj_from_res.assert_called_with({'id': 123}, deck=deck)
        self.m_actions_for_btn.assert_called_with(button)


if __name__ == '__main__':
    unittest.main()
