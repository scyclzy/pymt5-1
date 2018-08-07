import json

from .mt5_exceptions import MT5ResponseError
from .mt5_logger import MT5Logger


class MT5Response(object):

    def __init__(self, header, body, log_level='ERROR'):
        """
        :param header:
        :type header: MT5HeaderProtocol
        :param body:
        :type body: MT5BodyProtocol
        """
        self.logger = MT5Logger(self.__class__.__name__, level=log_level)
        self.__header = header
        self.__body = body

    @property
    def data(self):
        """
        Get response body
        :return:
        :rtype: dict
        :raise: MT5ResponseError
        """

        if not self.__body or self.__body.data is None:
            message = "Get data failed"
            self.logger.error(message)
            raise MT5ResponseError(message)

        return json.loads(self.__body.data)

    def get(self, param):
        """
        Get param
        :param param:
        :return:
        :raise: MT5ResponseError
        """

        if param not in self.__body.options:
            message = "Param not found"
            self.logger.error(message)
            raise MT5ResponseError(message)

        return self.__body.options[param]

    def get_int(self, param):
        """
        Get int param
        :param param:
        :return:
        :raise: MT5ResponseError
        """

        try:
            return int(self.get(param))
        except ValueError:
            message = "Param can't convert to int"
            self.logger.error(message)
            raise MT5ResponseError(message)

