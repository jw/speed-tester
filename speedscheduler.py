#!/usr/bin/env python3

from crontab import CronTab
import sys
import argparse

COMMENT = "speed-tester"


def abort(message, code=1):
    print("Aborting: {0}".format(message))
    sys.exit(code)


def main():
    parser = get_parser()
    args = parser.parse_args()
    schedule(args)


def get_parser():
    # get the host and the port arguments and optionally the logfile
    description = "Switches the scheduled cronjob on or off."
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument("host", type=str,
                        help="The host where the monitor runs.")
    parser.add_argument("port", type=str,
                        help='The port where the monitor runs.')
    parser.add_argument("name", type=str, nargs="?",
                        default="/usr/local/bin/speedtester",
                        help="The speedtester command.")
    parser.add_argument("logfile", type=str, nargs="?",
                        default="/tmp/speedtester.log",
                        help="The log file for the speedtester.")
    parser.add_argument("user", type=str, nargs="?",
                        help="The user which will run the speedtester.")
    parser.add_argument("--verbose", action="store_true",
                        help="Increase verbosity level.")
    return parser


def schedule(args):
    if args.user is None:
        args.user = True

    cron = CronTab(user=args.user)

    if len(list(cron.find_comment(COMMENT))) == 0:
        # no job found - create one...
        print("Enabling speedtester...", end='')
        command = "{0} {1} {2} {3}".format(args.name, args.host,
                                           args.port, args.logfile)
        job = cron.new(command=command, comment=COMMENT)
        job.minute.every(10)
        print(" done.")
        if args.verbose:
            print("Added '{0}' to crontab.".format(command))

    else:
        # ...remove all found jobs
        print("Disabling speedtester...", end='')
        for job in cron.find_comment(COMMENT):
            cron.remove(job)
        print(" done.")

    cron.write()


if __name__ == '__main__':
    main()
