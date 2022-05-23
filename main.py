# information from https://stackoverflow.com/questions/51537063/url-format-for-google-news-rss-feed
# 
# possible endpoints (rss):
# https://news.google.com/news/rss/headlines/section/topic/{topic} where topic has to be one of these: WORLD NATION BUSINESS TECHNOLOGY ENTERTAINMENT SPORTS SCIENCE HEALTH
# https://news.google.com/rss/search?q={query} (BUT: not allowed to use (robot.txt))


# https://news.google.com/rss/search?q=Wirtschaft+after:2020-06-02+before:2020-06-10&ceid=DE:de&hl=de&gl=DE

import click
from news_extractor import News_Extractor
from constant import Topic

@click.command()
#@click.option("-s", "--startDate", type=str, help="The earliest publication date of an article")
#@click.option("-t", "--topic", type=click.Choice(Topic), help="A specific topic the articles should be filtered by")
def run():
    news_crawler = News_Extractor()
    print("Google News crawling started ...")
    news_crawler.crawl()

if __name__ == "__main__":
    run()