import logging
from socket import gethostname

# setup `logging` module
logger = logging.getLogger('awaymo')
logger.setLevel(logging.INFO)
FORMAT = "{} [%(filename)s:%(lineno)s - %(funcName)s()] %(message)s".format(gethostname())
formatter = logging.Formatter(FORMAT)
ch = logging.StreamHandler()
logger.addHandler(ch)