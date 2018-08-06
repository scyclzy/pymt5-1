import json

from .mt5_request import MT5Request
from .mt5_protocol import MT5ReturnCodes


class MT5Group(MT5Request):

    CMD_GROUP_GET = 'GROUP_GET'
    CMD_GROUP_ADD = 'GROUP_ADD'
    CMD_GROUP_DELETE = 'GROUP_DELETE'
    CMD_GROUP_TOTAL = 'GROUP_TOTAL'
    CMD_GROUP_NEXT = 'GROUP_NEXT'

    PARAM_GROUP = 'GROUP'

    def get(self, group):
        """
        Get group
        :return:
        """
        if not self.connect.send(self.CMD_GROUP_GET, {
            self.PARAM_GROUP: group
        }):
            self.logger.error("Get group failed")
            return False

        try:
            header, body = self.connect.read()
        except TypeError:
            self.logger.error("Read group failed")
            return False

        if MT5ReturnCodes.PARAM not in body.options \
                or body.data is None \
                or body.options[MT5ReturnCodes.PARAM] != MT5ReturnCodes.STATUS_DONE:
            self.logger.error("Get group failed")
            return False

        return json.loads(body.data)

    def add(self, data):
        """
        Add group
        :param data:
        :return:
        """
        if not self.connect.send(self.CMD_GROUP_ADD, {}, data=data):
            self.logger.error("Add group failed")
            return False

        try:
            header, body = self.connect.read()
        except TypeError:
            self.logger.error("Add group failed")
            return False

        if MT5ReturnCodes.PARAM not in body.options \
                or body.data is None \
                or body.options[MT5ReturnCodes.PARAM] != MT5ReturnCodes.STATUS_DONE:
            self.logger.error("Add group failed")
            return False

        return json.loads(body.data)

    def delete(self):
        pass

    def get_total(self):
        """
        Get total group
        :return:
        """
        if not self.connect.send(self.CMD_GROUP_TOTAL, {}):
            self.logger.error("Get group total failed")
            return False

        try:
            header, body = self.connect.read()
        except TypeError:
            self.logger.error("Get group total failed")
            return False

        if MT5ReturnCodes.PARAM not in body.options \
                or body.data is None \
                or body.options[MT5ReturnCodes.PARAM] != MT5ReturnCodes.STATUS_DONE:
            self.logger.error("Get group failed")
            return False

        return json.loads(body.data)

    def get_next(self):
        pass

    def get_all(self):
        pass
