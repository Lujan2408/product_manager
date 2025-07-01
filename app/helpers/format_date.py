from datetime import datetime

def now_without_microseconds(): 
  return datetime.now().replace(microsecond=0)