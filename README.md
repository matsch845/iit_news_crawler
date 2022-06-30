# information_integration_2022

## general architecture
The google news crawler is based on the general functionality of the rb_crawler. Found here: 
https://github.com/bakdata/hpi-ii-project-2022
It crawls the rss feed of google news via specific keywords.
The keywords are set to the extracted rb_companies.


example query: 
https://news.google.com/rss/search?q=Apple

The xml gets parsed and sent via protobuff to kafka.

more details in presentation.

## how2run
1. `poetry install`
2. `poetry run python main.py
