from abc import ABC


class SearchEngineScraper(ABC):
    def scrape(self, company_names):
        pass


class ScraperClient:
    def __init__(self, scraper_strategy):
        self.scraper_strategy = scraper_strategy

    def set_strategy(self, scraper_strategy):
        self.scraper_strategy = scraper_strategy

    def scrape(self, company_names):
        self.scraper_strategy.scrape(company_names)
