import json
import requests

import os
from dotenv import load_dotenv
load_dotenv()

with open('../check-domains.txt', 'r') as main:

  for line in main:
    response = requests.get("https://www.whoisxmlapi.com/whoisserver/WhoisService",
      {
        'domainName' : line,
        'outputFormat': 'json',
        'apiKey' : os.getenv('whoisxmlapikey'),
        'thinWhois' : 'true'
      }
    )

    data=response.json()

    print(
      json.dumps(
        {
          'domain': line.rstrip("\n"),
          'hostNames': data['WhoisRecord']['registryData']['nameServers']['hostNames']
        }, indent=4
      )
    )
