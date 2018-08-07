from hashlib import md5

from .mt5_crypt import MT5Crypt
from .mt5_protocol import VERSION
from .mt5_request import MT5Request
from .mt5_utils import MT5Utils


class MT5Auth(MT5Request):

    CMD_AUTH_START = 'AUTH_START'
    CMD_AUTH_ANSWER = 'AUTH_ANSWER'

    PARAM_AGENT = 'AGENT'
    PARAM_VERSION = 'VERSION'
    PARAM_TYPE = 'TYPE'
    PARAM_LOGIN = 'LOGIN'
    PARAM_SRV_RAND = 'SRV_RAND'
    PARAM_SRV_RAND_ANSWER = 'SRV_RAND_ANSWER'
    PARAM_CLI_RAND = 'CLI_RAND'
    PARAM_CLI_RAND_ANSWER = 'CLI_RAND_ANSWER'
    PARAM_CRYPT_RAND = 'CRYPT_RAND'
    PARAM_CRYPT_METHOD = 'CRYPT_METHOD'

    VAL_CRYPT_NONE = "NONE"
    VAL_CRYPT_AES256OFB = "AES256OFB"

    connect = None
    agent = None

    def __init__(self, connect, log_level='ERROR', agent='PYMT5'):
        """
        Init
        :param connect:
        :type connect: MT5Connect
        :param agent:
        :type agent: str
        """
        super().__init__(connect, log_level)
        self.agent = agent

    def auth(self, login, password):
        """
        Auth to MT5 server
        :param login:
        :type login: str
        :param password:
        :type password: str
        :return:
        :rtype: bool
        """

        """
        Auth start
        """
        response = self.send(self.CMD_AUTH_START, {
                self.PARAM_VERSION: VERSION,
                self.PARAM_AGENT: self.agent,
                self.PARAM_LOGIN: login,
                self.PARAM_TYPE: 'MANAGER',
                self.PARAM_CRYPT_METHOD: self.VAL_CRYPT_AES256OFB if self.connect.is_crypt else self.VAL_CRYPT_NONE
            })

        """
        Auth answer
        """
        cli_rand = MT5Utils.get_random_hex(16)

        pass_hash = MT5Utils.get_hash_from_password(password)

        srv_rand_answ = md5(
            bytes.fromhex(pass_hash) +
            bytes.fromhex(response.get_int(self.PARAM_SRV_RAND))).hexdigest()

        response = self.send(self.CMD_AUTH_ANSWER, {
                self.PARAM_SRV_RAND_ANSWER: srv_rand_answ,
                self.PARAM_CLI_RAND: cli_rand
            })

        """
        Check auth user answer
        """

        cli_rand_answ = md5(
            bytes.fromhex(pass_hash) +
            bytes.fromhex(cli_rand)).hexdigest()

        if response.get(self.PARAM_CLI_RAND_ANSWER) != cli_rand_answ:
            self.logger.error("Server return broken password hash")
            return False

        self.connect.crypt = MT5Crypt(response.get(self.PARAM_CRYPT_RAND), pass_hash)

        return True


