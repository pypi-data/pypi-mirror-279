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

    def __init__(self, start_urls: list|str = None, *args, **kwargs):
        """
        Initializes the spider and the link extractor with allowed domains.
        """
        super().__init__(*args, **kwargs)
        self.start_urls = [start_urls] if isinstance(start_urls, str) else start_urls
        self.allowed_domains = [urlparse(url).netloc for url in self.start_urls]
        self.link_extractor = scrapy.linkextractors.LinkExtractor(allow_domains=self.allowed_domains)
        self.logger.info(
            f"Initialized spider with start URLs: {self.start_urls} "
            f"and allowed domains: {self.allowed_domains}")

    def start_requests(self):
        for url in self.start_urls:
            self.logger.info(f"Generating direct request for {url}")
            yield scrapy.Request(url=url, callback=self.parse)

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
        parsed_url = urlparse(response.url)

        # Full URL without query string
        url_full = f"{parsed_url.scheme}://{parsed_url.netloc}{parsed_url.path}"

        # Only the path part of the URL
        url_path = parsed_url.path if parsed_url.path else None

        # Parameters attached to the URL (semicolon-separated values in the path)
        url_params = parsed_url.params if parsed_url.params else None

        x_robots_tag = response.headers.get('X-Robots-Tag', None)
        x_robots_tag = x_robots_tag.decode('utf-8') if x_robots_tag else x_robots_tag

        headings = {
            f'h{i}': response.xpath(f"normalize-space(//h{i}/text())").get() or None
            for i in range(1, 5)
        }

        images = [
            {
                'src': img.xpath('@src').get(),
                'alt': img.xpath('@alt').get()
            }
            for img in response.xpath('//img')
        ]

        links = [
            {
                'url': response.urljoin(link),
                'text': response.xpath(f"normalize-space(//a[@href='{link}']/text())").get()
            }
            for link in response.css('a::attr(href)').getall()
        ]

        item = {
            'url_full': url_full,
            'url_path': url_path,
            'url_params': url_params,
            'status_code': response.status,
            'response_time': response.meta.get('download_latency'),
            'title': response.xpath('normalize-space(//title/text())').get(),
            'meta_description': response.css('meta[name="description"]::attr(content)').get(),
            'headings': headings,
            'links': links,
            'images': images,
            'canonical_link': response.xpath('//link[@rel="canonical"]/@href').get(),
            'robots_meta': response.xpath('//meta[@name="robots"]/@content').get(),
            'x_robots': x_robots_tag,
            'language': response.xpath('/html/@lang').get(),
            'depth': response.meta.get('depth', 0),
            'html': response.text
        }

        yield item

        for link in self.link_extractor.extract_links(response):
            yield response.follow(link, self.parse)
