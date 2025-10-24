#BusSchedule.py
#Name:
#Date:
#Assignment:

import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By


def loadURL(url):
  """
  This function loads a given URL and returns the text
  that is displayed on the site. It does not return the
  raw HTML code but only the code that is visible on the page.
  """
  chrome_options = Options()
  chrome_options.add_argument('--no-sandbox')
  chrome_options.add_argument('--disable-dev-shm-usage')
  chrome_options.add_argument("--headless");
  driver = webdriver.Chrome(options=chrome_options)
  driver.get(url)
  content=driver.find_element(By.XPATH, "/html/body").text
  driver.quit()

  return content

def loadTestPage():
  """
  This function returns the contents of our test page.
  This is done to avoid unnecessary calls to the site
  for our testing.
  """
  page = open("testPage.txt", 'r')
  contents = page.read()
  page.close()

  return contents
now = datetime.datetime.now()
currentHour = (now.hour + 19) - 12
currentMinute = now.minute
currentTime = currentHour,":",currentMinute

def getHours(time):
  """Converts 12 hour clock to 24 hour clock"""
  ampm = time.strftime("%p")
  if ampm == "AM":
    time = currentHour + 12
  print(time)
  return time

def getMinutes(time):
  """Extracts only the minutes from a time input"""
  minutes= time.strftime("%M")
  print(minutes)
  return minutes

def isLater(time1, time2):
  """Determines if time1 is later than time2"""
  later == False
  time1AMPM = time1.strftime("%p%")
  time2AMPM = time2.strftime("%p%")
  if time1AMPM == "AM" and time2AMPM == "PM":
    later = False
  elif time1AMPM == "PM" and time2AMPM == "AM":
    later = True
  elif time1.strftime("%H") > time2.strftime("%H"):
    later = True
  elif time1.strftime("%H") == time2.strftime("%H") and time1.strftime("%M") > time2.strftime("%M"):
    later = True
  elif time1 == time2:
    later = False
  return later


def timesList(stopInfo):
  """Takes information from the stop, determines if a word is a time and makes a list of the times at that stop"""
  allInfo = []
  allTimes = []
  word = stopInfo.split()
  allInfo.append(word)
  flatInfo = [w for group in allInfo for w in group]
  for word in flatInfo: 
    w = word.strip().lower().replace('.', '').replace(',', '')
    if ":" in w: 
      parts = w.split(":")
      if len(parts) == 2 and parts[0].isdigit() and parts[1][:2].isdigit():
        hour = int(parts[0])
        minute = int(parts[1][:2])
        if 0 <= hour <= 23 and 0 <= minute <= 59:
          allTimes.append(word)
  return allTimes
  
def timeToMinutes(t):
  """Converts a time to minutes"""
  if isinstance(t, tuple):
   t = t[0]
  t = str(t)
  t = t.strip().lower().replace('.', '')
  hour = 0 
  minutes = 0 
  isPM = 'pm' in t 
  isAM = 'am' in t 
  t = t.replace('am', '').replace('pm', '')
  if ':' in t:
    h, m = t.split(':', 1) 
    hour = int(h)
    minutes = int(m)
  else:
    hour = int(t)
    minutes = 0 
    if isPM and hour != 12:
      hour += 12
    if isAM and hour != 12:
      hour = 0
  return hour * 60 + minutes



stopCode = "2269"
routeNumber = "11"
directionName = "EAST"
    

  



def main():
  url = "https://myride.ometro.com/Schedule?stopCode="+stopCode+"&routeNumber="+routeNumber+"&directionName="+directionName
  #c1 = loadURL(url) #loads the web page
  c1 = loadTestPage() #loads the test page
  #print(c1)
  #getHours(now)
  #getMinutes(now)
  timesList(c1)
  print("The current time is",currentHour,":",currentMinute)
  timeInMins = timeToMinutes(currentTime)
  timeMinutes = [timeToMinutes(t) for t in timesList(c1)]
  nextTimes = []
  for i, tMinutes in enumerate(timeMinutes):
    if tMinutes > timeInMins:
      nextTimes = timesList(c1)[i:i+2]
      break
  if len(nextTimes) < 2:
    needed = 2 - len(nextTimes)
    nextTimes += timesList(c1)[:needed]
  for t in nextTimes:
    diff = (timeToMinutes(t)- timeInMins) % (24 * 60)
    hours = diff // 60
    minutes = diff % 60
    print("The next bus is",minutes,"minutes away")
main()
