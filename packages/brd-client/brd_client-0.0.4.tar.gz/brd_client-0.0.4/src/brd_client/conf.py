import logging
import os

from botocore.exceptions import ClientError
from dasida import get_secrets

logger = logging.getLogger(__name__)

SM_BRD_FOOD360 = os.getenv("SM_BRD_FOOD360", "brd-food360-eugene")
SM_BRD_FOOD360_TOKEN = os.getenv("SM_BRD_FOOD360", "brd-food360-usertoken")

secret = dict()
# user account to access Bright Data Food360 Zone
try:
    secret = get_secrets(SM_BRD_FOOD360)
except ClientError as e:
    logging.info("No Access Key for AWS SecretsManager!")
USERNAME = secret.get("username")
PASSWORD = secret.get("password")

# user token to access Bright Data
try:
    secret = get_secrets(SM_BRD_FOOD360_TOKEN)
except ClientError as e:
    logging.info("No Access Key for AWS SecretsManager!")
API_TOKEN = secret.get("token")
