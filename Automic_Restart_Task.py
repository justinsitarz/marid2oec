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

  # get alert details
  alert_details = queue_message.get('params').get('alertDetails')

  # get restartURL
  url = "http://" + alert_details.restartURL
  logger.info("webLink - restartURL={}".format(url));

  # get url to execute
  res = requests.get(url)


if __name__ == '__main__':
    main()