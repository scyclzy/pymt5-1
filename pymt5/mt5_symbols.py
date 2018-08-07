import json

from pymt5 import MT5Request


class MT5Symbols(MT5Request):

    CMD_SYMBOL_GET = 'SYMBOL_GET'
    CMD_SYMBOL_GET_GROUP = 'SYMBOL_GET_GROUP'
    CMD_SYMBOL_ADD = 'SYMBOL_ADD'
    CMD_SYMBOL_NEXT = 'SYMBOL_NEXT'
    CMD_SYMBOL_TOTAL = 'SYMBOL_TOTAL'

    PARAM_SYMBOL = 'SYMBOL'
    PARAM_GROUP = 'GROUP'
    PARAM_INDEX = 'INDEX'
    PARAM_TOTAL = 'TOTAL'

    def get(self, symbol):
        """
        Get symbol by name
        :param symbol:
        :return:
        """
        response = self.send(self.CMD_SYMBOL_GET, {
            self.PARAM_SYMBOL: symbol
        })

        return response.data

    def get_group(self, symbol, group):
        """
        Get symbol by name and group
        :param symbol:
        :param group:
        :return:
        """
        response = self.send(self.CMD_SYMBOL_GET_GROUP, {
            self.PARAM_SYMBOL: symbol,
            self.PARAM_GROUP: group
        })

        return response.data

    def get_next(self, index=0):
        """
        Get symbol by index
        :param index:
        :type index: int
        :return:
        """

        response = self.send(self.CMD_SYMBOL_NEXT, {
            self.PARAM_INDEX: index
        })

        return response.data

    def add(self, data):
        """
        Set symbol data
        :param data:
        :return:
        """

        response = self.send(self.CMD_SYMBOL_ADD, {}, json.dumps(data))
        return response.data

    def get_total(self):
        """
        Get total count symbols
        :return:
        """

        response = self.send(self.CMD_SYMBOL_TOTAL, {})
        return response.get_int(self.PARAM_TOTAL)

    def get_all(self):
        """
        Get all symbols
        :return:
        """

        result = []

        count = self.get_total()

        for index in range(0, count):
            symbol = self.get_next(index)
            result.append(symbol)

        return result
