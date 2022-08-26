import requests
import json
import argparse
import logging
import sys

from requests.auth import HTTPBasicAuth

# interpret data sent from Opsgenie #
parser = argparse.ArgumentParser()
parser.add_argument('-payload', '--queuePayload', help='Payload from queue', required=True)
parser.add_argument('-apiKey', '--apiKey', help='The apiKey of the integration', required=True)
parser.add_argument('-opsgenieUrl', '--opsgenieUrl', help='The url', required=True)
parser.add_argument('-logLevel', '--logLevel', help='Level of log', required=True)

# args contains everything sent from Opsgenie payload, apiKey, OpsgenieURL, loglevel #
args = vars(parser.parse_args())
logging.basicConfig(stream=sys.stdout, level=args['logLevel'])

def main():
  logging.info(args['queuePayload'])

  # parse queuePayload to get alert object
  queue_message_string = args['queuePayload']
  queue_message = json.loads(queue_message_string)
  alert = queue_message["alert"]

  headers = {
        "Content-Type": "application/json",
        "Accept-Language": "application/json",
        "Authorization": "GenieKey " + args['apiKey']
    }

  ack_alert_url = args['opsgenieUrl'] + "/v2/alerts/" + alert["alertId"] + "/acknowledge"
  close_alert_url = args['opsgenieUrl'] + "/v2/alerts/" + alert["alertId"] + "/acknowledge"

  # get alert details
  alert_details = queue_message.get('params').get('alertDetails')

  # get bypassURL
  url = "http://" + alert_details.get('bypassURL')
  logging.info("webLink - bypassURL={}".format(url));

  # get url to execute
  response = requests.get(url)

  # acknowledge alert
  response = requests.post(url=ack_alert_url, headers=headers)

  # close alert
  response = requests.post(url=close_alert_url, headers=headers)


if __name__ == '__main__':
    main()
