import logging


logger = logging.getLogger()
logger.setLevel(logging.INFO)
hndl = logging.StreamHandler()
formatter = logging.Formatter("     %(levelname)s [%(module)s in %(funcName)s (line:%(lineno)d)]\n%(message)s")
hndl.setFormatter(formatter)
logger.addHandler(hndl)
