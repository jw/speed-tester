from crontab import CronTab
import speedscheduler


def is_enabled():
    cron = CronTab(True)
    if len(list(cron.find_comment(speedscheduler.COMMENT))) == 0:
        return False
    else:
        return True


def test_creation():
    print(is_enabled)
    assert 4 == 4