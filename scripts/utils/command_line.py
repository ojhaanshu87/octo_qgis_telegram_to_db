import logging
import sys
import traceback
from os import path 
from optparse import OptionParser

logging.basicConfig(format='%(asctime)s %(name)-18s %(levelname)-8s \
    %(message)s', level=logging.DEBUG, datefmt='%Y/%m/%d %H:%M:%S ')
LOGGER = logging.getLogger('get config file from command line args')

Class GetArgsFromCommandLine(object):
    def __init__(self, config_file_path):
      self.config_file_path = config_file_path

    def read_arguments(self):
      try:
        parser = OptionParser()
        parser.add_option("-c", "--cfile", dest="config_file_path", help="Config File")
        (options, args) = parser.parse_args()
        return [options.config_file_path]
      except:
        LOGGER.info(str(traceback.format_exception(*sys.exc_info())))

