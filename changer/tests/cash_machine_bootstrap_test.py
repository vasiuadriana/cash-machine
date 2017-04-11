import os
import unittest
from unittest.mock import patch, Mock

from changer.cash_machine_bootstrap import CashMachineBootstrap
from changer.cash_machine_exceptions import InvalidBanknoteTypeException, InvalidCoinTypeException
from changer.cash_machine_user_messages import INVALID_OPERATION, INVALID_OPERATION_INPUT, AMOUNT_NOT_SUPPORTED

TEST_DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data')


class CashMachineBootstrapTest(unittest.TestCase):

    def setUp(self):
        self.bootstrap = CashMachineBootstrap()

    def test_bootstrap_returns_invalid_operation_message_if_commands_provided_are_not_supported(self):
        invalid_input_file = os.path.join(TEST_DATA_DIR, 'invalid_operation.txt')
        with open(invalid_input_file, 'r') as input_file_handler:
            self.assertEqual(INVALID_OPERATION, self.bootstrap.bootstrap_machine_from_file(input_file_handler))

    def test_bootstrap_returns_invalid_operation_input_if_input_for_load_is_invalid(self):
        invalid_input_file = os.path.join(TEST_DATA_DIR, 'invalid_load_operation_input.txt')
        with open(invalid_input_file, 'r') as input_file_handler:
            self.assertEqual(INVALID_OPERATION_INPUT, self.bootstrap.bootstrap_machine_from_file(input_file_handler))

    def test_bootstrap_returns_invalid_operation_input_if_input_for_exchange_is_invalid(self):
        invalid_input_file = os.path.join(TEST_DATA_DIR, 'invalid_exchange_operation_input.txt')
        with open(invalid_input_file, 'r') as input_file_handler:
            self.assertEqual(INVALID_OPERATION_INPUT, self.bootstrap.bootstrap_machine_from_file(input_file_handler))

    @patch('changer.cash_machine.CashMachine.exchange')
    def test_bootstrap_returns_amount_not_accepted_if_banknote_type_is_not_accepted_by_machine(self, mock_load):
        invalid_input_file = os.path.join(TEST_DATA_DIR, 'not_accepted_banknote_amount.txt')
        with open(invalid_input_file, 'r') as input_file_handler:
            mock_load.side_effect = InvalidBanknoteTypeException("Banknote amount is not accepted")
            self.assertEqual(AMOUNT_NOT_SUPPORTED, self.bootstrap.bootstrap_machine_from_file(input_file_handler))

    @patch('changer.cash_machine.CashMachine.load')
    def test_bootstrap_returns_amount_not_accepted_if_coin_type_is_not_accepted_by_machine(self, mock_load):
        invalid_input_file = os.path.join(TEST_DATA_DIR, 'not_accepted_coin_type.txt')
        with open(invalid_input_file, 'r') as input_file_handler:
            mock_load.side_effect = InvalidCoinTypeException("Coin type not accepted")
            self.assertEqual(AMOUNT_NOT_SUPPORTED,self.bootstrap.bootstrap_machine_from_file(input_file_handler))

    def test_bootstrap_outputs_back_the_command_and_after_each_command_the_coins_and_banknotes_in_machine(self):
        input_file = os.path.join(TEST_DATA_DIR, 'valid_input.txt')
        with open(input_file, 'r') as input_file_handler:
            actual_result = self.bootstrap.bootstrap_machine_from_file(input_file_handler)
            expected_lines = [
                '> LOAD 10 1',
                '= 10 1£',
                '> LOAD 20 2',
                '= 10 1£, 20 2£',
                '> EXCHANGE 20',
                '< 10 1£, 5 2£',
                '= 15 2£, 1 20£',
                '> EXCHANGE 20',
                '< 10 2£',
                '= 5 2£, 2 20£',
                '> EXCHANGE 20',
                '< CANNOT EXCHANGE',
                '= 5 2£, 2 20£',
                '> EXCHANGE 10',
                '< 5 2£',
                '= 1 10£, 2 20£'
            ]
            expected_result = '\n'.join(expected_lines)
            self.assertMultiLineEqual(expected_result, actual_result)

if __name__ == '__main__':
    unittest.main()