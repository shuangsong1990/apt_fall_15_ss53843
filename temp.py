import json
import sys
import re
import urllib 
import operator
import copy
from bs4 import BeautifulSoup

def contractAsJson(filename):
	jsonQuoteData = {"currPrice": 0.0, "dataUrls": [], "optionQuotes": []}
	
	soup = BeautifulSoup(open(filename),"html.parser")
	mydivs =  soup.find_all('span',class_="time_rtq_ticker") #####this class name can be found in html source page#########
		
	for div in mydivs:
		jsonQuoteData["currPrice"] = float(div.find('span', id="yfs_l84_aapl").text)

	mylinks = soup.find_all('a', attrs={'href': re.compile("\/q\/[a-z]+\?s=[a-zA-Z0-9&;]*m=")})
	
	for link in mylinks:
#		print link['href']
		temp = link['href'].replace('&','&amp;')
		jsonQuoteData["dataUrls"].append("http://finance.yahoo.com"+temp) 


	mytables = soup.find_all('table', class_="yfnc_datamodoutline1")
	
#	print len(mytables)

	num_dict = 0
	dict = {}	
	for table in mytables:
#		print table	

		rows = table.findAll('tr')
		print len(rows)

		for tr in rows:
			cols = tr.findAll(True,{'class':['yfnc_h','yfnc_tabledata1']})
#			cols = tr.find_all(class_=re.compile("yfnc_((h)|(tabledata1))"))
			counter = 1
			for c in cols:
#				print c.text
				if(counter == 1):
					dict["Strike"] = c.text
				elif(counter == 2):
					#list = []
					#list = c.text
					if(str(c.text[:5]) == "AAPL1"):
						dict["Symbol"] = "AAPL"
#						print c.text[4:10]
						dict["Date"] = c.text[4:10]
#						print c.text[10]
						dict["Type"] = c.text[10]
					elif(str(c.text[:5]) == "AAPL7"):
						dict["Symbol"] = c.text[:5]
#						print c.text[5:11]
						dict["Date"] = c.text[5:11]
#						print c.text[11]	
						dict["Type"] = c.text[11]
		
				elif(counter == 3):
					dict["Last"] = c.text
				elif(counter == 4):
					dict["Change"] = c.text
				elif(counter == 5):
					dict["Bid"] = c.text
				elif(counter == 6):
					dict["Ask"] = c.text
				elif(counter == 7):
					dict["Vol"] = c.text
				elif(counter == 8):
					dict["Open"] = int(str(c.text).translate(None,','))
#					print dict["Open"]
				counter = counter + 1

			jsonQuoteData["optionQuotes"].append(dict.copy())
#			num_dict = num_dict + 1
#			if(('Open' in dict.keys()) == False):
#				print dict
		num_dict = num_dict + 1
#		print "table : "
#		print num_dict	
		
	jsonQuoteData["optionQuotes"].sort(key=operator.itemgetter('Open'),reverse=True)
#	print jsonQuoteData["optionQuotes"]
	for x in jsonQuoteData["optionQuotes"]:
		x['Open'] = str(x['Open'])
#		print x['Open'].translate(None,',')
#		print x['Open']	
#	print num_dict
#	jsonQuoteData = "[]"
	print len(jsonQuoteData["optionQuotes"])
	jsonQuoteData = json.dumps(jsonQuoteData)
  	return jsonQuoteData
