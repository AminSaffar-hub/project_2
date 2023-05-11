from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from tqdm import tqdm
import pandas as pd
import time
import re 
from tqdm import tqdm
class ScrapingAziza:
    def __init__(self) -> None:
       self.urls ="https://aziza.tn/fr/home"
       self.html_file = "output_azziza.html"
       self.timer=10
       self.name=[]
       self.link=[]
       self.product_type=[]
       self.price=[]
       self.url=[]

    def save_html(self,content):
            with open(self.html_file, "w", encoding="utf-8") as f:
                f.write(content)
    def main(self):
        driver = webdriver.Chrome()
        driver.get(self.urls)
        html_content = driver.page_source 
        self.save_html(html_content) 

    
if __name__ == "__main__":
    scraper = ScrapingAziza()
    scraper.main()

