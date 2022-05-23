# information_integration_2022

# general architecture
The google news crawler is based on the general functionality of the rb_crawler.
It crawls the rss feed of google news via specific keywords we set for every day ytd 2022.
This is necesseray since the rss feed is limited to 100 entries per request. 
The keywords got set to cover a broad spectrum of news about (german) companies.

keywords = [
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


Adding the date via a start and end-date the query looks something like:
https://news.google.com/rss/search?q=" + keyword + "+after:" + start_date.strftime(dateformat) + "+before:" + end_date.strftime(dateformat) + "&ceid=DE:de&hl=de&gl=DE

So the crawler iterates over each keyword for every date ytd.

example query: 
https://news.google.com/rss/search?q=Wirtschaft+after:2022-01-01+before:2022-01-02&ceid=DE:de&hl=de&gl=DE

The xml gets parsed and sent via protobuff to kafka.

# how2run

