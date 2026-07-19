# -*- coding: utf-8 -*-
"""
test_banker.py
---------------
Kiem thu don vi (unit test), doi chieu voi kich ban ground-truth trong
Chuong 1 tai lieu OSG203: 5 tien trinh (P0..P4), 3 loai tai nguyen (A,B,C),
Available = [3, 3, 2].

Chay:
    python3 -m unittest tests/test_banker.py -v
"""
import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "src"))

from banker_algorithm import safety_algorithm, request_algorithm


class TestBankerAlgorithm(unittest.TestCase):

    def setUp(self):
        self.available = [3, 3, 2]
        self.allocation = [
            [0, 1, 0],   # P0
            [2, 0, 0],   # P1
            [3, 0, 2],   # P2
            [2, 1, 1],   # P3
            [0, 0, 2],   # P4
        ]
        self.need = [
            [7, 4, 3],   # P0
            [1, 2, 2],   # P1
            [6, 0, 0],   # P2
            [0, 1, 1],   # P3
            [4, 3, 1],   # P4
        ]

    def test_system_is_safe(self):
        is_safe, sequence, _ = safety_algorithm(self.available, self.allocation, self.need)
        self.assertTrue(is_safe, "He thong phai duoc xac dinh la An toan theo tai lieu Chuong 1")
        self.assertEqual(sorted(sequence), [0, 1, 2, 3, 4], "Moi tien trinh phai xuat hien dung 1 lan trong sequence")

    def test_p1_is_first_in_sequence(self):
        # Voi Available ban dau = [3,3,2]: P0 khong thoa (Need=[7,4,3]),
        # nhung P1 thoa (Need=[1,2,2]) -> P1 phai la tien trinh dau tien
        # duoc chon khi duyet tu chi so nho nhat.
        _, sequence, _ = safety_algorithm(self.available, self.allocation, self.need)
        self.assertEqual(sequence[0], 1)

    def test_unsafe_when_no_resource_available(self):
        is_safe, sequence, _ = safety_algorithm([0, 0, 0], self.allocation, self.need)
        self.assertFalse(is_safe)
        self.assertEqual(sequence, [])

    def test_request_granted_when_still_safe(self):
        # P1 xin them [1,0,0]: Need[P1]=[1,2,2] -> con du (1<=1), Available=[3,3,2] -> du (1<=3)
        granted, new_state, _ = request_algorithm(1, [1, 0, 0], self.available, self.allocation, self.need)
        self.assertTrue(granted)
        self.assertIsNotNone(new_state)

    def test_request_denied_when_exceeds_need(self):
        # P0 xin [8,0,0] nhung Need[P0]=[7,4,3] -> 8 > 7 -> phai bi tu choi ngay
        granted, new_state, reason = request_algorithm(0, [8, 0, 0], self.available, self.allocation, self.need)
        self.assertFalse(granted)
        self.assertIsNone(new_state)


if __name__ == "__main__":
    unittest.main(verbosity=2)
