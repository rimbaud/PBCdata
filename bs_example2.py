# -*- coding: utf-8 -*- 
# file: bs_example2.py
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

#url="http://www.pbc.gov.cn/publish/zhengcehuobisi/617/2013/20130909173619580320775/20130909173619580320775_.html"

#url="http://www.pbc.gov.cn/publish/zhengcehuobisi/617/2013/20130108102145973413565/20130108102145973413565_.html"

#央行票据
#url = "http://www.pbc.gov.cn/publish/zhengcehuobisi/617/2010/20101028105031390610655/20101028105031390610655_.html"

#正回购
url="http://www.pbc.gov.cn/publish/zhengcehuobisi/617/2012/20121115102737517551394/20121115102737517551394_.html"

#多张表格
url="http://www.pbc.gov.cn/publish/zhengcehuobisi/617/2010/20101028105031390610655/20101028105031390610655_.html"

#续做央票
#url = "http://www.pbc.gov.cn/publish/zhengcehuobisi/617/2013/20130909173619580320775/20130909173619580320775_.html"

#表格中有两笔操作
url = "http://www.pbc.gov.cn/publish/zhengcehuobisi/617/2012/20121115102737517551394/20121115102737517551394_.html"

#2007年时候的表格
url = "http://www.pbc.gov.cn/publish/zhengcehuobisi/617/1244/12442/12442_.html"

#2009
url = "http://www.pbc.gov.cn/publish/zhengcehuobisi/617/2010/20100428110659150968590/20100428110659150968590_.html"
#2010
#url = "http://www.pbc.gov.cn/publish/zhengcehuobisi/617/2010/20100428110808275437703/20100428110808275437703_.html"
html = urllib2.Request(url)
#page = urllib2.urlopen(html)

#content = page.read()
content = urllib2.urlopen(html).read()
soup = BeautifulSoup(content)

#print(soup.prettify())
#print(soup.get_text())

#div = soup.find_all("div")
table = soup.find_all('table')

print len(table)

#print table[13]

term1 = table[13].find_all('td')

p2 = table[13].find_all('tr')



print "td层数：",len(term1)


print "tr层数:",len(p2)


#print p2[0].get_text()

p3 = p2[0].find_all('td')

print "p3 len = ",len(p3)

p31 = p3[0].find_all('p',align='center')
print 'p3层的<p>层数:',len(p31)

#print p31[0].get_text()

tbody = table[13].find_all('tbody')

#len(tbody)代表了有几张表格
print 'tbody层数=',len(tbody)

#根据tbody的层数对每张表格逐个判断类型;经过测试，可以正确识别;但仅限于2010年之后的发布数据
for i in xrange(len(tbody)):
	tbody_tr = tbody[i].find_all('tr')
	ncol = tbody_tr[0].find_all('td')

	if len(ncol)==5:
		print '这是一张按照价格招标的央行票据'

	elif len(ncol)==4:
		if str(ncol[0].get_text().encode('utf-8')).find('名称')==1:
			if str(ncol[1].get_text().encode('utf-8')).find('续')==1:
				print '这是一张续作央票'
			else:
				print '这是一张按照利率招标的央行票据' 
	else: 
		print '这是正/逆回购操作'


print table[13].get_text()

'''
print ncol[0].get_text()

#在这里选择tbody层，也就是选择第几张表格
tbody_tr = tbody[0].find_all('tr')
#选择了tbody层的第一行，也就是表格的第一行
ncol = tbody_tr[0].find_all('td')

print ncol[0].get_text()
print '表格列数=',len(ncol)



if len(ncol)==5:
	print '这是一张按照价格招标的央行票据'

elif len(ncol)==4:
	if str(ncol[0].get_text().encode('utf-8')).find('名称')==1:
		if str(ncol[1].get_text().encode('utf-8')).find('续')==1:
			print '这是一张续作央票'
		else:
			print '这是一张按照利率招标的央行票据' 
else: 
	print '这是正/逆回购操作'


print ncol[0].get_text()

'''

'''
通过tr层确定有几笔资金投放;
公开市场操作数量= len(tr层）-2，减去的2代表了表格的标题层和层首的文字层。

'''


'''
BeautifulSoup的层级情况，如果<tr>层中包含<tr>层，例如组织如下：

<tr> abc
	<tr> 123</tr>
	<tr>456</tr>
</tr>

那么按照find_all('tr')搜索,tr共有3层，第一层的内容(index=0)是:
<tr> abc
	<tr> 123</tr>
	<tr>456</tr>
</tr>

第二层(index=1)的内容是：<tr> 123</tr>

'''



'''
#直接指向表格层级
p4 = p3[0].find_all('table')
print "p4 = ",len(p4)
print p4[0].get_text()
'''
#正回购和逆回购情况的处理



'''
目前发现有3类通告：
1、正回购、逆回购
2、央行票据发行情况
3、央行票据到期续做情况
'''


'''
for i in xrange(len(term1)):
	print term1[i].get_text()
'''


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
	


