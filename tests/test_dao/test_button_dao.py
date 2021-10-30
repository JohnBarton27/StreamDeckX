import unittest
from unittest.mock import MagicMock, call, patch

from dao.button_dao import ButtonDao
from button import Button, ButtonMissingIdError


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

        self.m_cursor.execute.assert_called_with('SELECT * FROM button WHERE id=?;', ('123',))
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

        self.m_cursor.execute.assert_called_with('SELECT * FROM button WHERE id=?;', ('123',))
        m_obj_from_res.assert_called_with({'id': 123}, deck=deck)
        self.m_actions_for_btn.assert_called_with(button)

    def test_get_for_deck_dne(self):
        self.m_cursor.fetchall.return_value = []

        deck = MagicMock()
        deck.id = 'abc123'

        bd = ButtonDao()
        buttons = bd.get_for_deck(deck)

        self.assertIsNone(buttons)

        self.m_cursor.execute.assert_called_with('SELECT * FROM button WHERE deck_id=?;', ('abc123',))

    @patch('dao.button_dao.ButtonDao.get_objs_from_result')
    def test_get_for_deck(self, m_objs_from_res):
        self.m_cursor.fetchall.return_value = [{'id': '1'}, {'id': '2'}]

        deck = MagicMock()
        deck.id = 'abc123'

        button1 = MagicMock()
        button2 = MagicMock()

        m_objs_from_res.return_value = [button1, button2]

        action1 = MagicMock()
        action2 = MagicMock()
        action3 = MagicMock()
        self.m_actions_for_btn.side_effect = [[action1, action2], [action3]]

        bd = ButtonDao()
        buttons = bd.get_for_deck(deck)

        self.assertEqual([button1, button2], buttons)
        self.assertEqual([action1, action2], button1.actions)
        self.assertEqual([action3], button2.actions)

        self.m_cursor.execute.assert_called_with('SELECT * FROM button WHERE deck_id=?;', ('abc123',))
        m_objs_from_res.assert_called_with([{'id': '1'}, {'id': '2'}], deck=deck)
        self.m_actions_for_btn.assert_has_calls([call(button1), call(button2)])

    def test_create(self):
        deck = MagicMock()
        deck.id = 'abc123'
        button = Button(12, deck)

        bd = ButtonDao()

        self.m_cursor.lastrowid = 57

        bd.create(button)

        self.assertEqual(57, button.id)

        self.m_cursor.execute.assert_called_with('INSERT INTO button (deck_id, position) VALUES (?, ?);', ('abc123', 12))

    def test_update(self):
        deck = MagicMock()
        deck.id = 'abc123'
        button = Button(12, deck, btn_id=57)

        style = MagicMock()
        style.icon = 'my_icon.png'
        style.font = 'Arial'
        style.label = 'Press Me!'

        button.style = style

        bd = ButtonDao()
        bd.update(button)

        self.m_cursor.execute.assert_called_with('UPDATE button SET icon = ?, font = ?, label = ? WHERE id = ?;', ('my_icon.png', 'Arial', 'Press Me!', 57))
        self.m_log_debug.assert_called()

    def test_update_missing_id(self):
        deck = MagicMock()
        deck.id = 'abc123'
        button = Button(12, deck)

        bd = ButtonDao()
        self.assertRaises(ButtonMissingIdError, bd.update, button)

        self.m_cursor.execute.assert_not_called()


if __name__ == '__main__':
    unittest.main()
