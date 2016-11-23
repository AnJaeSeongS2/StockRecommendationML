import BeautifulSoup


def downloadCode(self, market_type):
	url = 'http://datamall.koscom.co.kr/servlet/infoService/SearchIssue'
	html = requests.post(url, data= {'flag':'SEARCH', 'marketDisabled': 'null','marketBit':market_type})
	return html.content

def parseCodeHTML(self, html, market_type):
	soup = BeautifulSoup.BeautifulSoup(html)
	options = soup.findAll('option')
	codes = StockCode()
	for a_option in options:
		if len(a_option) ==0:
			continue
		code = a_option.text[1:7]
		company = a_option.text[8:]
		full_code = a_option.get('value')

	codes.add(market_type, code,full_code, company)
	return codes

class StockCode:
	def __init__(self):
		self.items ={}
	
	def count(self):
		return len(self.items)

	def clear(self):
		self.items.clear()

	def add(self,market_type, code, full_code, company):
		a_item = StockCodeItem(market_type, code, full_code, company)
		self.items[code] = a_item
		
	def remove(self, stock_code):
		del self.items[stock_code]

	def find (self, stock_code):
		return self.items[stock_code]
	
	def iterItems(self):
		return self.items.iteritems()

	def dump(self):
		index = 0
		for key, value in self.items.iteritems():
			print "%s : %s - Code = %s, Full Code = %s, Company = %s" % (index, value.market_type, key, value.full_code, value.company)
			index +=1

	
