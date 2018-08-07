from .mt5_request import MT5Request


class MT5Common(MT5Request):

    CMD_COMMON_GET = 'COMMON_GET'

    def get(self):
        """
        Get common information
        :return:
        """

        response = self.send(self.CMD_COMMON_GET, {})
        return response.data
