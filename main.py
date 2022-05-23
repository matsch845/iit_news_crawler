import click
import datetime
from datetime import date
from news_extractor import News_Extractor
from constant import Topic, DATEFORMAT

@click.command()
@click.option("-s", "--start_date", type=str, help="The earliest publication date of an article (format YYYY-MM-DD)")
@click.option("-e", "--end_date", type=str, help="The last publication date of an article (format YYYY-MM-DD). If this option is not provided, it defaults to the current date")
def run(start_date: str, end_date: str):
    if(start_date is None):
        print("No valid start date provided")
        exit(1)
    
    try:
        s_date = datetime.datetime.strptime(start_date, DATEFORMAT).date()
    except:
        print("No valid start date provided. Please use the following format: YYYY-MM-DD")
        exit(1)
    
    if(end_date is None):
        e_date = date.today()
    else:
        try:
            e_date = datetime.datetime.strptime(end_date, DATEFORMAT).date()
        except:
            print("No valid end date provided. Please use the following format: YYYY-MM-DD")
            exit(1)

    news_crawler = News_Extractor()
    print("News crawling started (" + s_date.strftime(DATEFORMAT) + " - " + e_date.strftime(DATEFORMAT) + ")")
    
    news_crawler.crawl(s_date, e_date)

if __name__ == "__main__":
    run()