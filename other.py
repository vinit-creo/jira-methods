# This code sample uses the 'requests' library:
# http://docs.python-requests.org
import requests
from requests.auth import HTTPBasicAuth
import json


WORK_DOMAIN ="https://merry-weather.atlassian.net/"

url = f"{WORK_DOMAIN}api/3/bulk/issues/transition"

auth = HTTPBasicAuth("email@example.com", "<api_token>")

headers = {
  "Accept": "application/json"
}

query = {
  'issueIdsOrKeys': '{issueIdsOrKeys}'
}








def fetch_tickets_status():
    response = requests.request(
        "GET",
        url,
        headers=headers,
        params=query,
        auth=auth,
        )
    print(json.dumps(json.loads(response.text), sort_keys=True, indent=4, separators=(",", ": ")))