import logging
import os

from dasida import get_secrets

logger = logging.getLogger(__name__)

SM_BRD_FOOD360 = os.getenv("SM_BRD_FOOD360", "brd-food360-eugene")
SM_BRD_FOOD360_TOKEN = os.getenv("SM_BRD_FOOD360", "brd-food360-usertoken")

secret = dict()
# user account to access Bright Data Food360 Zone
try:
    secret = get_secrets(SM_BRD_FOOD360)
except:
    logging.warning("No Access Key for AWS SecretsManager!")
    pass
USERNAME = secret.get("username")
PASSWORD = secret.get("password")

# user token to access Bright Data
try:
    secret = get_secrets(SM_BRD_FOOD360_TOKEN)
except:
    logging.warning("No Access Key for AWS SecretsManager!")
    pass
API_TOKEN = secret.get("token")
