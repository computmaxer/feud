GOOGLE_CLIENT_ID = '387304306559.apps.googleusercontent.com'
GOOGLE_SECRET = '3o6xJe1kSg2LAvzSHjccoD47'

DEBUG = False

SECRET_KEY = 'blhablahashdjskfh'

# 1 day = 60s * 60m * 24h = 86400
TOKEN_SIGNING_TIMELIMIT = 86400

MEDIA_MERGED = True

try:
    from settingslocal import *
except ImportError:
    pass
