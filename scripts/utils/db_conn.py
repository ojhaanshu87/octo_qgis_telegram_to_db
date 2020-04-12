import logging
import sys
import traceback
from psycopg2 import connect

logging.basicConfig(format='%(asctime)s %(name)-18s %(levelname)-8s \
    %(message)s', level=logging.DEBUG, datefmt='%Y/%m/%d %H:%M:%S ')
LOGGER = logging.getLogger('get DB connection from postgres')

class GetDBConnFromConfigFile(object):
	def __init__(self):
		self.data = none

	def get_db_connection(self, env, config):
		try:
			conn_string = "host=%s dbname=%s user=%s port=%s password=%s" % (config.get(env, 'host'),
                                                                     config.get(env, 'dbname'),
                                                                     config.get(env, 'user'),
                                                                     config.get(env, 'port'),
                                                                     config.get(env, 'password'))
			return connect(conn_string)
		except:
			LOGGER.info(str(traceback.format_exception(*sys.exc_info())))