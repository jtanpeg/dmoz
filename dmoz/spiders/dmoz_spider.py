from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector

from dmoz.items import DmozItem

class DmozSpider(BaseSpider):
	name = "dmoz.org"
	allowed_domains = ["dmoz.org"]
	start_urls = [
		"http://www.dmoz.org/Computers/Programming/Languages/Python/Books/",
        "http://www.dmoz.org/Computers/Programming/Languages/Python/Resources/"
	]

	def parse(self, response):
		hxs = HtmlXPathSelector(response) #initiate the selectors
		sites = hxs.select('//ul[@class="directory-url"]/li')  #change this to select ul of class "directory-url"
		items = []		
		for site in sites:
			item = DmozItem()
			item['title'] = site.select('a/text()').extract()
			item['link'] = site.select('a/@href').extract()
			item['desc'] = site.select('text()').extract() #something is still wrong with description since its collecting the \t and \n elements
#i.e., ignore spaces, tabs, and new line breaks
			items.append(item)
		return items
