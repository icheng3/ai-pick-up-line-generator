import selenium
import scrapy
from selenium import webdriver
from scrapy import Selector
from selenium.webdriver.common.by import By
import time
import concurrent.futures
 

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-gpu")

class PULScraper():
    def __init__(self):
        self.webdriver = webdriver.Chrome(options=chrome_options)
        self.scraped_lines = set()
    
    def scrape_for_links(self):
        self.webdriver.get('https://pickupline.net/')
        entry_content = self.webdriver.find_element('xpath', "//div[@class='entry-content']")
        self.category_links = []
        categories = entry_content.find_elements('xpath', ".//div[@class='pt-cv-title']")
        print(len(categories))       
        for category in categories:
            link = category.find_element("xpath",'.//a[@href]')
            link = link.get_attribute('href')
            self.category_links.append(link)
        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
            executor.map(self.scrape_for_cateogry, self.category_links)
    
    def get_subcategory(self, text):
        subcategory = text.split(' ', 1)[-1]
        subcategory = subcategory.split('Pick')[0]
        return subcategory


    def scrape_for_cateogry(self, link):
        print('scraping for link', link)
        self.webdriver.get(link)
        entry_content = self.webdriver.find_element('xpath', "//div[@class='entry-content']")
        self.subcategory_links = {}
        categories = entry_content.find_elements('xpath', ".//div[@class='pt-cv-title']")    
        for category in categories:
            link = category.find_element("xpath",'.//a[@href]')
            text = link.text
            subcategory = self.get_subcategory(text)
            link = link.get_attribute('href')
            self.subcategory_links[subcategory] = link
        self.scrape_for_pick_lines()
            

    def scrape_for_pick_lines(self):
        for k, v in self.subcategory_links.items():
            self.webdriver.get(v)
            even = self.webdriver.find_elements('xpath', './/tr[contains(@class, "even")]')
            odd = self.webdriver.find_elements('xpath', './/tr[contains(@class, "odd")]')[1:]
            for line in even:
                pick_up_list = ["<<", k, ">>"]
                pick_up_selector = Selector(text=line.get_attribute('outerHTML'))
                pick_up_line = pick_up_selector.xpath('.//td[@class="column-1"]/text()').get(default='').strip()
                pick_up_list.append(pick_up_line)
                self.scraped_lines.add("".join(pick_up_list))
            for line in odd:
                pick_up_list = ["<<", k, ">>"]
                pick_up_selector = Selector(text=line.get_attribute('outerHTML'))
                pick_up_line = pick_up_selector.xpath('.//td[@class="column-1"]/text()').get(default='').strip()
                pick_up_list.append(pick_up_line)
                self.scraped_lines.add("".join(pick_up_list))
    
    def write_to_file(self):
        join_string = f"\n{'*'*50}\n"
        with open('pickup_training_data.txt', 'w') as f:
            f.write(join_string.join(self.scraped_lines))
        print('done!')


    def scrape_more_lines(self):
        self.webdriver.get('https://www.scarymommy.com/lifestyle/pick-up-lines-for-girls')
        lines = self.webdriver.find_element('xpath', "//div[@class='AOL Afg']")
        lines = lines.find_elements(By.TAG_NAME, 'li')
        for line in lines:
            pick_up_list = ["<<", 'random', ">>"]
            pick_up_list.append(line.text)
            self.scraped_lines.add("".join(pick_up_list))
    
