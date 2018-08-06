import json

from .mt5_request import MT5Request
from .mt5_protocol import MT5ReturnCodes


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

        if not self.connect.send(self.CMD_TICK_LAST, {
            self.PARAM_SYMBOL: symbol,
            self.PARAM_TRANS_ID: self.tick_last_trans_id
        }):
            self.logger.error("Get tick last failed")
            return False

        try:
            header, body = self.connect.read()
        except TypeError:
            self.logger.error("Read tick last data failed")
            return False

        if MT5ReturnCodes.PARAM not in body.options \
                or body.data is None \
                or body.options[MT5ReturnCodes.PARAM] != MT5ReturnCodes.STATUS_DONE:
            self.logger.error("Get tick last failed")
            return False

        if self.PARAM_TRANS_ID in body.options:
            self.tick_last_trans_id = body.options[self.PARAM_TRANS_ID]

        return json.loads(body.data)

    def tick_stat(self, symbol):
        """
        Get tick last stat
        :param symbol:
        :return:
        """

        if not self.connect.send(self.CMD_TICK_STAT, {
            self.PARAM_SYMBOL: symbol,
            self.PARAM_TRANS_ID: self.tick_stat_trans_id
        }):
            self.logger.error("Get tick stat failed")
            return False

        try:
            header, body = self.connect.read()
        except TypeError:
            self.logger.error("Read tick stat data failed")
            return False

        if MT5ReturnCodes.PARAM not in body.options \
                or body.data is None \
                or body.options[MT5ReturnCodes.PARAM] != MT5ReturnCodes.STATUS_DONE:
            self.logger.error("Get tick stat failed")
            return False

        if self.PARAM_TRANS_ID in body.options:
            self.tick_stat_trans_id = body.options[self.PARAM_TRANS_ID]

        return json.loads(body.data)
