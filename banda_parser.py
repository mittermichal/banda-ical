#from icalendar import Calendar, Event
from ics import Calendar, Event
from urllib.request import urlretrieve
from lxml import etree
import os
import time
import re
import datetime
import arrow

def display(cal):
  return cal.to_ical().decode('utf-8').replace('\r\n', '\n').strip()

def getCal(regex):
  file='cache.html'
  details_cache='details.txt'

  format="%d.%m.%Y %H:%M"

  if not os.path.exists(file) or time.time()-os.path.getmtime(file)>60:
    print('cache too old')
    urlretrieve('http://www.gullivers.banda.cz/nejblizsi-akce/',file)
  else:
    print('using cache')


  htmlparser = etree.HTMLParser(encoding='utf-8')
  tree = etree.parse(file,htmlparser)
  res=tree.xpath('//div[@class="event fulllist underline"]')
  #res=tree.xpath('//body')

  details=[]
  for line in open(details_cache,'r',encoding='utf-8').readlines():
    s=line.replace('\n','').split('\t')
    #print(s)
    if time.time()-datetime.datetime.strptime(s[2], format).timestamp()<60*30:
      details.append((s[0],s[1],s[2]))

  #print(details)

  cal = Calendar()

  for event in res:
    title=event[0][0].text
    if re.search(regex,title):
      url=event[0][0].items()[0][1]
      timenode=event[1][0].xpath('node()')[1].replace(' - \n                                    ','')
      interval=timenode.split(' - ')
      print(title,event[1][0][0].text,timenode,url)
      start_time=datetime.datetime.strptime(interval[0], format)
      try:
        end_time=datetime.datetime.strptime(interval[1], format)
      except ValueError:
        end_time=datetime.datetime.strptime(interval[1], "%H:%M")
        end_time=end_time.replace(day=start_time.day,month=start_time.month,year=start_time.year)
      #print(dir(event[1][0]))
      print(start_time,' - ',end_time)

      #print('')

      find=list(filter(lambda x: x[1]==url,details))
      if len(find):
        location=find[0][0]
        #'http://www.gullivers.banda.cz'
      else:
        urlretrieve('http://www.gullivers.banda.cz'+url,'tmp')
        tree = etree.parse('tmp', htmlparser)
        res = tree.xpath('//p[@class="location"]')
        details.append((res[0].text,url,datetime.datetime.fromtimestamp(time.time()).strftime(format)))
        location=res[0].text
      print(location)


      event = Event(location=location)
      event.name=title
      event.begin = arrow.get(start_time,'Europe/Prague')
      event.end = arrow.get(end_time,'Europe/Prague')

      cal.events.append(event)

  with open(details_cache,'w',encoding='utf-8') as d:
    for detail in details:
      for col in detail:
        d.write(col+'\t')
      d.write('\n')

  with open('my.ics', 'w', encoding='utf-8') as my_file:
    my_file.writelines(cal)

  return



