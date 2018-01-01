
[![Build Status](https://travis-ci.org/jw/speed-tester.svg?branch=master)](https://travis-ci.org/jw/speed-tester)

## Tests your network and sends results to a remote monitor

The `speedtester` runs a network connection speed test and sends the results
to a remote monitor (see the
[`speed-monitor` project](https://github.com/jw/speed-monitor) for this).

A `crontab` scheduler (called `speedscheduler`) is also provided.

## Installation

Install with `pip` or `pipenv`.

```bash
$ pip install speed-tester
```

## speedscheduler

The `speedscheduler` enables or disables the scheduler.  Each 10 minutes
the tester will be run if enabled.

The `host` and `port` of the monitor need to be provided; while the `logfile`
and `user` are optional.  There is also a `--verbose` flag.

See `speedscheduler --help` for more info.

```bash
$ speedscheduler host 8000
Enabling speed-tester... done.
```

## speedtester

The `speedtester` uses `speedtest` to check the connection; so it will
find the closest server (based on pings) and will run an upload and download
test with it.  The result will be sent to the monitor (at `host:port`),
and the logs will be kept in the provided logfile (by default it is
`speed-tester.log`).

The `--verbose` logs in DEBUG mode; the `--console` also logs to console.
See `speedtester --help` for more info.

```bash
$ python speedtester.py localhost 8000 --console --verbose
Starting the test at 2018-01-01 12:48:17.299942.
Sending the results to monitor at localhost:8000.
Found client Skynet Belgium (id:2).
Found server speedtest.valentin-deville.eu:8080 (id:5).
Getting download speed...
Getting upload speed...
Sending this result: {'download': 11385752.249035608, 'upload': 6069441.245542229, 'ping': 83.075, 'server': 5, 'timestamp': '2018-01-01T11:48:17.923443Z', 'bytes_sent': 7921664, 'bytes_received': 14592576, 'share': None, 'client': 2}.
Sent result [up:6069441.245542229, down:11385752.249035608].
Stopping the test at 2018-01-01 12:48:42.062086; took 0:00:24.762144.
```
