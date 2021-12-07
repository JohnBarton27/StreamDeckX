import unittest
from unittest.mock import MagicMock, patch

from test_base import BaseStreamdeckXTest

from action.application_action import ApplicationAction


class TestApplicationAction(BaseStreamdeckXTest):

    def test_action_type(self):
        btn = MagicMock()
        action = ApplicationAction('/home/john/my_app.sh', btn, 0)

        self.assertEqual('APPLICATION', action.action_type)

    def test_init(self):
        btn = MagicMock()
        action = ApplicationAction('/home/john/my_app.sh', btn, 0)

        self.assertEqual('/home/john/my_app.sh', action.application)
        self.assertEqual(btn, action.button)

    def test_display_value(self):
        btn = MagicMock()
        action = ApplicationAction('/home/john/my_app.sh', btn, 1)
        self.assertEqual('Open /home/john/my_app.sh', action.display_value)

    @patch('subprocess.call')
    def test_execute(self, m_sub_call):
        btn = MagicMock()
        action = ApplicationAction('/home/john/my_app.sh', btn, 1)
        action.execute()

        m_sub_call.assert_called_with('/home/john/my_app.sh')


if __name__ == '__main__':
    unittest.main()
