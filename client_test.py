import unittest
from client3 import getDataPoint, getRatio

class ClientTest(unittest.TestCase):
    def test_getDataPoint_calculatePrice(self):
        quotes = [
            {'top_ask': {'price': 121.2, 'size': 36}, 'timestamp': '2019-02-11 22:06:30.572453', 'top_bid': {'price': 120.48, 'size': 109}, 'id': '0.109974697771', 'stock': 'ABC'},
            {'top_ask': {'price': 121.68, 'size': 4}, 'timestamp': '2019-02-11 22:06:30.572453', 'top_bid': {'price': 117.87, 'size': 81}, 'id': '0.109974697771', 'stock': 'DEF'}
        ]
        for quote in quotes:
            self.assertEqual(getDataPoint(quote), 
                (quote['stock'], quote['top_bid']['price'], quote['top_ask']['price'], (quote['top_bid']['price'] + quote['top_ask']['price']) / 2))

    def test_getDataPoint_calculatePriceBidGreaterThanAsk(self):
        quotes = [
            {'top_ask': {'price': 119.2, 'size': 36}, 'timestamp': '2019-02-11 22:06:30.572453', 'top_bid': {'price': 120.48, 'size': 109}, 'id': '0.109974697771', 'stock': 'ABC'},
            {'top_ask': {'price': 121.68, 'size': 4}, 'timestamp': '2019-02-11 22:06:30.572453', 'top_bid': {'price': 117.87, 'size': 81}, 'id': '0.109974697771', 'stock': 'DEF'}
        ]
        for quote in quotes:
            self.assertEqual(getDataPoint(quote), 
                (quote['stock'], quote['top_bid']['price'], quote['top_ask']['price'], (quote['top_bid']['price'] + quote['top_ask']['price']) / 2))

    def test_getDataPoint_withZeroPrices(self):
        quote = {'top_ask': {'price': 0, 'size': 36}, 'timestamp': '2019-02-11 22:06:30.572453', 'top_bid': {'price': 0, 'size': 109}, 'id': '0.109974697771', 'stock': 'ABC'}
        expected = ('ABC', 0, 0, 0)
        self.assertEqual(getDataPoint(quote), expected)

    def test_getDataPoint_withNegativePrices(self):
        quote = {'top_ask': {'price': -121.2, 'size': 36}, 'timestamp': '2019-02-11 22:06:30.572453', 'top_bid': {'price': -120.48, 'size': 109}, 'id': '0.109974697771', 'stock': 'ABC'}
        expected = ('ABC', -120.48, -121.2, (-120.48 + -121.2) / 2)
        self.assertEqual(getDataPoint(quote), expected)

    def test_getDataPoint_withLargePrices(self):
        quote = {'top_ask': {'price': 1000000, 'size': 36}, 'timestamp': '2019-02-11 22:06:30.572453', 'top_bid': {'price': 999999, 'size': 109}, 'id': '0.109974697771', 'stock': 'ABC'}
        expected = ('ABC', 999999, 1000000, (999999 + 1000000) / 2)
        self.assertEqual(getDataPoint(quote), expected)

    def test_getRatio_normalCase(self):
        self.assertEqual(getRatio(120, 60), 2)

    def test_getRatio_priceBZero(self):
        self.assertIsNone(getRatio(120, 0))

    def test_getRatio_priceAZero(self):
        self.assertEqual(getRatio(0, 120), 0)

    def test_getRatio_bothPricesZero(self):
        self.assertIsNone(getRatio(0, 0))

    def test_getRatio_withNegativePrices(self):
        self.assertEqual(getRatio(-120, 60), -2)

    def test_getRatio_withLargePrices(self):
        self.assertEqual(getRatio(1e6, 1e3), 1000)


if __name__ == '__main__':
    unittest.main()
