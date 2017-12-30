from crontab import CronTab
import speedscheduler
import pytest


def is_enabled():
    cron = CronTab(True)
    if len(list(cron.find_comment(speedscheduler.COMMENT))) == 0:
        return False
    else:
        return True


def test_no_required_parameters():
    with pytest.raises(SystemExit):
        speedscheduler.main()


def test_scheduler():
    parser = speedscheduler.get_parser()
    args = parser.parse_args(['localhost', "80"])

    # empty the cron
    cron = CronTab(True)
    cron.remove_all()
    cron.write()

    speedscheduler.schedule(args)
    assert is_enabled()

    speedscheduler.schedule(args)
    assert not is_enabled()

    speedscheduler.schedule(args)
    assert is_enabled()

    speedscheduler.schedule(args)
    assert not is_enabled()
