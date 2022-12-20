import selenium
import scrapy
from selenium import webdriver
from scrapy import Selector
from selenium.webdriver.common.by import By
import time

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-gpu")

class PULScraper():
    def __init__(self):
        self.webdriver = webdriver.Chrome(options=chrome_options)
        self.scraped_lines = []
        #dictionary of category to list of pickuplines
        # get rid of the number though
    
    def scrape_for_links(self):
        self.webdriver.get('https://pickupline.net/')
        entry_content = self.webdriver.find_element('xpath', "//div[@class='entry-content']")
        self.category_links = []
        categories = entry_content.find_elements('xpath', ".//div[@class='pt-cv-title']")
        print(len(categories))       
        for category in categories:
            link = category.find_element("xpath",'.//a[@href]')
            self.category_links.append(link)
        print(len(self.category_links))
    

    def scrape_for_cateogry(self):
        for link in self.category_links:
            link.click()
            time.sleep(5.0)
            entry_content = self.webdriver.find_element('xpath', "//div[@class='entry-content']")
            self.subcategory_links = {}
            categories = entry_content.find_elements('xpath', ".//div[@class='pt-cv-title']")    
            for category in categories:
                link = category.find_element("xpath",'.//a[@href]')
                subcategory = None
                self.subcategory_links[subcategory] = link
            self.scrape_for_pick_lines()
            

    def scrape_for_pick_lines(self):
        for k, v in self.subcategory_links.items():
            v.click()
            time.sleep(5.0)
            table = self.driver.find_element('xpath', "//div[@class='dataTables_wrapper no-footer']")
            table_press = table.find_element('xpath', './/div[contains(@class, "tablepress")')
            line_els = table_press.find_elements(By.TAG_NAME('tr'))
            for line in line_els:
                pick_up_list = ["<<", k, ">>"]
                pick_up_selector = Selector(text=line.get_attribute('outerHTML'))
                pick_up_line = pick_up_selector.xpath('.//td[@class="column-1"]/text()').get(default='').strip()
                pick_up_list.append(pick_up_line)
                self.scraped_lines.append("".join(pick_up_list))
    
    def write_to_file():
        pass


