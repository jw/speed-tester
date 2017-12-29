from crontab import CronTab

cron = CronTab(user='jw')
cron.remove_all()

job = cron.new(command='python /home/jw/python/projects/speed-tester/tester.py', comment="speed-tester")
job.minute.every(10)

cron.write()

