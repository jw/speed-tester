
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
`speed-tester.log`.

See `speedtester --help` for more info.
