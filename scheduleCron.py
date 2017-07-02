from crontab import CronTab
import config

my_user_cron  = CronTab(user=True)

job = my_user_cron.new(command='/usr/bin/python %s/get_concurrencies.py' % config.file_path)
job.minute.every(1)
my_user_cron.write()

