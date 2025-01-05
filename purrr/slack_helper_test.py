"""Unit tests for the "slack_helper" module."""

import unittest

import slack_helper


class SlackHelperTest(unittest.TestCase):
    """Unit tests for the "slack_helper" module."""

    def test_normalize_channel_name(self):
        self.assertEqual(slack_helper.normalize_channel_name(""), "")
        self.assertEqual(slack_helper.normalize_channel_name('"isn\'t"'), "isnt")
        self.assertEqual(slack_helper.normalize_channel_name("TEST"), "test")
        self.assertEqual(slack_helper.normalize_channel_name("1  2--3__4"), "1-2-3-4")
        self.assertEqual(slack_helper.normalize_channel_name("a `~!@#$%^&*() 1"), "a-1")
        self.assertEqual(slack_helper.normalize_channel_name("b -_=+ []{}|\\ 2"), "b-2")
        self.assertEqual(slack_helper.normalize_channel_name("c ;:'\" ,.<>/? 3"), "c-3")
        self.assertEqual(slack_helper.normalize_channel_name("-foo "), "foo")


if __name__ == "__main__":
    unittest.main()
