import math
from collections import OrderedDict

from changer.cash_machine_exceptions import InvalidCoinTypeException, InvalidNumberOfCoinsException, \
    InvalidBanknoteTypeException


class CashMachine:

    SUPPORTED_OPERATIONS = ('LOAD', 'EXCHANGE')
    ACCEPTED_COINS = (0.20, 0.50, 1, 2)
    ACCEPTED_BANKNOTES = (5, 10, 20)

    def __init__(self):
        self._available_coins = OrderedDict()
        self._exchanged_banknotes = OrderedDict()

    def get_available_coins(self):
        return self._available_coins

    def get_exchanged_banknotes(self):
        return OrderedDict(sorted(self._exchanged_banknotes.items(), key=lambda t: t[0]))

    def load(self, number_of_coins, type_of_coins):
        number_of_coins, type_of_coins = self._validate_load_input(number_of_coins, type_of_coins)
        self._increment_available_coins(type_of_coins, number_of_coins)

    def exchange(self, banknote_amount):
        exchange_result = {}
        banknote_amount = self._validate_exchange_input(banknote_amount)
        try:
            first_combination = self._change(banknote_amount, list(self._available_coins.keys()), []).__next__()
        except StopIteration:
            return
        for coin in set(first_combination):
            number_of_coins_used = first_combination.count(coin)
            exchange_result[coin] = number_of_coins_used
            self._decrement_coins_used(coin, number_of_coins_used)
        self._increment_exchanged_banknotes(banknote_amount)
        return exchange_result

    def is_supported(self, operation):
        return operation in self.SUPPORTED_OPERATIONS

    def _change(self, banknote_amount, available_coins, used_coins):
        if not available_coins:
            pass
        elif used_coins.count(available_coins[0]) > self._available_coins[available_coins[0]]:
            pass
        elif math.fsum(used_coins) == banknote_amount:
            yield used_coins
        elif sum(used_coins) > banknote_amount:
            pass
        else:
            for c in self._change(banknote_amount, available_coins[:], used_coins + [available_coins[0]]):
                yield c
            for c in self._change(banknote_amount, available_coins[1:], used_coins):
                yield c

    def _increment_available_coins(self, type_of_coins, number_of_coins):
        self._increment_cash_amount(self._available_coins, type_of_coins, number_of_coins)

    def _increment_exchanged_banknotes(self, banknote):
        self._increment_cash_amount(self._exchanged_banknotes, banknote, 1)

    def _decrement_coins_used(self, coin, number_of_coins_used):
        self._available_coins[coin] -= number_of_coins_used
        if self._available_coins[coin] == 0:
            del self._available_coins[coin]

    def _validate_load_input(self, number_of_coins, type_of_coins):
        try:
            number_of_coins = int(number_of_coins)
        except ValueError:
            raise InvalidNumberOfCoinsException("Coin number is incorrect")
        try:
            type_of_coins = float(type_of_coins)
        except ValueError:
            raise InvalidCoinTypeException("Coin type not accepted")
        if type_of_coins not in self.ACCEPTED_COINS:
            raise InvalidCoinTypeException("Coin type not accepted")
        return number_of_coins, type_of_coins

    def _validate_exchange_input(self, banknote_amount):
        try:
            banknote_amount = int(banknote_amount)
        except ValueError:
            raise InvalidBanknoteTypeException("Banknote amount is not accepted")
        if banknote_amount not in self.ACCEPTED_BANKNOTES:
            raise InvalidBanknoteTypeException('Banknote amount not accepted')
        return banknote_amount

    @staticmethod
    def _increment_cash_amount(cash_store, cash_type, cash_amount):
        try:
            cash_store[cash_type] += cash_amount
        except KeyError:
            cash_store[cash_type] = cash_amount
