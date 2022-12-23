from PULScraper import PULScraper

scraper = PULScraper()
scraper.scrape_for_links()
scraper.scrape_more_lines()
scraper.write_to_file()