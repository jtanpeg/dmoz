#The googledir spider crawls the entire Google directory, though you may want to
#limit the crawl to a certain number of items
#to limit to 20 items: scrapy crawl googledir --set CLOSESPIDER_ITEMPASSED=20

from scrapy.selector import HtmlXPathSelector
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.loader import XPathItemLoader

from dirbot.items import Website

class GoogledirSpider(CrawlSpider):

    name = 'googledir'
    allowed_domains = ['directory.google.com']
    start_urls = ['http://directory.google.com/']

    rules = (
        Rule(SgmlLinkExtractor(allow='directory.google.com/[A-Z][a-zA-Z_/]+$'),
            'parse_category',
            follow=True,
        ),
    )
    
    def parse_category(self, response):
        # The main selector we're using to extract data from the page
        main_selector = HtmlXPathSelector(response)

        # The XPath to website links in the directory page
        xpath = '//td[descendant::a[contains(@href, "#pagerank")]]/following-sibling::td/font'

        # Get a list of (sub) selectors to each website node pointed by the XPath
        sub_selectors = main_selector.select(xpath)

        # Iterate over the sub-selectors to extract data for each website
        for selector in sub_selectors:
            item = Website()

            l = XPathItemLoader(item=item, selector=selector)
            l.add_xpath('name', 'a/text()')
            l.add_xpath('url', 'a/@href')
            l.add_xpath('description', 'font[2]/text()')

            # Here we populate the item and yield it
            yield l.load_item()
