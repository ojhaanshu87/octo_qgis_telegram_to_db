import json
import logging
import sys
import traceback
from os import path
import psycopg2
import qgis.utils
from PyQt4 import QtSql
from PyQt4.QtCore import *
from qgis.core import QgsProject
from qgis.core import *
from qgis.core import QgsVectorLayer, QgsDataSourceURI,QgsMapLayerRegistry, QgsFeature
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
		self.uri = QgsDataSourceURI()

	def import_from_postgres(self):
		try:
			#QgsDataSourceURI Automatically load the QGIS layer in canvas
			self.uri = QgsDataSourceURI()
			self.uri.setConnection(self.host, self.port, self.database, self.user, self.password)
			self.uri.setDataSource ("UGRoute", "Duct",,"Chamber", "geom")
			vlayer = QgsVectorLayer(self.uri.uri() ,"Duct", self.user)
		    return vlayer
		except:
			LOGGER.info(str(traceback.format_exception(*sys.exc_info())))

	def read_attribute_from_postgres(self):
		try:
			sql = "(select UGRoute as ug_route_line, Duct as duct_line, Chamber as chamber_point, geom from {0})".format(str(database))
			self.uri.setConnection(self.host, self.port, self.database, self.user, self.password)
			self.uri.setDataSource('public', self.database, 'geom', '4326')
			vlayer = QgsVectorLayer(self.uri.uri(),self.user)
			QgsMapLayerRegistry.instance().addMapLayer(vlayer)
		except:
			LOGGER.info(str(traceback.format_exception(*sys.exc_info())))

	def create_and_write_data_in_qgis_window(self):
		try:
			self.read_attribute_from_postgres()
			# load provider
			QgsApplication.initQgis()
			qgis.utils.iface
			# set active layer
			clayer = qgis.utils.iface.activeLayer()
			provider = clayer.dataProvider()
			# start editing mode
			clayer.startEditing()
			# add new fields
			caps = provider.capabilities()
			if caps & QgsVectorDataProvider.AddAttributes:
    			res = provider.addAttributes([QgsField("ug_route_line", QVariant.Int), QgsField("duct_line", QVariant.Int)])
    		self.insert_into_postgres()
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


