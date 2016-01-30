import sys
import urllib2
import re
from BeautifulSoup import BeautifulSoup
from datetime import datetime, timedelta

base_url = 'http://www.npr.org/sections/money/archive?date='
pod_matcher = re.compile('http://pd.npr.org/anon.npr-mp3/npr')

start_date_string = sys.argv[1]
end_date_string = sys.argv[2]
start_date = datetime.strptime(start_date_string, '%m-%d-%Y')
end_date = datetime.strptime(end_date_string, '%m-%d-%Y')
# start date should be in the future to end date
# download from start date backwards
if (start_date < end_date):
  end_date, start_date = start_date, end_date

current_date = start_date
downloaded_pods = {}
while (current_date > end_date):
  current_date_string = datetime.strftime(current_date, '%m-%d-%Y')
  raw_page = urllib2.urlopen(base_url + current_date_string).read()
  page = BeautifulSoup(raw_page)
  a_tags = page.findAll('a', href=pod_matcher)
  for a in a_tags:
    href = str(a['href'])
    filename = href.split('/')[-1].split('?')[0]
    if (filename not in downloaded_pods):
      print filename
      pod_url = urllib2.urlopen(href)
      # pod = open('../Downloads/' + filename, 'wb')
      pod = open(filename, 'wb')
      pod.write(pod_url.read())
      pod.close()
      downloaded_pods[filename] = True
  current_date = current_date - timedelta(7) # go back in time one week