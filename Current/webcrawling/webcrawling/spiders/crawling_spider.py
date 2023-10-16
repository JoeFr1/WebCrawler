from pymongo import MongoClient
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor


class CrawlingSpider(CrawlSpider):
    # Define a web crawling spider for scraping articles from the BBC website
    name = "bbc_spider"
    allowed_domains = ["bbc.com"]
    start_urls = ["https://www.bbc.com/"]

    rules = (
        Rule(LinkExtractor(allow=""), callback="parse_items"),
    )

    def parse_items(self, response):
        # Extract title of the article
        title = response.css(".e1mcntqj3 h1::text").get()

        # Extract the author's name, or set it not "Author Not Available" if not found
        author = response.css("div.ssrcss-68pt20-Text-TextContributorName.e8mq1e96::text").get()
        if author is None:
            author = "Author not Available"

        # Get the URL of the current page
        url = response.request.url

        # Initialize content
        text_content = ""

        # Check if post is a video (Contains /av in URL)
        if "/av" in url:
            # Loop through the divs with specified class
            for div in response.css('div.ssrcss-1s1kjo7-RichTextContainer.e5tfeyi1'):
                # Extract text from all p elements within div
                div_text = ''.join(div.css('p::text').getall())
                text_content += div_text

        else:
            # Loop through first div with class
            for div in response.css('div.ssrcss-11r1m41-RichTextContainer.e5tfeyi1'):
                # Extract text from all p elements
                div_text = ''.join(div.css('p::text').getall())
                text_content += div_text

            # Loop through the second div with class
            for div in response.css('div.ssrcss-7uxr49-RichTextContainer.e5tfeyi1'):
                # Extract text from all p and a elements within div
                div_text = ''.join(div.css('p::text').getall())
                div_text = ''.join(div.css('a::text').getall())
                text_content += div_text

        if title is not None:
            # Create a dictionary with extracted data
            data = {
                "title": title,
                "Author": author.replace("By ", ""),
                "URL": url,
                "Content": text_content
            }
        client = MongoClient(
            "mongodb+srv://josephf:4tqqTe1wjnBYbUg4@cluster.muizicl.mongodb.net/?retryWrites=true&w=majority"
        )
        db = client.webscrap
        bbc = db.bbcscrap
        bbc.insert_one(data)
