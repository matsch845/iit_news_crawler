import logging
from time import sleep
from datetime import date, datetime, timedelta

# import elementpath
import lxml.etree as etree
from lxml.etree import fromstring

import requests

from news_producer import News_Producer
from build.gen.article_pb2 import Article

import pandas as pd

from elasticsearch import Elasticsearch
from elasticsearch.helpers import scan

import urllib.parse

from constant import DATEFORMAT

log = logging.getLogger(__name__)

es = Elasticsearch(['localhost:9200'])

es.info()


class News_Extractor:
    def __init__(self):
        self.news_producer = News_Producer()
        self.keywords = []

    def get_data_from_elastic(self, table_name):
        query = {
            "query": {
                "match_all": {}
            }
        }

        rel = scan(client=es,
                   query=query,
                   scroll='1m',
                   index=table_name,
                   raise_on_error=True,
                   preserve_order=False,
                   clear_scroll=True)

        result = list(rel)
        temp = []

        for hit in result:
            temp.append(hit['_source'])

        df = pd.DataFrame(temp)
        return df

    def crawl(self):
        df_rb = self.get_data_from_elastic("corporate-events-full")

        for i in range(0, 20000):
            rb_id = df_rb["id"][i]
            info = df_rb["information"][i]

            keyword = self.find_company(info)
            rb_id = rb_id

            self.crawl_by_keyword_and_date(keyword, rb_id)

    def find_company(self, inp):
        start = inp.find(":")
        end = inp.find(",")
        company = inp[start + 2:end]

        if (len(company) == 0):
            company = inp[0:inp.find(",")]

        return company

    def crawl_by_keyword_and_date(self, keyword, rb_id):
        try:
            text, url = self.send_request(keyword)

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

                    article.search_keyword = keyword + "%" + rb_id
                    article.search_url = url
                    # print(article.title + " " + keyword + " " + url)
                    # print("-------------------------------------------------------")

                    self.news_producer.produce_to_topic(article)


        except Exception as ex:
            print(ex)
            log.error(f"Error")

    def send_request(self, keyword) -> str:
        keyword = urllib.parse.quote(keyword)

        url = f"https://news.google.com/rss/search?q=" + keyword + "&ceid=DE:de&hl=de&gl=DE"

        print("used url: " + url)

        return requests.get(url=url).text, url
