import json

from .mt5_request import MT5Request
from .mt5_protocol import MT5ReturnCodes


class MT5Common(MT5Request):

    CMD_COMMON_GET = 'COMMON_GET'

    def get(self):
        """
        Get common information
        :return:
        """

        if not self.connect.send(self.CMD_COMMON_GET, {}):
            self.logger.error("Get common information failed")
            return False

        try:
            header, body = self.connect.read()
        except TypeError:
            self.logger.error("Read common information failed")
            return False

        if MT5ReturnCodes.PARAM not in body.options \
                or body.data is None \
                or body.options[MT5ReturnCodes.PARAM] != MT5ReturnCodes.STATUS_DONE:
            self.logger.error("Get common information failed")
            return False

        return json.loads(body.data)
