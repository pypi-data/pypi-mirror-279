# import logging
# from logging.handlers import RotatingFileHandler
#
# def setup_logging():
#     logger = logging.getLogger()
#     logger.setLevel(logging.INFO)
#
#     file_handler = RotatingFileHandler('logs/application.log', maxBytes=5 * 1024 * 1024, backupCount=7)  # 5MB
#     file_handler.setLevel(logging.INFO)
#
#     formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
#     file_handler.setFormatter(formatter)
#
#     logger.addHandler(file_handler)
#
