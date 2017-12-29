from crontab import CronTab

# get the local directory

cron = CronTab(user='jw')
cron.remove_all()

command = 'python /home/jw/python/projects/speed-tester/tester.py ' \
          'localhost 8000 /tmp/speed-tester.log'
job = cron.new(command=command, comment="speed-tester")
job.minute.every(10)

cron.write()
