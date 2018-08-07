from .mt5_request import MT5Request


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
        response = self.send(self.CMD_GROUP_GET, {
            self.PARAM_GROUP: group
        })

        return response.data

    def add(self, data):
        """
        Add group
        :param data:
        :return:
        """

        response = self.send(self.CMD_GROUP_ADD, {}, data=data)
        return response.data

    def delete(self):
        pass

    def get_total(self):
        """
        Get total group
        :return:
        """
        response = self.send(self.CMD_GROUP_TOTAL, {})
        return response.data

    def get_next(self):
        pass

    def get_all(self):
        pass
