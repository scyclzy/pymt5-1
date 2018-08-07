from .mt5_request import MT5Request


class MT5Ticks(MT5Request):

    CMD_TICK_LAST = 'TICK_LAST'
    CMD_TICK_STAT = 'TICK_STAT'

    PARAM_SYMBOL = 'SYMBOL'
    PARAM_TRANS_ID = 'TRANS_ID'

    tick_last_trans_id = 0
    tick_stat_trans_id = 0

    def tick_last(self, symbol):
        """
        Get tick last
        :param symbol:
        :type symbol: str
        :return:
        """

        response = self.send(self.CMD_TICK_LAST, {
            self.PARAM_SYMBOL: symbol,
            self.PARAM_TRANS_ID: self.tick_last_trans_id
        })

        self.tick_last_trans_id = response.get(self.PARAM_TRANS_ID)
        return response.data

    def tick_stat(self, symbol):
        """
        Get tick last stat
        :param symbol:
        :return:
        """

        response = self.send(self.CMD_TICK_STAT, {
            self.PARAM_SYMBOL: symbol,
            self.PARAM_TRANS_ID: self.tick_stat_trans_id
        })

        self.tick_stat_trans_id = response.get(self.PARAM_TRANS_ID)
        return response.data
