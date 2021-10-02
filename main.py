import datetime
import time

from daily_clock import daily_health_report

flag = False
today = datetime.date.today()
print("starting...")
while True:
    if datetime.date.today() != today:
        flag = False
    if not flag:
        now = datetime.datetime.now().strftime("%H:%M")
        if now >= '06:00' and now <= '19:30':
            rlist = daily_health_report()
            if len(rlist) and rlist[0]:
                flag = True
                today = datetime.date.today()
                print(datetime.datetime.now(), ": Finished.")
        else:
            print(datetime.datetime.now(), "It is not time to ...")
    else:
        print(datetime.datetime.now(), "Have Finished.")

    time.sleep(60*60*1.1)
