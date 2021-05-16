"""
    @author : Manouchehr Rasouli
    @data   : 19 March 2018
    @since  : 19 March 2018
"""
import logging


def logger(level, message):
    FORMAT = '%(asctime)-15s %(level)s %(data)s %(message)-8s'
    logging.basicConfig(format=FORMAT)
    d = {'level': level, 'data': message}
    logger = logging.getLogger('monitoring_engine')
    logger.warning('%s', ' ', extra=d)
