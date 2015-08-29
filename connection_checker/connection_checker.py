from datetime import datetime
import os
import time


class Status(object):
  Success = 0
  Fail = 1


hostnames = ["www.google.com", "www.facebook.com", "www.yandex.ru"]


interval = 1


def WriteToLog(message, append_date_time=True, draw_line=True):
  if append_date_time:
    message += ' '+str(datetime.now())
  message += '\n'
  if draw_line:
    message += '-'*80+'\n'
  log_file=open('log.txt', 'a')
  log_file.write(message)
  log_file.close()
  print(message, end='')


def Ping ():
  ping_failed = False
  for hostname in hostnames:
    ping_failed = ping_failed or os.system("ping -n 1 " + hostname)
  return (Status.Fail if ping_failed else Status.Success)


def ConnectionChecker():
  prev_status = Status.Success
  WriteToLog('The program started working at')
  try:
    while True:
      status = Ping()
      if status != prev_status:
        if (status == Status.Success):
          WriteToLog('Connection was established at')
        else:
          WriteToLog('Connection was lost at', draw_line=False)
      prev_status = status
      time.sleep(interval)
  except KeyboardInterrupt:
    WriteToLog('The program finished working at')
  except Exception:
    WriteToLog('The program failed at')


if __name__ == '__main__':
  ConnectionChecker()
