import logging

class Logging():
    """
    Our logging class
    """
    def __init__(self):
        self.log = logging.getLogger('zabbix')

    def setup(self,file_name='zabbix.log',console_level="CRITICAL",file_level='WARNING'):
        """
        Creates a logger object

        @type file_name: str
        @param warn: File name to output logs to

        @type console_level: str
        @param console_level: Level for console output

        @type file_level: str
        @param file_level: Level for console output
        """
        self.log.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(asctime)s %(name)-12s %(levelname)-8s %(message)s')


        self.fh = logging.FileHandler(file_name)
        self.fh.setFormatter(formatter)
        self.fh.setLevel(self.getLevel(file_level))
        self.log.addHandler(self.fh)

        self.ch = logging.StreamHandler()
        self.ch.setFormatter(formatter)
        self.ch.setLevel(self.getLevel(console_level))
        self.log.addHandler(self.ch)

    def getLevel(self,level):
        """
        Return logging.LEVEL

        @type level: str
        @param level: Logging level as string
        """
        if level == 'DEBUG':
            return logging.DEBUG
        elif level == 'INFO':
            return logging.INFO
        elif level == 'WARNING':
            return logging.WARNING
        elif level == 'ERROR':
            return logging.ERROR
        elif level == 'CRITICAL':
            return logging.CRITICAL

def setup_logging(console_level="WARNING",file_level="WARNING",file_name="zabbix.log"):
    _logger = Logging()
    _logger.setup(console_level=console_level,file_level=file_level,file_name=file_name)
    return Logging().log
