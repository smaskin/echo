import logging
from logging.handlers import TimedRotatingFileHandler

handler = TimedRotatingFileHandler('runtime/app.log', when="d", interval=1, backupCount=5)
handler.setFormatter(logging.Formatter("%(asctime)s %(levelname)-10s %(module)s %(funcName)s %(message)s"))

app_log = logging.getLogger('app')
app_log.addHandler(handler)
app_log.setLevel(logging.INFO)
