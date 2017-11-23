#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2017-11-23 18:08:20
# @Author  : Milktea (milktea@vmoe.info)
# @Link    : https://milktea.info
#
# eBook Downloader for www.yushuwu.com
# python2 ONLY !
# Usage : If you don't wanna change the source code,
#         Just run `python book.py <book_id>`.
#         But in fact, it supports batch processing.
#         Find it yourself, 23333.

import sys,os
import re
import requests
import hashlib
import base64

url = "https://www.yushuwu.com/read/%d/"
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36"
headers = {'user-agent': UA,}
black_list = [56888,]

def Milktea_parser(context):
	context = context.replace('&nbsp;&nbsp;&nbsp;&nbsp;','  ') # Why So many space
	context = context.replace('&nbsp;',' ') # Manual HTML_Parser
	context = context.replace('&#039;',chr(39)) # A stupid escape
	context = context.replace('\r\n','\n') # I'm using Windows, But I love Linux
	context = context.replace('\n\n','\n') # Compress it
	context = context.replace('\n\n','\n') # Again 2333
	return context

def decrypt(cipher):
	key = hashlib.md5('123456').hexdigest()
	m = base64.b64decode(cipher)
	code = ""
	for i in range(len(m)):
		k = i % 32
		code += chr(ord(m[i]) ^ ord(key[k]))
	return base64.b64decode(code)

def get_filename(book_id):
	r = requests.get(url % book_id, headers=headers)
	r.encoding = 'gbk'
	t = r.text
	filename = re.search('h1(.+)h1',t).group()[3:-4]
	return filename.replace('&#039;',chr(39)).replace('\\','')

def get_pagelist(book_id):
	r = requests.get(url % book_id, headers=headers)
	r.encoding = 'gbk'
	t = r.text
	dd = t.split("<dd class='chapter_list'>")[1:]
	page = [re.search('"(.+)",',i).group()[1:-2] for i in dd]
	page_list = [int(decrypt(i)) for i in page]
	page_list.sort()
	return page_list

def get_context(book_id,page_list,filename):
	if book_id in black_list:
		print '[Error] : This book is in Black List !'
		return
	try:
		f = open('['+str(book_id)+']'+filename+'.txt','w')
	except Exception as e:
		print e
		# raise e
		f = open(str(book_id)+'.txt','w')
	# f = open('['+str(book_id)+']'+filename+'.txt','w')
	for i in page_list:
		r = requests.get(url % book_id +str(i) + '/', headers=headers)
		r.encoding = 'gbk'
		t = r.text
		main = t.split('<article id="main">')[1].split('</article>')[0]
		# head = re.search('h1(.+)h1',main).group()[4:-4].encode('utf-8')
		# f.write(head)
		main = re.sub('<span(.+)</span>','',main) # remove CopyRight
		main = re.sub('(<p></p>)|(</p><p>)','',main) # remove extra '<p>'
		context = re.search('<p>(.+)</p>',main,re.DOTALL).group()[4:-4].encode('utf-8')
		context = Milktea_parser(context)
		# context
		f.write(context)
		print '[Downloading] : ' + str(book_id) + " - " + str(i) + ' / ' + str(page_list[-1])
	f.close()
	print '[Downloaded] : ' + str(book_id) + ' Finished !'

# book_id = int(sys.argv[1])
# page_list = get_pagelist(book_id)
# filename = get_filename(book_id)

# get_context(book_id,page_list,filename)

for i in range(20):
	URL = "https://m.yushuwu.com/tag/sm/p_%d.html" % i
	r = requests.get(URL, headers=headers)
	t = r.text
	li = re.search('<ul id="list_ul">(.+)</ul>',t,re.DOTALL).group()
	li = li.split('novel')
	li_1 = []
	for i in li:
		if i[6:11] == '.html':
			li_1.append(i[1:6])
	# li_1.pop(0)
	for i in li_1:
		i = int(i)
		filename = get_filename(i)
		page_list = get_pagelist(i)
		get_context(i,page_list,filename)


# for i in range(7326886,7326967):
# 	f = open(str(i)+'.txt','w')
# 	r = requests.get(url % i, headers=headers)
# 	r.encoding = 'gbk'
# 	t = r.text
# 	main = t.split('<article id="main">')[1].split('</article>')[0]
# 	head = re.search('h1(.+)h1',main).group()[4:-4].encode('utf-8')
# 	# f.write(head)
# 	main = re.sub('<span(.+)</span>','',main) # remove CopyRight
# 	main = re.sub('(<p></p>)|(</p><p>)','',main) # remove extra '<p>'
# 	context = re.search('<p>(.+)</p>',main,re.DOTALL).group()[4:-4].encode('utf-8')
# 	f.write(context)
#	f.close()


# r = requests.get(url, headers=headers)
# r.encoding = 'gbk'
# t = r.text
# main = t.split('<article id="main">')[1].split('</article>')[0]
# head = re.search('h1(.+)h1',main).group()[4:-4].encode('utf-8')
# main = re.sub('<span(.+)</span>','',main) # remove CopyRight
# main = re.sub('(<p></p>)|(</p><p>)','',main) # remove extra '<p>'
# context = re.search('<p>(.+)</p>',main,re.DOTALL).group()[4:-4].encode('utf-8')