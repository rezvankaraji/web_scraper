install:
pip install scrapy
pip install scrapy-random-useragent

run:
scrapy crawl houzz.co.uk -a page_limit=n -o houzz.json
%%% put your favourite number instead of n :))) %%%
