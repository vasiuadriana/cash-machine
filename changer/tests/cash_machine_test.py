import unittest

from changer.cash_machine import CashMachine
from changer.cash_machine_exceptions import InvalidCoinTypeException, InvalidNumberOfCoinsException, \
    InvalidBanknoteTypeException


class CashMachineTest(unittest.TestCase):

    def setUp(self):
        self.cash_machine = CashMachine()

    def test_cash_machine_has_no_available_coins_initially(self):
        self.assertDictEqual({}, self.cash_machine.get_available_coins())

    def test_cash_machine_has_no_exchanged_banknotes_initially(self):
        self.assertDictEqual({}, self.cash_machine.get_exchanged_banknotes())

    def test_load_adds_change_into_empty_machine(self):
        self.assertDictEqual({}, self.cash_machine.get_available_coins())
        self.cash_machine.load(50, 0.20)
        self.assertDictEqual({0.20: 50}, self.cash_machine.get_available_coins())

    def test_load_adds_same_type_of_change_into_non_empty_machine(self):
        self.cash_machine.load(50, 0.20)
        self.cash_machine.load(20, 0.20)
        self.assertDictEqual({0.20: 70}, self.cash_machine.get_available_coins())

    def test_load_mixed_type_of_change_into_non_empty_machine(self):
        self.cash_machine.load(50, 0.20)
        self.cash_machine.load(10, 1)
        self.assertDictEqual({0.20: 50, 1: 10}, self.cash_machine.get_available_coins())

    def test_load_type_of_coins_not_accepted_by_the_machine_produces_an_error(self):
        with self.assertRaises(InvalidCoinTypeException):
            self.cash_machine.load(50, 'invalid_coin_type')

    def test_load_invalid_number_of_coins_in_machine_produces_an_error(self):
        with self.assertRaises(InvalidNumberOfCoinsException):
            self.cash_machine.load('invalid_number_of_coins', 1)

    def test_exchange_returns_None_if_not_enough_cash_in_the_machine(self):
        self.assertDictEqual({}, self.cash_machine.get_available_coins())
        self.assertIsNone(self.cash_machine.exchange(20))

        self.cash_machine.load(5, 1)
        self.assertIsNone(self.cash_machine.exchange(20))

        self.cash_machine.load(14, 1)
        self.assertIsNone(self.cash_machine.exchange(20))

    def test_exchange_type_of_banknotes_not_accepted_by_the_machine_produces_an_error(self):
        with self.assertRaises(InvalidBanknoteTypeException):
            self.cash_machine.exchange('invalid_banknote_amount')

    def test_successful_exchange_returns_the_first_possible_coin_combination(self):
        self.cash_machine.load(10, 1)
        self.cash_machine.load(5, 2)
        exchange_result = self.cash_machine.exchange(20)
        self.assertEqual({1: 10, 2: 5}, exchange_result)
        self.cash_machine.load(15, 0.2)
        self.cash_machine.load(11, 0.2)
        self.assertEquals({0.2: 25}, self.cash_machine.exchange(5))

    def test_successfully_exchanged_banknotes_are_stored_in_the_machine(self):
        self.assertEqual({}, self.cash_machine.get_exchanged_banknotes())
        self.cash_machine.load(20, 1)
        self.assertDictEqual({1: 20}, self.cash_machine.exchange(20))
        self.assertEqual({20: 1}, self.cash_machine.get_exchanged_banknotes())

    def test_successfully_exchanged_coins_are_removed_from_the_machine(self):
        self.cash_machine.load(20, 1)
        self.cash_machine.load(5, 2)
        self.assertEqual({1: 20, 2: 5}, self.cash_machine.get_available_coins())
        self.assertDictEqual({1: 20}, self.cash_machine.exchange(20))
        self.assertEqual({2: 5}, self.cash_machine.get_available_coins())

    def test_if_cannot_exchange_no_coins_are_removed_from_machine(self):
        self.assertDictEqual({}, self.cash_machine.get_exchanged_banknotes())
        self.cash_machine.exchange(20)
        self.assertDictEqual({}, self.cash_machine.get_exchanged_banknotes())

    def test_if_cannot_exchange_no_banknotes_are_stored_in_the_machine(self):
        self.cash_machine.load(10, 1)
        self.assertDictEqual({1: 10}, self.cash_machine.get_available_coins())
        self.cash_machine.exchange(20)
        self.assertDictEqual({1: 10}, self.cash_machine.get_available_coins())



if __name__ == '__main__':
    unittest.main()