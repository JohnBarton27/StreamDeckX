import unittest
from unittest.mock import MagicMock, patch

from action import TextAction, ActionMissingIdError
from dao.action_dao import ActionDao


class TestActionDao(unittest.TestCase):

    def setUp(self) -> None:
        get_conn_patch = patch('dao.action_dao.ActionDao.get_db_conn')
        self.m_get_conn = get_conn_patch.start()
        self.addCleanup(get_conn_patch.stop)

        # Mock Connection
        self.m_conn = MagicMock()
        self.m_get_conn.return_value = self.m_conn

        # Mock Cursor
        self.m_cursor = MagicMock()
        self.m_conn.cursor.return_value = self.m_cursor

        # Logging
        log_debug_patch = patch('dao.action_dao.logging.debug')
        self.m_log_debug = log_debug_patch.start()
        self.addCleanup(log_debug_patch.stop)

    def test_get_by_id_dne(self):
        self.m_cursor.fetchall.return_value = []

        ad = ActionDao()
        result = ad.get_by_id(123)
        self.m_cursor.execute.assert_called_with('SELECT * FROM action WHERE id=?;', ('123',))

        self.assertIsNone(result)

    @patch('dao.action_dao.ActionDao.get_obj_from_result')
    def test_get_by_id_exists_no_button(self, m_obj_from_result):
        self.m_cursor.fetchall.return_value = [{'id': 123}]
        retrieved_action = MagicMock()
        m_obj_from_result.return_value = retrieved_action

        ad = ActionDao()
        result = ad.get_by_id(123)
        self.m_cursor.execute.assert_called_with('SELECT * FROM action WHERE id=?;', ('123',))
        m_obj_from_result.assert_called_with({'id': 123}, button=None)

        self.assertEqual(result, retrieved_action)

    def test_get_for_button_none(self):
        self.m_cursor.fetchall.return_value = []
        button = MagicMock()
        button.id = 123

        ad = ActionDao()
        results = ad.get_for_button(button)
        self.m_cursor.execute.assert_called_with('SELECT * FROM action WHERE button_id=?;', ('123',))

        self.assertIsNone(results)

    @patch('dao.action_dao.ActionDao.get_objs_from_result')
    def test_get_for_button_single(self, m_objs_from_result):
        self.m_cursor.fetchall.return_value = [{'id': 1}]
        button = MagicMock()
        button.id = 123

        retrieved_action = MagicMock()
        m_objs_from_result.return_value = [retrieved_action]

        ad = ActionDao()
        results = ad.get_for_button(button)
        self.m_cursor.execute.assert_called_with('SELECT * FROM action WHERE button_id=?;', ('123',))

        m_objs_from_result.assert_called_with([{'id': 1}], button=button)
        self.assertEqual(results, [retrieved_action])

    @patch('dao.action_dao.ActionDao.get_objs_from_result')
    def test_get_for_button_multiple(self, m_objs_from_result):
        self.m_cursor.fetchall.return_value = [{'id': 1}, {'id': 2}, {'id': 3}]
        button = MagicMock()
        button.id = 123

        retrieved_action1 = MagicMock()
        retrieved_action2 = MagicMock()
        retrieved_action3 = MagicMock()
        m_objs_from_result.return_value = [retrieved_action1, retrieved_action2, retrieved_action3]

        ad = ActionDao()
        results = ad.get_for_button(button)
        self.m_cursor.execute.assert_called_with('SELECT * FROM action WHERE button_id=?;', ('123',))

        m_objs_from_result.assert_called_with([{'id': 1}, {'id': 2}, {'id': 3}], button=button)
        self.assertEqual(results, [retrieved_action1, retrieved_action2, retrieved_action3])

    def test_create(self):
        button = MagicMock()
        button.id = 123
        action = TextAction('My Text', button, 0)

        ad = ActionDao()
        ad.create(action)

        self.m_cursor.execute.assert_called_with(
            'INSERT INTO action (type, button_id, action_order, parameter) VALUES (?, ?, ?, ?);',
            ('TEXT', 123, 0, 'My Text'))
        self.m_conn.commit.assert_called()

    def test_update(self):
        button = MagicMock()
        button.id = 123
        action = TextAction('My Text', button, 0, action_id=4)

        ad = ActionDao()
        ad.update(action)

        self.m_cursor.execute.assert_called_with('UPDATE action SET action_order = ?, parameter = ? WHERE id = ?;',
                                                 (0, 'My Text', 4))
        self.m_conn.commit.assert_called()
        self.m_log_debug.assert_called_with('Updating action (4): action.order=0 | action.parameter=\'My Text\'')

    def test_update_no_id(self):
        button = MagicMock()
        button.id = 123
        action = TextAction('My Text', button, 0)

        ad = ActionDao()
        self.assertRaises(ActionMissingIdError, ad.update, action)

        # Nothing should have been called
        self.m_cursor.execute.assert_not_called()
        self.m_conn.commit.assert_not_called()
        self.m_log_debug.assert_not_called()

    def test_delete(self):
        button = MagicMock()
        button.id = 123
        action = TextAction('My Text', button, 0, action_id=4)

        ad = ActionDao()
        ad.delete(action)

        self.m_cursor.execute.assert_called_with('DELETE FROM action WHERE id = ?;', (4,))
        self.m_conn.commit.assert_called()
        self.m_log_debug.assert_called_with('Deleting action (4): action.order=0 | action.parameter=\'My Text\'')

    def test_delete_no_id(self):
        button = MagicMock()
        button.id = 123
        action = TextAction('My Text', button, 0)

        ad = ActionDao()
        self.assertRaises(ActionMissingIdError, ad.delete, action)

        # Nothing should have been called
        self.m_cursor.execute.assert_not_called()
        self.m_conn.commit.assert_not_called()
        self.m_log_debug.assert_not_called()

    def test_obj_from_result_with_button(self):
        button = MagicMock()

        result = {
            'id': 17,
            'type': 'TEXT',
            'button_id': 4,
            'action_order': 1,
            'parameter': 'Hello, World!'
        }

        action = ActionDao.get_obj_from_result(result, button)

        self.assertEqual(action.id, 17)
        self.assertIsInstance(action, TextAction)
        self.assertEqual(action.button, button)
        self.assertEqual(action.order, 1)
        self.assertEqual(action.parameter, 'Hello, World!')

    @patch('dao.button_dao.ButtonDao.get_by_id')
    def test_obj_from_result_without_button(self, m_button_by_id):
        button = MagicMock()
        m_button_by_id.return_value = button

        result = {
            'id': 17,
            'type': 'TEXT',
            'button_id': 4,
            'action_order': 1,
            'parameter': 'Hello, World!'
        }

        action = ActionDao.get_obj_from_result(result)

        m_button_by_id.assert_called_with(4)

        self.assertEqual(action.id, 17)
        self.assertIsInstance(action, TextAction)
        self.assertEqual(action.button, button)
        self.assertEqual(action.order, 1)
        self.assertEqual(action.parameter, 'Hello, World!')

    def test_objs_from_result_with_button(self):
        button = MagicMock()

        results = [
            {
                'id': 17,
                'type': 'TEXT',
                'button_id': 4,
                'action_order': 0,
                'parameter': 'Hello, '
            },
            {
                'id': 18,
                'type': 'TEXT',
                'button_id': 4,
                'action_order': 1,
                'parameter': 'World!'
            }
        ]

        actions = ActionDao.get_objs_from_result(results, button)

        self.assertEqual(actions[0].id, 17)
        self.assertIsInstance(actions[0], TextAction)
        self.assertEqual(actions[0].button, button)
        self.assertEqual(actions[0].order, 0)
        self.assertEqual(actions[0].parameter, 'Hello, ')

        self.assertEqual(actions[1].id, 18)
        self.assertIsInstance(actions[1], TextAction)
        self.assertEqual(actions[1].button, button)
        self.assertEqual(actions[1].order, 1)
        self.assertEqual(actions[1].parameter, 'World!')

    @patch('dao.button_dao.ButtonDao.get_by_id')
    def test_objs_from_result_without_button(self, m_button_by_id):
        button = MagicMock()
        m_button_by_id.return_value = button

        results = [
            {
                'id': 17,
                'type': 'TEXT',
                'button_id': 4,
                'action_order': 0,
                'parameter': 'Hello, '
            },
            {
                'id': 18,
                'type': 'TEXT',
                'button_id': 4,
                'action_order': 1,
                'parameter': 'World!'
            }
        ]

        actions = ActionDao.get_objs_from_result(results)

        m_button_by_id.assert_called_with(4)

        self.assertEqual(actions[0].id, 17)
        self.assertIsInstance(actions[0], TextAction)
        self.assertEqual(actions[0].button, button)
        self.assertEqual(actions[0].order, 0)
        self.assertEqual(actions[0].parameter, 'Hello, ')

        self.assertEqual(actions[1].id, 18)
        self.assertIsInstance(actions[1], TextAction)
        self.assertEqual(actions[1].button, button)
        self.assertEqual(actions[1].order, 1)
        self.assertEqual(actions[1].parameter, 'World!')


if __name__ == '__main__':
    unittest.main()
