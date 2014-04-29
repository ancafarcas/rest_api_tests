BLUEPRINT_PATH = "./apiary.json"
BLUEPRINT_URL = "http://superdesk.apiary.io"

#SERVER_URL = "http://superdesk.apiary.io"
SERVER_URL = "http://localhost:8081/api-test"
IGNORE_ENDPOINTS = ['/Security/Login', '/Security/Authentication', ]
LOGIN = 'admin'
PASS = 'admin'

PRINT_URL = False
PRINT_PAYLOAD = False
PRINT_DELIMITER = False
XML_OUTPUT = False

try:
    from tests.settings_local import *
except:
    pass
