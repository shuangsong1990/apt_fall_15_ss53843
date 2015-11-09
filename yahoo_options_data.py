import json
import sys
import re
import urllib 
import operator
import copy
from bs4 import BeautifulSoup

def contractAsJson(filename):
	jsonQuoteData = {"currPrice": 0.0, "dateUrls": [], "optionQuotes": []}
#	jsonQuoteData = {"optionQuotes": []}
	
	soup = BeautifulSoup(open(filename),"html.parser")
	mydivs =  soup.find_all('span',class_="time_rtq_ticker") #####this class name can be found in html source page#########
		
	for div in mydivs:
		jsonQuoteData["currPrice"] = float(div.find('span', id=re.compile("yfs_l84_*")).text)
		#print float(div.find('span', id=re.compile("yfs_l84_*")).text)

	mylinks = soup.find_all('a', attrs={'href': re.compile("\/q\/[a-z]+\?s=[a-zA-Z0-9&;]*m=")})
	
	for link in mylinks:
		temp = link['href'].replace('&','&amp;')
		jsonQuoteData["dateUrls"].append("http://finance.yahoo.com"+temp) 
	mytables = soup.find_all('table', class_="yfnc_datamodoutline1")

	num_dict = 0
	
	dict = {}	
	for table in mytables:
		cols = table.find_all(True, {'class':['yfnc_h','yfnc_tabledata1']})
		counter = 1
		for c in cols:
			if(counter == 1):
				dict["Strike"] = str(c.text)
			elif(counter == 2):
				#list = []
				#list = c.text
				#if(str(c.text[:5]) == "AAPL1"):
				#	dict["Symbol"] = "AAPL"
				#	dict["Date"] = c.text[4:10]
				#	dict["Type"] = c.text[10]
				#	print c.text[10]
				#elif(str(c.text[:5]) == "AAPL7"):
				dict["Symbol"] = str(c.text[:-15])
				dict["Date"] = str(c.text[-15:-9])
				dict["Type"] = str(c.text[-9:-8])
				#	print c.text[11]		
			elif(counter == 3):
				dict["Last"] = str(c.text)
			elif(counter == 4):
				dict["Change"] = str(c.text)
			elif(counter == 5):
				dict["Bid"] = str(c.text)
			elif(counter == 6):
				dict["Ask"] = str(c.text)
			elif(counter == 7):
				dict["Vol"] = str(c.text)
			elif(counter == 8):
				dict["Open"] = str(c.text) #int(str(c.text).translate(None,','))
				counter = 0
				jsonQuoteData["optionQuotes"].append(dict.copy())
			counter = counter + 1

	jsonQuoteData["optionQuotes"].sort(key=lambda a: int(str(a["Open"]).translate(None,',')),reverse=True)		
#	jsonQuoteData["optionQuotes"].sort(key=operator.itemgetter('Open'),reverse=True)
#	for x in jsonQuoteData["optionQuotes"]:
#		x['Open'] = str(x['Open']) 
	
	jsonQuoteData = json.dumps(jsonQuoteData)
	return jsonQuoteData
