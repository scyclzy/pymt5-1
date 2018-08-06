from pymt5 import MT5Logger


class MT5Request(object):

    connect = None

    def __init__(self, connect, log_level='ERROR'):
        """
        :param connect:
        :type connect: MT5Connect
        """
        self.logger = MT5Logger(self.__class__.__name__, level=log_level)
        self.connect = connect

