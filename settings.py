GOOGLE_CLIENT_ID = ''
GOOGLE_SECRET = ''

DEBUG = False

SECRET_KEY = 'blhablahashdjskfh'

# 1 day = 60s * 60m * 24h = 86400
TOKEN_SIGNING_TIMELIMIT = 86400

MEDIA_MERGED = True

try:
    from settingslocal import *
except ImportError:
    pass
