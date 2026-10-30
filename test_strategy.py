import unittest
from strategy import decide


class DecisionTests(unittest.TestCase):
    def test_rising_trend_respects_both_position_limits(self):
        prices = [100 + i for i in range(40)]
        d = decide(prices)
        self.assertEqual(d.signal, "LONG")
        self.assertLessEqual(d.suggested_shares * prices[-1], 2000)
        self.assertLessEqual(d.suggested_shares * prices[-1] * .05, 100)

    def test_falling_or_flat_market_has_no_long_position(self):
        for prices in ([150 - i for i in range(40)], [100] * 40):
            self.assertEqual(decide(prices).suggested_shares, 0)
            self.assertEqual(decide(prices).signal, "FLAT")

    def test_invalid_and_insufficient_data_is_rejected(self):
        for prices in ([100] * 3, [100] * 20 + [float("nan")], [100] * 20 + [0]):
            with self.assertRaises(ValueError):
                decide(prices)

    def test_small_budget_cannot_buy_fractional_share(self):
        self.assertEqual(decide(range(100, 140), equity=1).suggested_shares, 0)


if __name__ == "__main__":
    unittest.main()
