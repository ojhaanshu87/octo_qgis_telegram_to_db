import json
import logging
import sys
import traceback
from os import path
import psycopg2
from PyQt4 import QtSql
from qgis.core import *
from qgis.core import QgsVectorLayer, QgsDataSourceURI,QgsMapLayerRegistry
from config.db_conn import GetDBConnFromConfigFile
from config.command_line import GetArgsFromCommandLine

logging.basicConfig(format='%(asctime)s %(name)-18s %(levelname)-8s \
    %(message)s', level=logging.DEBUG, datefmt='%Y/%m/%d %H:%M:%S ')
LOGGER = logging.getLogger('push data to postgres using QGIS Driver')

class DataOperationQGISToPostgres(self):
	def __init__(self):
		self.get_db_conn = GetDBConnFromConfigFile().get_db_connection()
		self.config_file_path = path.join(path.expanduser('~'), 'octo_qgis_telegram_to_db', 'config', 'config.ini'))
		self.get_arguments = GetArgsFromCommandLine(self.config_file_path).read_arguments()
		self.user = self.get_arguments['user']
		self.password = self.get_arguments['password']
		self.port = self.get_arguments['port']
		self.host = self.get_arguments['host']
		self.database = self.get_argumentsp['dbname']

	def import_from_postgres(self):
		try:
			#QgsDataSourceURI Automatically load the QGIS layer in canvas
			uri = QgsDataSourceURI()
			uri.setConnection(self.host, self.port, self.database, self.user, self.password)
			uri.setDataSource ("UGRoute", "Duct",,"Chamber", "geom")
			vlayer = QgsVectorLayer(uri.uri() ,"Duct", self.user)
		    return vlayer
		except:
			LOGGER.info(str(traceback.format_exception(*sys.exc_info())))

	def read_attribute_from_postgres(self):
		try:
			sql = "(select UGRoute as ug_route_line, Duct as duct_line, Chamber as chamber_point, geom from {0})".format(str(database))
			uri = QgsDataSourceURI()
			uri.setConnection(self.host, self.port, self.database, self.user, self.password)
			uri.setDataSource('public', self.database, 'geom', '4326')
			vlayer = QgsVectorLayer(uri.uri(),self.user)
			QgsMapLayerRegistry.instance().addMapLayer(vlayer)
		except:
			LOGGER.info(str(traceback.format_exception(*sys.exc_info())))

	def insert_into_postgres(self):
		try:
			conn_string = "host=%s dbname=%s user=%s port=%s password=%s" % (self.get_arguments.get('dev', 'host'),
                                                                     self.get_arguments.get('dev', 'dbname'),
                                                                     self.get_arguments.get('dev', 'user'),
                                                                     self.get_arguments.get('dev', 'port'),
                                                                     self.get_arguments.get('dev', 'password'))
			conn = psycopg2.connect(conn_string)
			cursor = conn.cursor()
			cursor.execute("INSERT INTO qgis_data (UGRoute, Duct, Chamber, geom) VALUES (%s, %s, %s, ST_GeomFromText(%s));", (str(pipe['UGRoute']), str(pipe('Duct'))str(pipe['Chamber']), geom.asWkt()))
		except:
			LOGGER.info(str(traceback.format_exception(*sys.exc_info())))


