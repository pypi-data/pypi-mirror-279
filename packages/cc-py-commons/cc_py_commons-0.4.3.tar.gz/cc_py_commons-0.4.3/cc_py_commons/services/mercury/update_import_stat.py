import os
import requests

MERCURY_URL = os.environ.get("MERCURY_URL")
MERCURY_TOKEN = os.environ.get("MERCURY_TOKEN")

from cc_py_commons.utils.logger_v2 import logger


def execute(updated_data, import_stat_id):
  url = f"{MERCURY_URL}/importStats/{import_stat_id}"
  token = f"Bearer {MERCURY_TOKEN}"
  headers = {
    "Authorization": token
  }
  logger.debug(f"Update import stat: {import_stat_id} with data: {updated_data}")
  response = requests.put(url, json=updated_data, headers=headers)
  if response.status_code not in [200, 201]:
    return None
  else:
    return response.json()
