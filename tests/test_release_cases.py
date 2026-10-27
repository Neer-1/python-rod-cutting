import itertools
import subprocess
import sys
import unittest
from pathlib import Path
from decimal import Decimal
from Assignment import build_cut_plan


def optimal_bins(values, capacity=10):
    # Exhaustive assignment to bins for small integer fixtures, independent of greedy packing.
    best = len(values)
    def search(index, loads):
        nonlocal best
        if index == len(values):
            best = min(best, len(loads))
            return
        if len(loads) >= best:
            return
        value = values[index]
        seen = set()
        for i, load in enumerate(loads):
            if load not in seen and load + value <= capacity:
                seen.add(load)
                loads[i] += value
                search(index + 1, loads)
                loads[i] -= value
        search(index + 1, loads + [value])
    search(0, [])
    return best


class ReleaseCases(unittest.TestCase):
    def test_known_greedy_optimality_gap_is_explicit(self):
        values = [6, 5, 3, 2, 2, 2]
        plan = build_cut_plan([Decimal(v) * Decimal('0.4') for v in values])
        self.assertEqual(plan['rod_count'], 3)
        self.assertEqual(optimal_bins(values), 2)

    def test_small_exhaustive_feasibility_benchmark(self):
        # 923 multisets: sizes 1..6 from six integer lengths.
        count = 0
        for size in range(1, 7):
            for values in itertools.combinations_with_replacement([1, 2, 3, 5, 6, 9], size):
                plan = build_cut_plan([Decimal(v) * Decimal('0.4') for v in values])
                self.assertGreaterEqual(plan['rod_count'], optimal_bins(values))
                self.assertEqual(sum(len(rod) for rod in plan['rods']), len(values))
                self.assertTrue(all(sum(rod) <= 4 for rod in plan['rods']))
                count += 1
        self.assertEqual(count, 923)

    def run_cli(self, data):
        result = subprocess.run([sys.executable, '-B', 'Assignment.py'], input=data, text=True,
                                capture_output=True, cwd=Path(__file__).resolve().parents[1], timeout=5)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertNotIn('Traceback', result.stderr)
        return result.stdout

    def test_eof_at_all_input_stages(self):
        for data in ['', '1\n', '2\n1\n']:
            with self.subTest(data=data):
                self.assertIn('Input ended', self.run_cli(data))

    def test_invalid_inputs_and_clean_exit(self):
        output = self.run_cli('bad\n-1\n1\nNaN\nInfinity\n0\n5\nwrong\n4\n0\n')
        self.assertIn('Total number of 4-meter rods used: 1', output)
        self.assertIn('Waste generated: 0.00', output)

    def test_cli_does_not_round_input_through_float(self):
        output = self.run_cli('2\n2.0000000000000001\n2.0000000000000001\n0\n')
        self.assertIn('Total number of 4-meter rods used: 2', output)
