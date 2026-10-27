import unittest
from decimal import Decimal
from collections import Counter
from Assignment import build_cut_plan

class CuttingTests(unittest.TestCase):
    def test_count_uses_actual_plan_not_length_lower_bound(self):
        plan = build_cut_plan([2.5, 2.5, 2.5])
        self.assertEqual(plan['rod_count'], 3)
        self.assertEqual(plan['waste'], Decimal('4.5'))
        self.assertEqual(plan['revenue'], 1500)

    def test_decimal_cuts_fit_exactly(self):
        plan = build_cut_plan([0.1] * 40)
        self.assertEqual(plan['rod_count'], 1)
        self.assertEqual(plan['waste'], 0)

    def test_input_and_cut_quantities_are_preserved(self):
        values = [1, 3, 2.5, 0.5, 2]
        original = values.copy()
        plan = build_cut_plan(values)
        self.assertEqual(values, original)
        self.assertEqual(Counter(c for rod in plan['rods'] for c in rod), Counter(Decimal(str(v)) for v in values))
        self.assertTrue(all(sum(rod) <= 4 for rod in plan['rods']))
        self.assertEqual(sum(Decimal(str(v)) for v in values) + plan['waste'], 4 * plan['rod_count'])

    def test_empty_order_uses_no_stock(self):
        self.assertEqual(build_cut_plan([]), {'rods': [], 'rod_count': 0, 'revenue': 0, 'waste': 0})

    def test_invalid_values_are_rejected(self):
        for value in [0, -1, 4.01, float('nan'), float('inf'), 'bad', None]:
            with self.subTest(value=value), self.assertRaises(ValueError):
                build_cut_plan([value])

if __name__ == '__main__':
    unittest.main()
