import unittest
from unittest.mock import patch

from input.key import Key, KeyGroup, pkey


class TestKey(unittest.TestCase):

    def test_init(self):
        key = Key('a', 'a')
        self.assertEqual('a', key.name)
        self.assertEqual('a', key.pkey)

    def test_str(self):
        key = Key('F1', pkey.f1)

        self.assertEqual('F1', str(key))

    def test_repr(self):
        key = Key('F1', pkey.f1)

        self.assertEqual('F1', repr(key))

    def test_hash(self):
        key = Key('F1', pkey.f1)

        self.assertEqual(hash('F1'), hash(key))

    def test_eq_equals(self):
        key1 = Key('F1', pkey.f1)
        key2 = Key('F1', pkey.f1)

        self.assertEqual(key1, key2)

    def test_eq_diff_types(self):
        key1 = Key('F1', pkey.f1)
        key2 = 'ABC'

        self.assertNotEqual(key1, key2)

    def test_eq_diff_names(self):
        key1 = Key('F1', pkey.f1)
        key2 = Key('F2', pkey.f2)

        self.assertNotEqual(key1, key2)

    def test_json(self):
        key = Key('F1', pkey.f1)

        self.assertEqual({ 'value': 'F1' }, key.json())

    def test_get_function_keys(self):
        function_keys = Key.get_function_keys()
        
        self.assertEqual(24, len(function_keys))
        self.assertEqual('F3', function_keys[2].name)

    def test_get_alpha_keys(self):
        alpha_keys = Key.get_alpha_keys()

        self.assertEqual(26, len(alpha_keys))
        self.assertEqual('j', alpha_keys[9].name)

    def test_get_num_keys(self):
        num_keys = Key.get_num_keys()

        self.assertEqual(10, len(num_keys))
        self.assertEqual('7', num_keys[7].name)

    def test_get_special_keys(self):
        special_keys = Key.get_special_keys()

        self.assertTrue(any(key.name == 'ENTER' for key in special_keys))
        self.assertTrue(any(key.name == 'ESC' for key in special_keys))
        self.assertTrue(any(key.name == 'SPACE' for key in special_keys))

    @patch('input.key.Key.get_special_keys')
    @patch('input.key.Key.get_num_keys')
    @patch('input.key.Key.get_alpha_keys')
    @patch('input.key.Key.get_function_keys')
    def test_get_all_keys(self, m_function, m_alpha, m_num, m_special):
        f1 = Key('F1', pkey.f1)
        f2 = Key('F2', pkey.f2)
        m_function.return_value = [f1, f2]

        a = Key('a', 'a')
        q = Key('q', 'q')
        m_alpha.return_value = [a, q]

        three = Key('3', '3')
        m_num.return_value = [three]

        enter = Key('ENTER', pkey.enter)
        esc = Key('ESC', pkey.esc)
        m_special.return_value = [enter, esc]

        all_keys = Key.get_all_keys()
        self.assertEqual(7, len(all_keys))

        self.assertTrue(f1 in all_keys)
        self.assertTrue(f2 in all_keys)
        self.assertTrue(a in all_keys)
        self.assertTrue(q in all_keys)
        self.assertTrue(three in all_keys)
        self.assertTrue(enter in all_keys)
        self.assertTrue(esc in all_keys)


class TestKeyGroup(unittest.TestCase):

    def test_init(self):
        keys = [Key('a', 'a'), Key('e', 'e')]
        kgroup = KeyGroup('Vowels', keys)

        self.assertEqual([Key('a', 'a'), Key('e', 'e')], kgroup.keys)
        self.assertEqual('Vowels', kgroup.name)

    def test_str(self):
        keys = [Key('a', 'a'), Key('e', 'e')]
        kgroup = KeyGroup('Vowels', keys)

        self.assertEqual('Vowels', str(kgroup))

    def test_repr(self):
        keys = [Key('a', 'a'), Key('e', 'e')]
        kgroup = KeyGroup('Vowels', keys)

        self.assertEqual('Vowels', repr(kgroup))

    def test_json(self):
        keys = [Key('a', 'a'), Key('e', 'e')]
        kgroup = KeyGroup('Vowels', keys)

        self.assertEqual({
            'keys': [Key('a', 'a').json(), Key('e', 'e').json()],
            'name': 'Vowels'
        }, kgroup.json())

    @patch('input.key.Key.get_special_keys')
    @patch('input.key.Key.get_num_keys')
    @patch('input.key.Key.get_alpha_keys')
    @patch('input.key.Key.get_function_keys')
    def test_get_all(self, m_function, m_alpha, m_num, m_special):
        f1 = Key('F1', pkey.f1)
        f2 = Key('F2', pkey.f2)
        m_function.return_value = [f1, f2]

        a = Key('a', 'a')
        q = Key('q', 'q')
        m_alpha.return_value = [a, q]

        three = Key('3', '3')
        m_num.return_value = [three]

        enter = Key('ENTER', pkey.enter)
        esc = Key('ESC', pkey.esc)
        m_special.return_value = [enter, esc]

        all_keys = KeyGroup.get_all()

        self.assertEqual('Special', all_keys[0].name)
        self.assertTrue(enter in all_keys[0].keys)

        self.assertEqual('Alpha', all_keys[1].name)
        self.assertTrue(q in all_keys[1].keys)

        self.assertEqual('Numbers', all_keys[2].name)
        self.assertTrue(three in all_keys[2].keys)

        self.assertEqual('Function', all_keys[3].name)
        self.assertTrue(f1 in all_keys[3].keys)

        m_function.assert_called()
        m_alpha.assert_called()
        m_num.assert_called()
        m_special.assert_called()


if __name__ == '__main__':
    unittest.main()
