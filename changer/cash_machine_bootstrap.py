from changer.cash_machine_exceptions import CashMachineException
from changer.cash_machine import CashMachine
from changer.cash_machine_user_messages import INVALID_OPERATION, INVALID_OPERATION_INPUT, AMOUNT_NOT_SUPPORTED


class CashMachineBootstrap:
    def __init__(self):
        self._cash_machine_operator = CashMachine()

    def bootstrap_machine_from_file(self, file_handler):
        output_lines = []
        for command in file_handler:
            validation_output = self._validate_command(command.split())
            if validation_output:
                return validation_output
            try:
                command_output = self._format_command_output(command.split())
            except CashMachineException:
                return AMOUNT_NOT_SUPPORTED
            output_lines.extend([command.strip(), command_output, self._format_available_cash_output()])
        return '\n'.join(list(filter(None, output_lines)))

    def _validate_command(self, data):
        command = data[1]
        if not self._cash_machine_operator.is_supported(command):
            return INVALID_OPERATION
        if len(data) - 2 != self._number_of_parameters_required(command):
            return INVALID_OPERATION_INPUT

    def _format_command_output(self, data):
        if data[1] == 'LOAD':
            self._cash_machine_operator.load(data[2], data[3])
        if data[1] == 'EXCHANGE':
            result = self._cash_machine_operator.exchange(data[2])
            if not result:
                return '< CANNOT EXCHANGE'
            return '< ' + ', '.join(self._format_items(result))

    def _format_available_cash_output(self):
        output_items = self._format_items(self._cash_machine_operator.get_available_coins())
        output_items.extend(self._format_items(self._cash_machine_operator.get_exchanged_banknotes()))
        return "= " + ', '.join(output_items)

    @staticmethod
    def _format_items(item_dict):
        formatted_items = []
        for key, value in item_dict.items():
            formatted_items.append('{0:d} {1:g}£'.format(value, key))
        return formatted_items

    @staticmethod
    def _number_of_parameters_required(command):
        parameter_number = {'LOAD': 2, 'EXCHANGE': 1}
        return parameter_number[command]
