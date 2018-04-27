#coding=utf-8
import re
import urllib2
from bs4 import BeautifulSoup

import threading
import time
from random import choice


iplist=['118.1899.69.34','124.193.144.238','211.144.76.58','58.248.137.228']
exitFlag = 0
class myThread(threading.Thread):
	def __init__(self, threadID, name, startnumber):
		threading.Thread.__init__(self)
		self.threadID = threadID
		self.name = name
		self.startnumber = startnumber
	def run(self):
		x = 1
		while x < 6:
			print "Starting" + self.name + '%d' % self.startnumber +'\n'
			def getHtml(url):
				ip = choice(iplist)
				proxy_support = urllib2.ProxyHandler({'https': 'https://' + ip})
				opener = urllib2.build_opener(proxy_support)
				urllib2.install_opener(opener)

				page = urllib2.urlopen(url)
				html = page.read()
				return html

 			url = "http://www.medica-tradefair.com/vis/v1/en/search?oid=80396&lang=2&_query=&f_type=profile&f_country=DE&f_tag=medcom2016.MEDICA.0&f_tag=medcom2016.MEDICA.3&_start=" + str(self.startnumber)
			html = getHtml(url)
			# print html

			def getUrl(html):
				req = r'<a href=\"(/vis/v1/en/exhibitors/medcom2016.*?\?oid=80396&amp;lang=2&amp;_query=&amp;f_type=profile&amp;f_country=DE&amp;f_tag=medcom2016.MEDICA.0&amp;f_tag=medcom2016.MEDICA.3)\"*'
				imgre = re.compile(req)
				companyandurllist = re.findall(imgre, html)
				return companyandurllist

			urllist = getUrl(html)
 			print urllist
			for item in urllist:
				item = 'http://www.medica-tradefair.com' + item
				item += '\n'
				f = open('URLtext2', 'a')
				f.writelines(item)
				f.close()
			x += 1
			self.startnumber += 20
			time.sleep(10)
			print "Seeping" + self.name + '\n'
startnumberlist = [0, 100, 200, 300, 400, 500]
thread1 = myThread(1, "thread_1", startnumberlist[0])
thread2 = myThread(2, "thread_2", startnumberlist[1])
thread3 = myThread(3, "thread_3", startnumberlist[2])
thread4 = myThread(4, "thread_4", startnumberlist[3])
thread5 = myThread(5, "thread_5", startnumberlist[4])
thread6 = myThread(6, "thread_6", startnumberlist[5])

thread1.start()
thread2.start()
thread3.start()
thread4.start()
thread5.start()
thread6.start()
