import requests
from requests.exceptions import ConnectionError
import speedtest
import logging
import sys
import argparse


logging.basicConfig(filename="speed-tester.log", level=logging.INFO)


def abort(message, code=1):
    logging.error("Aborting: {0}".format(message))
    sys.exit(code)


# get the host and the port
description = "Tests the speed of your network connection and sends the result to a monitor."
parser = argparse.ArgumentParser(description=description)
parser.add_argument("host", type=str,
                    help="The host where the monitor runs.")
parser.add_argument("port", type=str,
                    help='The port where the monitor runs.')
args = parser.parse_args()

logging.info("Sending the results to monitor at {0}:{1}.".format(args.host, args.port))

# the rester tester
s = speedtest.Speedtest()

# first get client
config = s.get_config()
client = s.config['client']

# get or create it via rest
try:
    r = requests.get("http://localhost:8000/api/clients?ip={0}&isp={1}".format(client["ip"], client["isp"]))
    if r.ok and len(r.json()) == 1:
        logging.info("Found client {0} (id:{1}) ".format(r.json()[0]["isp"], r.json()[0]["id"]))
        client_id = r.json()[0]["id"]
    else:
        logging.info("Creating client {0} (ip:{1})".format(client["isp"], client["ip"]))
        r = requests.post('http://localhost:8000/api/clients', json=s.config['client'])
        if r.ok:
            logging.info("Created client {0} (id:{1}) ".format(r.json()["isp"], r.json()["id"]))
            client_id = r.json()["id"]
        else:
            abort("Could get or create the client!")
except ConnectionError:
    abort("Could not connect to the monitor; is it running?")

# then get the server
s.get_best_server()

# get or create it via rest
try:
    r = requests.get('http://localhost:8000/api/servers?url={0}'.format(s.best["url"]))
    if r.ok and len(r.json()) == 1:
        logging.info("Found server {0} (id:{1}) ".format(r.json()[0]["url"], r.json()[0]["id"]))
        server_id = r.json()[0]["id"]
    else:
        logging.info("Creating server {0} (name:{1})".format(s.best["url"], s.best["name"]))
        r = requests.post('http://localhost:8000/api/servers', json=s.best)
        if r.ok:
            logging.info("Created server {0} (id:{1}) ".format(r.json()["url"], r.json()["id"]))
            server_id = r.json()["id"]
        else:
            abort("Could get or create the server!")
except ConnectionError:
    abort("Could not connect to the monitor; is it running?")

# test the speed of the link
logging.info("Getting download speed...")
s.download()
logging.info("Getting upload speed...")
s.upload()

# prepare the result...
result = s.results.dict()
result["client"] = client_id
result["server"] = server_id

# ...and send it to the monitor
r = requests.post('http://localhost:8000/api/results', json=result)
if r.ok:
    logging.info("Added result [up:{0}, down:{1}] ".format(result["upload"], result["download"]))
else:
    abort("Could not send the result to the monitor!")
