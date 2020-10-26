import logging
import sys

class Logger:

    def __init__(self,filename):
        
        self.logger = logging.getLogger()
        self.logger.setLevel(logging.INFO)
        self.filename = filename

    def start(self):

        self.file_handler = logging.FileHandler(self.filename)
        self.stream_handler = logging.StreamHandler(sys.stdout)
        self.logger.addHandler(self.file_handler)
        self.logger.addHandler(self.stream_handler)

        return self.logger

    def close_logging(self):

        logging.shutdown()









