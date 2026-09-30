import unittest
from features import extract_tickers, sentiment
from reddit_adapter import Reddit


class ReviewTests(unittest.TestCase):
    def test_mentions(self):
        self.assertEqual(extract_tickers('$AAPL bullish; MSFT strong', ['AAPL', 'MSFT']), ['AAPL', 'MSFT'])

    def test_sentiment(self):
        self.assertGreater(sentiment('bullish strong growth'), 0)
        self.assertLess(sentiment('not bullish, weak'), 0)

    def test_access_disabled_without_permission(self):
        with self.assertRaisesRegex(ValueError, 'disabled'):
            Reddit().collect({'reddit_permitted': False})


if __name__ == '__main__':
    unittest.main()
