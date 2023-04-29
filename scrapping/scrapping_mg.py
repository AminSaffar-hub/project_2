from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from tqdm import tqdm
import pandas as pd
import time
import re 
from tqdm import tqdm

class ScrapingMG:
    def __init__(self) -> None:
       self.urls ={"Alimentaire": "https://mg.tn/61-promotion", "Hygiène":"https://mg.tn/64-promotion","Marché frais":"https://mg.tn/67-promotion"}
       self.html_file = "output.html"
       self.timer=10
       self.name=[]
       self.link=[]
       self.product_type=[]
       self.price=[]
       self.url=[]

    def scroll_down(self,driver):

        last_height = driver.execute_script("return document.body.scrollHeight")
        while True:
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(self.timer) 
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height :
                break
            last_height = new_height
         
    
    def save_html(self, content):
        with open(self.html_file, "w", encoding="utf-8") as f:
            f.write(content)

    def save_data_frame(self):
        print(len(self.name),len(self.link),len(self.product_type))
        data = {
        'name': self.name,
        'link': self.link,
        'product_type': self.product_type,
        'price': self.price,
        'link_image':self.url
        }
        df = pd.DataFrame(data)
        csv_file = "output_mg.csv"
        df.to_csv(csv_file, index=False)
        return(df)


    def extract_info_per_product(self,link,driver):
        driver.get(link)
        html_content = driver.page_source
        soup = BeautifulSoup(html_content, 'html.parser')
        has_discount_divs = soup.find_all('div', class_='has-discount')
        meta_tag = soup.find('meta', property='og:image')

        if meta_tag:
            image_url = meta_tag['content']
            self.url.append(image_url)
        else:
            self.url.append("Element not found")
        text_=""
        if not has_discount_divs:
            text_="no prices"
        else:    
            for div in has_discount_divs:
                cleaned_text = " ".join(div.text.split())
                text_ = text_ + cleaned_text
        self.price.append(text_)

        
    def main(self):
            driver = webdriver.Chrome()
            for sector_url in tqdm(self.urls.values()):
                driver.get(sector_url)
                self.scroll_down(driver)
                html_content = driver.page_source                
                soup = BeautifulSoup(html_content, 'html.parser')
                product_titles = soup.find_all('h2', class_='h3 product-title')
                product_type= soup.find_all('div',class_='product-category-name text-muted')
                for title,div in zip(product_titles,product_type):
                    self.product_type.append(div.text)
                    link_tag = title.find('a')
                    if link_tag:
                        link = link_tag.get('href')
                        product_name = link_tag.text
                        self.link.append(link)
                        self.extract_info_per_product(link,driver)
                        self.name.append(product_name)
            driver.quit()


if __name__ == "__main__":
    scraper = ScrapingMG()
    scraper.main()
    data_frame=scraper.save_data_frame()
    print(data_frame)


        