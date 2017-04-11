class CashMachineException(Exception):
    pass


class InvalidCoinTypeException(CashMachineException):
    pass


class InvalidNumberOfCoinsException(CashMachineException):
    pass


class InvalidBanknoteTypeException(CashMachineException):
    pass
