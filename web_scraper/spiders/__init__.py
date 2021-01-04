# This package will contain the spiders of your Scrapy project
#
# Please refer to the documentation for information on how to create and manage
# your spiders.

import scrapy
from web_scraper.items import WebScraperItem


class Spider(scrapy.Spider):
    name = "houzz.co.uk"
    start_urls = [
        "https://www.houzz.com/products/beds",
        "https://www.houzz.com/products/chairs",
        "https://www.houzz.com/products/dining-tables",
        "https://www.houzz.com/products/sofas-and-sectionals",
    ]

    def parse(self, response):
        for url in self.start_urls:
            yield scrapy.Request(url=url, callback=self.parse_product)

        next_page = response.css(".hz-pagination-link--next::attr(href)").get()
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)

    def parse_product(self, response):
        urls = response.css(".hz-product-card__link::attr(href)").getall()
        for url in urls:
            yield response.follow(url, callback=self.parse_item)

    def parse_item(self, response):
        item = WebScraperItem()
        # url
        item["url"] = response.url

        # title
        item["title"] = response.css(".view-product-title::text").get()

        # image
        thumb_urls = response.css(".alt-images__thumb img::attr(src)").getall()
        first_image_url = response.css(".view-product-image-print::attr(src)").get()
        image_urls = first_image_url

        try:
            first_code = first_image_url.split("/")[-2].split("_")[0]
            image_urls = []

            for thumb_url in thumb_urls:
                try:
                    code = thumb_url.split("/")[-1].split("_")[0]
                    image_urls.append(first_image_url.replace(first_code, code))
                except:
                    pass
        except:
            pass

        item["images"] = image_urls[:2]

        # key words
        item["keywords"] = response.css(".product-keywords__word::text").getall()

        # description
        item["description"] = (
            " ".join(response.css(".vp-redesign-description::text").getall())
            + " "
            + ",".join(response.css(".description-item::text").getall())
        )

        yield item

