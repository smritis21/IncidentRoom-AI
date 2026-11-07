import unittest
import checkout
class CheckoutTests(unittest.TestCase):
    def test_missing_coupon(self): self.assertEqual(checkout.total(1000,None),1000)
    def test_discount(self): self.assertEqual(checkout.total(1000,'save10'),900)
    def test_unknown_coupon(self): self.assertEqual(checkout.total(1000,'OTHER'),1000)
