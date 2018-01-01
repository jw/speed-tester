#!/usr/bin/env python3

import requests
from requests.exceptions import ConnectionError
import speedtest
import logging
import sys
import argparse
from datetime import datetime

logger = logging.getLogger('speedlogger')


def abort(message, code=1):
    logger.error("Aborting: {0}".format(message))
    sys.exit(code)


def main():
    args = get_parser()
    create_logger(args)
    perfrom_test(args.host, args.port)


def create_logger(args):
    """
    Create a logger.  If --console is given, also log to console; if
    --verbse is set, enable the Logging.DEBUG.
    :param args:
    :return:
    """
    if args.verbose:
        logger.setLevel(logging.DEBUG)
    else:
        logger.setLevel(logging.INFO)

    fh = logging.FileHandler(args.logfile)
    logger.addHandler(fh)

    if args.console:
        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)
        logger.addHandler(ch)


def perfrom_test(host, port):
    now = datetime.now()

    logger.info("Starting the test at {0}.".format(now))
    logger.info("Sending the results to monitor at {0}:{1}.".
                format(host, port))

    # the real tester
    s = speedtest.Speedtest()

    # first get client
    client = s.config["client"]

    # get or create it via rest
    try:
        r = requests.get("http://{0}:{1}/api/clients?ip={2}&isp={3}".
                         format(host, port, client["ip"], client["isp"]))
        if r.ok and len(r.json()) == 1:
            logger.info("Found client {0} (id:{1}).".
                        format(r.json()[0]["isp"], r.json()[0]["id"]))
            client_id = r.json()[0]["id"]
        else:
            logger.info("Creating client {0} (ip:{1})...".
                        format(client["isp"], client["ip"]))
            logger.debug("Creating client using {0}.".format(client))
            r = requests.post("http://{0}:{1}/api/clients".
                              format(host, port), json=client)
            if r.ok:
                logger.info("Created client {0} (id:{1}).".
                            format(r.json()["isp"], r.json()["id"]))
                client_id = r.json()["id"]
            else:
                abort("Could not get or create the client!")
    except ConnectionError:
        abort("Could not connect to the monitor; is it running?")

    # then get the server
    s.get_best_server()

    # get or create it via rest
    try:
        r = requests.get('http://{0}:{1}/api/servers?host={0}'.
                         format(host, port, s.best["host"]))
        if r.ok and len(r.json()) == 1:
            logger.info("Found server {0} (id:{1}).".
                        format(r.json()[0]["host"], r.json()[0]["id"]))
            server_id = r.json()[0]["id"]
        else:
            logger.info("Creating server {0} (name:{1})...".
                        format(s.best["host"], s.best["name"]))
            s.best['identifier'] = s.best['id']
            del s.best['id']
            logger.debug("Creating server using {0}.".format(s.best))
            r = requests.post("http://{0}:{1}/api/servers".
                              format(host, port), json=s.best)
            if r.ok:
                logger.info("Created server {0} (id:{1}).".
                            format(r.json()["host"], r.json()["id"]))
                server_id = r.json()["id"]
            else:
                abort("Could not get or create the server!")
    except ConnectionError:
        abort("Could not connect to the monitor; is it running?")

    # test the speed of the link
    logger.info("Getting download speed...")
    s.download()
    logger.info("Getting upload speed...")
    s.upload()

    # prepare the result...
    result = s.results.dict()
    result["client"] = client_id
    result["server"] = server_id

    # ...and send it to the monitor
    try:
        logger.debug("Sending this result: {0}.".format(result))
        r = requests.post("http://{0}:{1}/api/results".
                          format(host, port), json=result)
        if r.ok:
            logger.info("Sent result [up:{0}, down:{1}].".
                        format(result["upload"], result["download"]))
        else:
            abort("Could not send the result to the monitor!")
    except ConnectionError:
        abort("Could not connect to the monitor; is it running?")

    later = datetime.now()

    logger.info("Stopping the test at {0}; took {1}.".format(later,
                                                             later - now))


def get_parser():
    description = "Test the speed of your network connection and " \
                  "send the result to a monitor."
    # get the host and the port arguments and optionally the logfile
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument("host", type=str,
                        help="The host where the monitor runs.")
    parser.add_argument("port", type=str,
                        help='The port where the monitor runs.')
    parser.add_argument("logfile", type=str, nargs="?",
                        default="speed-tester.log", help="The log file.")
    parser.add_argument("--console", action="store_true",
                        help="Also log to console.")
    parser.add_argument("--verbose", action="store_true",
                        help="Log more verbosely (i.e. in DEBUG mode).")
    args = parser.parse_args()
    return args


if __name__ == '__main__':
    main()
