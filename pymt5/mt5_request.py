from .mt5_exceptions import MT5RequestError
from .mt5_logger import MT5Logger
from .mt5_protocol import MT5ReturnCodes
from .mt5_response import MT5Response


class MT5Request(object):

    connect = None

    def __init__(self, connect, log_level='ERROR'):
        """
        :param connect:
        :type connect: MT5Connect
        """
        self.logger = MT5Logger(self.__class__.__name__, level=log_level)
        self.log_level = log_level
        self.connect = connect

    def send(self, command, params, data=None):
        """
        Send request and validate data
        :param command:
        :param params:
        :param data:
        :return:
        :rtype: MT5Response
        :raise: MT5RequestError
        """

        if not self.connect.send(command, params, data):
            message = "Send request failed"
            self.logger.error(message)
            raise MT5RequestError(message)

        try:
            header, body = self.connect.read()
        except TypeError:
            message = "Read response data failed"
            self.logger.error(message)
            raise MT5RequestError(message)

        if MT5ReturnCodes.PARAM not in body.options:
            message = "Can't read request status"
            self.logger.error(message)
            raise MT5RequestError(message)

        if body.options[MT5ReturnCodes.PARAM] != MT5ReturnCodes.STATUS_DONE:
            message = "Request failed: " + body.options[MT5ReturnCodes.PARAM]
            self.logger.error(message)
            raise MT5RequestError(message)

        return MT5Response(header, body, self.log_level)
