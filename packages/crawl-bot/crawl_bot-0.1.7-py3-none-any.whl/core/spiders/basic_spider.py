"Basic spider module"

from urllib.parse import urlparse

import scrapy


class BasicSpider(scrapy.spiders.SitemapSpider):
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

    def __init__(self, start_urls: list|str, *args, **kwargs):
        """
        Initializes the spider and the link extractor with allowed domains.
        """
        super().__init__(*args, **kwargs)
        self.start_urls = [start_urls] if isinstance(start_urls, str) else start_urls
        self.allowed_domains = [urlparse(url).netloc for url in self.start_urls]
        self.link_extractor = scrapy.linkextractors.LinkExtractor(allow_domains=self.allowed_domains)

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
        self.logger.info('Got successful response from {}'.format(response.url))

        headings = {f'h{i}': response.xpath(f'//h{i}/text()').get() for i in range(1, 5)}

        images = [
            {
                'src': img.xpath('@src').get(),
                'alt': img.xpath('@alt').get()
            }
            for img in response.xpath('//img')
        ]

        x_robots_tag = response.headers.get('X-Robots-Tag', b'').decode('utf-8').lower()

        item = {
            'url': response.url,
            'status_code': response.status,
            'response_time': response.meta['download_latency'],
            'title': response.xpath('//title/text()').get(),
            'meta_description': response.css('meta[name="description"]::attr(content)').get(),
            'headings': headings,
            'links': [
                {
                    'url': link.url,
                    'text': link.text
                }
                for link in response.css('a::attr(href)').getall()
            ],
            'images': images,
            'canonical_link': response.xpath('//link[@rel="canonical"]/@href').get(),
            'robots_meta': response.xpath('//meta[@name="robots"]/@content').get(),
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
