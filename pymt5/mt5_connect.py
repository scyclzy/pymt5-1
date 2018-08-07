
import socket

from pymt5 import MT5Logger, MT5HeaderProtocol, MT5BodyProtocol, MT5ConnectionError, MT5SocketError


class MT5Connect(object):

    CMD_WEBAPI = b'MT5WEBAPI'
    CMD_QUIT = b'QUIT'

    HEADER_LENGTH = 9
    MAX_CLIENT_COMMAND = 16383

    port = None
    host = None
    timeout = None
    is_crypt = None

    crypt = None

    number_command = 0

    __socket = None

    def __init__(self, host, port, timeout=5, is_crypt=False, log_level='ERROR'):
        """
        Connection init
        :param host: MT5 server host
        :type host: str
        :param port: MT5 server port
        :type port: int
        :param timeout: Connection timeout
        :type timeout: int
        :param is_crypt:
        :type is_crypt: bool
        """

        self.logger = MT5Logger(self.__class__.__name__, level=log_level)

        self.host = host
        self.port = port
        self.timeout = timeout
        self.is_crypt = is_crypt

    def connect(self):
        """
        Connect to MT5 server
        :return: Connect status
        """

        try:
            self.__socket = socket.create_connection(address=(self.host, self.port))
        except socket.error as e:
            message = "Can't not connect to MT5 server"
            self.logger.error(str(e))
            self.logger.error(message)
            raise MT5ConnectionError(message)
        else:
            self.logger.debug("Successful connection")

        self.__socket.setblocking(True)

        """
        Set WebAPI Mode
        """
        try:
            self.__socket.send(self.CMD_WEBAPI)
        except socket.error as e:
            message = "Can't not set WebAPI mode"
            self.logger.error(str(e))
            self.logger.error(message)
            raise MT5SocketError(message)

        return True

    def send(self, command, options, data=None):
        """
        Send command to MT5 server
        :param command:
        :type command: str
        :param options:
        :type options: dict(str, str)
        :param data:
        :type data:
        :return:
        :rtype: bool
        """

        if not isinstance(self.__socket, socket.socket):
            message = "Connection is broken. Data can't be sent"
            self.logger.error(message)
            raise MT5SocketError(message)

        self.number_command = \
            (self.number_command + 1) if self.number_command < self.MAX_CLIENT_COMMAND else 0

        body = MT5BodyProtocol(
            command=command,
            options=options,
            data=data
        )

        body_data = self.crypt.crypt_packet(body.bytes) \
            if self.is_crypt and self.crypt else body.bytes

        header_data = MT5HeaderProtocol(
            body_size=len(body_data),
            number_command=self.number_command
        ).bytes

        self.logger.debug("Send data: " + str(body).replace('\r\n', ' '))

        try:
            self.__socket.send(header_data)
            self.__socket.sendall(body_data)
        except socket.error as e:
            message = "Data can't be sent"
            self.logger.error(str(e))
            self.logger.error(message)
            raise MT5SocketError(message)

        return True

    def read(self):
        """
        Read data from MT5 server
        :return:
        :rtype: tuple(MTHeaderProtocol, MTBodyProtocol) or None
        """

        if not isinstance(self.__socket, socket.socket):
            message = "Connection is broken. Data can't be read"
            self.logger.error(message)
            raise MT5SocketError(message)

        while True:

            try:
                header = self.__read_header()
            except socket.error as e:
                message = "Data can't be read"
                self.logger.error(str(e))
                self.logger.error(message)
                raise MT5SocketError(message)

            if not isinstance(header, MT5HeaderProtocol):
                self.logger.error("Incorrect header")
                return None

            try:
                body = self.__read_body(header.body_size)
            except socket.error as e:
                message = "Data can't be read"
                self.logger.error(str(e))
                self.logger.error(message)
                raise MT5SocketError(message)

            if not isinstance(body, MT5BodyProtocol):
                self.logger.error("Incorrect body")
                return None

            if header.number_command != self.number_command:

                if header.body_size != 0:
                    self.logger.debug(
                        "Number of packet incorrect. Need: %d, but get %d" %
                        (self.number_command, header.number_command, ))
                else:
                    self.logger.debug("PING Packet")

                continue

            break

        self.logger.debug("Read data: " + str(body).replace('\r\n', ' '))

        return header, body

    def __read_header(self):
        """
        Read header package
        :return:
        :rtype: MT5HeaderProtocol or bytes
        """
        data = self.__socket.recv(MT5HeaderProtocol.HEADER_LENGTH)
        return MT5HeaderProtocol.parse(data) or data

    def __read_body(self, size):
        """
        Read body packages
        :param size:
        :return:
        :rtype: MT5BodyProtocol or bytes
        """

        buffer = b''

        while len(buffer) < size:
            packet = self.__socket.recv(size - len(buffer))

            if not packet:
                return None

            buffer += packet

        return MT5BodyProtocol.parse(self.crypt.decrypt_packet(buffer)) \
            if self.is_crypt and self.crypt else MT5BodyProtocol.parse(buffer)

    def disconnect(self):
        """
        Disconnect
        :return:
        """

        try:
            self.__socket.send(self.CMD_QUIT)
            self.__socket.close()
        except:
            pass

        self.logger.debug("Connection closed")

