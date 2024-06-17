"Basic spider module"

import scrapy
from scrapy.spiders import SitemapSpider
from scrapy.linkextractors import LinkExtractor
from urllib.parse import urlparse

class BasicSpider(SitemapSpider):
    """
    A basic crawler spider that extends Scrapy's CrawlSpider to crawl specified domains
    extracting various webpage components like headings, images, links, etc.

    Attributes:
    - name (str):
        The name of the spider.
    - allowed_domains (list):
        A list of domains that the spider is allowed to crawl.
    - start_urls (list):
        A list of URLs where the spider will begin to crawl from.
    - custom_settings (dict):
        Contains settings such as request concurrency, depth limit, etc.
    """
    name = 'basic_spider'
    sitemap_urls = []
    start_urls = []
    custom_settings = {}

    def __init__(self, *args, **kwargs):
        """
        Initializes the spider and the link extractor with allowed domains.
        """
        self.start_urls = kwargs['start_urls']
        super(BasicSpider, self).__init__(*args,**kwargs)
        self.allowed_domains = [urlparse(url).netloc for url in self.start_urls]
        self.link_extractor = LinkExtractor(allow_domains=self.allowed_domains)

    def parse(self, response: scrapy.http.Response):
        """
        Parses a single webpage and extracts various elements like titles,
        headings, images, links, and more, then yields them as a dictionary.

        @params:
        - response (scrapy.http.Response):
            The response object from which data is extracted.

        @returns:
        - Yields a dictionary with the scraped data.
        """
        headings = {f'h{i}': response.xpath(f'//h{i}/text()').get().strip() for i in range(1, 5)}

        images = [
            {
                'src': img.xpath('@src').get().strip(),
                'alt': img.xpath('@alt').get().strip()
            }
            for img in response.xpath('//img')
        ]

        x_robots_tag = response.headers.get('X-Robots-Tag', b'').decode('utf-8').lower()

        item = {
            'url': response.url,
            'status_code': response.status,
            'response_time': response.meta['download_latency'],
            'title': response.xpath('//title/text()').get().strip(),
            'meta_description': response.css('meta[name="description"]::attr(content)').get().strip(),
            'headings': headings,
            'links': [
                {
                    'url': link.url,
                    'text': link.text.strip()
                }
                for link in response.css('a::attr(href)').getall()
            ],
            'images': images,
            'canonical_link': response.xpath('//link[@rel="canonical"]/@href').get().strip(),
            'robots_meta': response.xpath('//meta[@name="robots"]/@content').get().strip(),
            'x_robots_tag': x_robots_tag,
            'language': response.xpath('/html/@lang').get(),
            'html': response.text
        }
        
        is_indexable = (
            ('noindex' not in (item['robots_meta'] or '').lower()) and
            ('noindex' not in (item['x_robots_tag'] or '').lower()) and
            (item['canonical_link'] == response.url or item['canonical_link'] is None)
        )

        item['is_indexable'] = all(is_indexable)

        yield item

        for link in self.link_extractor.extract_links(response):
            yield response.follow(link, self.parse)

    def closed(self, reason: str):
        """
        Handles final operations after the spider has finished crawling.
        Logs the reason for closing and the count of items scraped.

        @params:
        - reason (str):
            The reason why the spider was closed.
        """
        self.log(
            f"Crawl finished: {reason} with "
            f"{len(self.crawler.stats.get_value('item_scraped_count'))} items scraped.",
            level=scrapy.log.INFO)
