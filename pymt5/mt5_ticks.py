import json

from .mt5_logger import MT5Logger
from .mt5_connect import MT5Connect
from .mt5_protocol import MT5ReturnCodes


class MT5Ticks(object):

    CMD_TICK_LAST = 'TICK_LAST'

    PARAM_SYMBOL = 'SYMBOL'
    PARAM_TRANS_ID = 'TRANS_ID'

    tick_last_trans_id = 0

    connect = None

    def __init__(self, connect, log_level='ERROR'):
        """
        Init tick module
        :param connect:
        :type connect: MT5Connect
        """
        self.logger = MT5Logger(self.__class__.__name__, level=log_level)
        self.connect = connect

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

