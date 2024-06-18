# import logging
# import logging.handlers
# import os
# import gzip
#
# class CombinedRotatingFileHandler(logging.handlers.TimedRotatingFileHandler, logging.handlers.RotatingFileHandler):
#     def __init__(self, filename, when='midnight', interval=1, backupCount=7, maxBytes=5*1024*1024, encoding=None, delay=False, utc=False, atTime=None):
#         # Initialize both TimedRotatingFileHandler and RotatingFileHandler
#         logging.handlers.TimedRotatingFileHandler.__init__(self, filename, when, interval, backupCount, encoding, delay, utc, atTime)
#         self.maxBytes = maxBytes

# # Function to compress old log files
# def compress_old_logs(log_dir):
#     for filename in os.listdir(log_dir):
#         if filename.endswith(".log.1"):
#             with open(os.path.join(log_dir, filename), 'rb') as f_in:
#                 with gzip.open(os.path.join(log_dir, filename + '.gz'), 'wb') as f_out:
#                     f_out.writelines(f_in)
#             os.remove(os.path.join(log_dir, filename))
