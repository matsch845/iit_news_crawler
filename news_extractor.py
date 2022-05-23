import logging
from time import sleep
from datetime import date, datetime, timedelta

#import elementpath
import lxml.etree as etree
from lxml.etree import fromstring

import requests
from parsel import Selector

from news_producer import News_Producer
from build.gen.article_pb2 import Article

from constant import DATEFORMAT


log = logging.getLogger(__name__)

class News_Extractor:
    def __init__(self):
        self.news_producer = News_Producer()
        self.keywords = [
            "Wirtschaft", 
            "Politik", 
            "Firma", 
            "Umsatz", 
            "Gewinn", 
            "Neueintragung", 
            "Skandal",
            "Management",
            "Konzern",
            "Unternehmen",
            "Covid",
            "Betrieb",
            "Aktionäre",
            "Ukraine",
            "Russland",
            "Öl",
            "Preise"]

    def crawl(self, start_date: date, end_date: date):
        delta = timedelta(days=1)

        while start_date <= end_date:
            for keyword in self.keywords:
                end_date_temp = start_date + delta

                print("crawling keyword " + keyword + " within daterange: " + start_date.strftime(DATEFORMAT) + " - " + end_date_temp.strftime(DATEFORMAT) )
                
                self.crawl_by_keyword_and_date(keyword, start_date, end_date_temp)
                sleep(0.5)

            start_date += delta

    def crawl_by_keyword_and_date(self, keyword, start_date, end_date):
        try:
            text, url = self.send_request(keyword, start_date, end_date)
            
            xml = text.encode('utf-8')
            parser = etree.XMLParser(ns_clean=True, recover=True, encoding='utf-8')
            root = fromstring(xml, parser=parser)

            for channel in root:
                print("Items found: " + str(len(channel)))

                for item in channel:
                    if item is None or len(item) < 1:
                        continue

                    article = Article()

                    for elem in item:
                        if elem is None or elem.tag is None:
                            print("elem null!!!!")

                        if elem.tag == "title":
                            article.title = elem.text

                        if elem.tag == "link":
                            article.link = elem.text
                        
                        if elem.tag == "guid":
                            article.id = elem.text

                        if elem.tag == "pubDate":
                            article.publication_date = elem.text
                        
                        if elem.tag == "description":
                            article.description = elem.text
                        
                        if elem.tag == "source":
                            article.source = elem.text

                    article.search_keyword = keyword
                    article.search_url = url
                    # print(article.title + " " + keyword + " " + url)
                    # print("-------------------------------------------------------")
                    
                    self.news_producer.produce_to_topic(article)


        except Exception as ex:
            print(ex)
            log.error(f"Error")

    def send_request(self, keyword, start_date, end_date) -> str:
        url = f"https://news.google.com/rss/search?q=" + keyword + "+after:" + start_date.strftime(DATEFORMAT) + "+before:" + end_date.strftime(DATEFORMAT) + "&ceid=DE:de&hl=de&gl=DE"

        print("used url: " + url)

        return requests.get(url=url).text, url
