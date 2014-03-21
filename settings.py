BLUEPRINT_PATH = "./apiary.json"
BLUEPRINT_URL = "http://superdesk.apiary.io"

SERVER_URL = "http://superdesk.apiary.io"
IGNORE_ENDPOINTS = ['/Security/Login', '/Security/Authentication', ]
LOGIN = 'admin'
PASS = 'admin'

VERBOSITY = 2
PRINT_URL = True
XML_OUTPUT = False

try:
    from settings_local import *
except:
    pass
