import click
import datetime
from datetime import date
from news_extractor import News_Extractor
from constant import Topic, DATEFORMAT


def run():

    news_crawler = News_Extractor()
    print("News crawling started...")

    news_crawler.crawl()


if __name__ == "__main__":
    run()
