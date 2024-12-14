"""
Main crawler used for crawling pages and getting all the needed links. 
"""

import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from multiprocessing import Process, Queue 
from urllib.parse import urlparse
import tldextract
import os 
from pathlib import Path

class LinkExtractorSpider(CrawlSpider):
    """Simple Spider to crawl a website to a given depth"""
    
    name = "link_extractor_spider"

    def __init__(self, start_url, allowed_domains, max_depth, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.start_urls = [start_url]
        self.allowed_domains = allowed_domains
        self.max_depth = int(max_depth)
        self.link_extractor = LinkExtractor(allow_domains=self.allowed_domains)
        self.rules = [
            Rule(self.link_extractor, callback='parse_links', follow=True)
        ]
        self._compile_rules()

    def parse_links(self, response):
        current_depth = response.meta.get('depth', 0)
        if current_depth <= self.max_depth:
            links = self.link_extractor.extract_links(response)
            yield {
                'sitemap': response.url,
                'pagetitle': response.css('title::text').get(),
                'links': {link.text: link.url for link in links}
            }

    def _requests_to_follow(self, response):
        if response.meta.get('depth', 0) >= self.max_depth:
            return
        return super()._requests_to_follow(response)

def run_links_extractor(start_url, allowed_domains, max_depth=1, output_file_name="links_output.json"):
    """Sets up the crawler to save outputs to a file. This can be later saved into a database"""
    process = CrawlerProcess(settings={
        "FEEDS": {
            output_file_name: {"format": "json"},
        },
        "LOG_LEVEL": "INFO",
    })
    process.crawl(LinkExtractorSpider, start_url=start_url, allowed_domains=allowed_domains, max_depth=max_depth)
    process.start()



def crawl_threaded_process(start_url, allowed_domains, max_depth=1, output_file_name="links_output.json"):
    """
    Was created to enable multithreading to allow multiple uses but some errors accoring as of now. 
    Just gonna park it for now
    """
    
    p1 = Process(target=run_links_extractor, args=(start_url, allowed_domains, max_depth, output_file_name))
    p1.start()
    p1.join()
    return output_file_name

def run_crawl_process(start_url, allowed_domains=[], max_depth=2, save_directory=".cache/links_cache"):
    """
    Single Call Crawler. Sadly can't be reused unless called from main with a new thread
    """
    Path(save_directory).mkdir(parents=True, exist_ok=True)
    
    primary_domain = tldextract.extract(start_url).registered_domain
    allowed_domains.append(primary_domain)
    output_file_name = os.path.join(save_directory,f"{primary_domain}.json")
    
    with open(output_file_name, 'w') as ff:
        ff.write('')
    
    
    run_links_extractor(start_url, allowed_domains, max_depth, output_file_name)

    
    print(f"Crawled {start_url}, URLs saved to  {output_file_name}")
    
    return output_file_name
    
    


# if __name__=="__main__":
#     run_crawl_process(start_url="https://www.joveo.com/")
#     print(f"Completed Joveo, switching to gihub")
#     run_crawl_process("https://www.github.com/")
#     print("Completed github")