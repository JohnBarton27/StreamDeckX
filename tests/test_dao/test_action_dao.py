import unittest
from unittest.mock import MagicMock, patch

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


if __name__ == '__main__':
    unittest.main()
