# -*- coding: utf-8 -*- 
# file: bs_weblist.py
#Author: Shen Cong


import sys
sys.path.append('/Users/rimbaud/Documents/PythonLib/Library/')
from bs4 import BeautifulSoup
import urllib2
import csv
import os
import re

os.chdir("/Users/rimbaud/Documents/PythonLib/WebDataMining/")

'''
从人民银行网站下载 公开市场业务交易公告数据

地址：首页/货币政策司/货币政策工具/公开市场业务/公开市场业务交易公告
'''

''' #Proxy setting
proxy = urllib2.ProxyHandler({'http':'http://127.0.0.1:8087'})
opener = urllib2.build_opener(proxy)
urllib2.install_opener(opener)
'''

url ="http://www.pbc.gov.cn/publish/zhengcehuobisi/617/index.html"
html = urllib2.Request(url)
page = urllib2.urlopen(html)

content = page.read()

soup = BeautifulSoup(content)

#print(soup.prettify())
#print(soup.get_text())

#div = soup.find_all("div")
table = soup.find_all('table',width='90%')

list = table[0].find_all('td',height="22")
#html的每页有40个交易公告，len(list)=40；可以对list做循环逐个获取href地址



'''Get HTTP address
#Method 1
for a in list[0].find_all('a',href=True):
	print "链接地址: http://www.pbc.gov.cn"+ a['href']
'''

#Method 2
'''
obj = list[1].find_all('a',href=True)
print "链接地址: http://www.pbc.gov.cn" + obj[1].get('href')
'''
html_addr=[]
for i in xrange(len(list)):
	href = list[i].find_all('a',href=True)
	#print "链接地址: http://www.pbc.gov.cn"+href[1].get('href')
	temp = "http://www.pbc.gov.cn"+href[1].get('href')
	html_addr.append(temp)



for i in xrange(len(list)):
	print html_addr[i]
	html = urllib2.Request(html_addr[i])
	content = urllib2.urlopen(html).read()
	soup = BeautifulSoup(content)
	table = soup.find_all('table',width='610')


	# bond info
	term = table[0].find_all('td',width='187')
	amount = table[0].find_all('td',width='221')
	rate = table[0].find_all('td',width='202') 

	#issuing date
	date = soup.find_all('table',width="90%")
	term =term[1].get_text().encode('utf-8').replace('\n',"")
	amount = amount[1].get_text().encode('utf-8').replace('\n',"")
	rate = rate[1].get_text().encode('utf-8').replace('\n',"")
	
	date =  date[0].find_all("td",align='right')
	date = date[0].get_text().encode('utf-8')
	#print "发布日期:",date[0].get_text()
	saveFormat = term,amount,rate,date
	saveFormat = str(saveFormat)
	appendFile = open('info_list.txt','a')
	appendFile.write(saveFormat)
	appendFile.write('\n')
	appendFile.close()


'''
# bond info
duration = table[0].find_all('td',width='187')
amount = table[0].find_all('td',width='221')
rate = table[0].find_all('td',width='202') 

#issuing date
date = soup.find_all('table',width="90%")

print duration[0].get_text(),duration[1].get_text()
print amount[0].get_text(),amount[1].get_text()
print rate[0].get_text(),rate[1].get_text()

date =  date[0].find_all("td",align='right')

print "发布日期:",date[0].get_text()

'''

