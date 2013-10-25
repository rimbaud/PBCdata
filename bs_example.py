# -*- coding: utf-8 -*- 
# file: bs_example.py
#Author: Shen Cong
'''
从人民银行网站下载 公开市场业务交易公告数据

地址：首页/货币政策司/货币政策工具/公开市场业务/公开市场业务交易公告
'''
import sys
sys.path.append('/Users/rimbaud/Documents/PythonLib/Library/')
from bs4 import BeautifulSoup
import urllib2
import csv
import os
import re

''' #Proxy setting
proxy = urllib2.ProxyHandler({'http':'http://127.0.0.1:8087'})
opener = urllib2.build_opener(proxy)
urllib2.install_opener(opener)
'''

#url ="http://www.pbc.gov.cn/publish/zhengcehuobisi/617/2013/20130924101842840143892/20130924101842840143892_.html"

url="http://www.pbc.gov.cn/publish/zhengcehuobisi/617/2013/20130909173619580320775/20130909173619580320775_.html"
html = urllib2.Request(url)
#page = urllib2.urlopen(html)

#content = page.read()
content = urllib2.urlopen(html).read()
soup = BeautifulSoup(content)

#print(soup.prettify())
#print(soup.get_text())

#div = soup.find_all("div")
table = soup.find_all('table',width='498')

'''
# bond info
term = table[0].find_all('td',width='187' )
amount = table[0].find_all('td',width='221')
rate = table[0].find_all('td',width='202') 

#issuing date
date = soup.find_all('table',width="90%")

print term[0].get_text(),term[1].get_text()
print amount[0].get_text(),amount[1].get_text()
print rate[0].get_text(),rate[1].get_text()

date =  date[0].find_all("td",align='right')


print "发布日期:",date[0].get_text()
'''
print table[0]

term1 = table[0].find_all('td')

for i in xrange(len(term1)):
	print term1[i].get_text()


'''
term1= term[1].get_text().encode('utf-8') #需要进行编码，不然中文编码显示错误
amount1 = amount[1].get_text().encode('utf-8')
rate1 = rate[1].get_text().encode('utf-8')
reformat = term1,amount1,rate1

term1 = term1.replace('\n',"")
amount1 = amount1.replace('\n',"")
rate1 = rate1.replace('\n',"")
f= openwriter(open("info.txt", "w"))
f.writerow(["term", "amount","rate"]) # Write column headers as the first line
f.writerow([term1,amount1,rate1])

'''

#saveFormat = str(reformat).replace('\'',"").replace('(',"").replace(')',"")   #这一步，把tuple转换回string
	


