# -*- coding: utf-8 -*- 
# file: bs_weblist2.py
#Author: Shen Cong
#这是针对一组网页地址的批量操作测试

'''
	从人民银行网站下载 公开市场业务交易公告数据

	地址：中国人民银行网站  首页/货币政策司/货币政策工具/公开市场业务/公开市场业务交易公告
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

#目前共有18页

rawlist = ["http://www.pbc.gov.cn/publish/zhengcehuobisi/617/index.html"]

for i in xrange(2,24):
	url = "http://www.pbc.gov.cn/publish/zhengcehuobisi/617/index_" + str(i) +".html"
	rawlist.append(url)

#print rawlist #test Ok

#store all the html in a list
html_addr=[]
for i in xrange(len(rawlist)):
	#print rawlist[i]
	url = rawlist[i]
	html = urllib2.Request(url)
	page = urllib2.urlopen(html)

	content = page.read()

	soup = BeautifulSoup(content)
	tablelist = soup.find_all('table',width='90%')
	iter_list = tablelist[0].find_all('td',height="22")
	#html的每页有40个交易公告，len(list)=40；可以对list做循环逐个获取href地址



	for i in xrange(len(iter_list)):
		href = iter_list[i].find_all('a',href=True)
		#print "链接地址: http://www.pbc.gov.cn"+href[1].get('href')
		temp = "http://www.pbc.gov.cn"+href[1].get('href')
		html_addr.append(temp)

#print html_addr #test Ok

#print html_addr


for i in xrange(len(html_addr)):

	url = html_addr[i]
	html = urllib2.Request(url)
	content = urllib2.urlopen(html).read()
	soup = BeautifulSoup(content)

	#print(soup.prettify())
	#print(soup.get_text())

	table = soup.find_all('table')

	table_layer = table[13].find_all('table')

	#len(tbody)代表了有几张表格
	#print 'table层数=',len(table_layer) #its a test to see if work OK

	#日期信息保存在table[11]
	date = table[11].get_text().encode('utf-8').split()[-2:] #表示截取最后两个元素
	date = str(date).replace('[',"").replace(']',"").replace(',','').replace("\'","")


	#根据table的层数对每张表格逐个判断类型;经过测试，可以正确识别2004年以来的所有表格
	for i in xrange(len(table_layer)):
		tbody_tr = table_layer[i].find_all('tr')  #对于每个table层，根据<tr>标签计算出行数
		ncol = tbody_tr[0].find_all('td')  #在表格的每一行中计算出该表格的列数
	
		operateType = 0 
		#####################################
		#	Define: 1:表示正回购			#
		#			-1:表示逆回购			#
		#			price:价格招标央票		#
		#			rate:利率招标央票		#
		#			extend:续做央票			#
		#####################################
		if len(ncol)==5:
			#print '这是一张按照价格招标的央行票据'
			operateType = 'price'  #表示这是按照价格招标的央票
			for i in xrange(1,len(tbody_tr)):
			#print tbody_tr[i].get_text()
			
				data = str(tbody_tr[i].get_text().encode('utf-8')).split() # 这是删除字符串中的空白字符串的方法 replace('\n'," ")
				#print str(data)
				supplement = data.pop(-2) #把价格信息从中删除
				data.append(operateType)  #把新信息添加进入原来的数组List
				data.append(date)
				data.append(supplement)
			
				#将处理完的数据写入txt文件保存
				f = csv.writer(open('class2.txt','a+b'))  # “+”号表示追加写
				#f.writerow(['term','amount','rate','type','date'])
				f.writerow(data)
				#print data
			
		elif len(ncol)==4:
			if str(ncol[0].get_text().encode('utf-8')).find('名称')>0:
				if str(ncol[1].get_text().encode('utf-8')).find('续')>0:
					#print '这是一张续做央票'
					operateType= 'extend'  #表示这是一张续做央票
					for i in xrange(1,len(tbody_tr)):
						data = str(tbody_tr[i].get_text().encode('utf-8')).split() # 这是删除字符串中的空白字符串的方法 replace('\n'," ")
			
						data.append(operateType)  #把新信息添加进入原来的数组List
						data.append(date)
			
						#将处理完的数据写入txt文件保存
						f = csv.writer(open('class2.txt','a+b'))  # “+”号表示追加写
						#f.writerow(['term','amount','rate','type','date'])
						f.writerow(data)
						#print data


				else:
					#print '这是一张按照利率招标的央行票据' 
					operateType = 'rate' #表示这是按利率招标的央票

					for i in xrange(1,len(tbody_tr)):
						data = str(tbody_tr[i].get_text().encode('utf-8')).split() # 这是删除字符串中的空白字符串的方法 replace('\n'," ")
			
						data.append(operateType)  #把新信息添加进入原来的数组List
						data.append(date)
				
						#将处理完的数据写入txt文件保存
						f = csv.writer(open('class2.txt','a+b'))  # “+”号表示追加写
						#f.writerow(['term','amount','rate','type','date'])
						f.writerow(data)
						#print data
		else: 
			if str(table[13].get_text().encode('utf-8')).find('逆回购') >0:
				#print '这是逆回购'
				operateType = -1
			elif str(table[13].get_text().encode('utf-8')).find('正回购')>0:
				#print '这是正回购' # it's a test to see if work right
				operateType = 1
			else:
				#print '不知道回购类型'
				operateType = 0

			#nrow = len(tbody_tr)
			#print '表格的行数:',nrow
	
			for i in xrange(1,len(tbody_tr)):
				data = str(tbody_tr[i].get_text().encode('utf-8')).split() # 这是删除字符串中的空白字符串的方法 replace('\n'," ")
			
				data.append(operateType)  #把新信息添加进入原来的数组List
				data.append(date)
			
				#将处理完的数据写入txt文件保存
				f = csv.writer(open('class1.txt','a+b'))  # “+”号表示追加写
				#f.writerow(['term','amount','rate','type','date'])
				f.writerow(data)
				#print data
		

#print str(date).replace('[',"").replace(']',"").replace(',','').replace("\'","")




'''
#这是通过对每个<p>层进行内容匹配，以此判断回购类型的方法
ptag = table[13].find_all('p')

ptag_index = -1
for i in xrange(5):
	if str(ptag[i].get_text().encode('utf-8')).find('回购') >0:
		ptag_index = i
		break

print ptag[ptag_index].get_text()

print ptag[2].get_text()

if u'回购' in ptag[2].get_text():
	print "找到回购："

print u'adbc'.find('g')
'''


#str(ptag[1].get_text().encode('utf-8')).find('回购')>0



#如果是单张表格,那么ptag[0]就是操作情况

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
	


