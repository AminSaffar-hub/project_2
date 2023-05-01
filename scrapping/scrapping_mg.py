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
       self.urls ={"food": "https://mg.tn/61-promotion", "self-care":"https://mg.tn/64-promotion","appliances":"https://mg.tn/67-promotion"}
       self.html_file = "output_mg.html"
       self.timer=10
       self.name=[]
       self.link=[]
       self.product_type=[]
       self.description=[]
       self.price=[]
       self.new_price=[]
       self.old_price=[]
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
        'old_price': self.old_price,
        'new_price': self.new_price,
        'image_link':self.url,
        'url': self.link,
        'description': self.description,
        'product_type': self.product_type
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

    def fix_info_df(self):
        no_price_indices = [i for i, price in enumerate(self.price) if price == "no prices"]
        for index in sorted(no_price_indices, reverse=True):
            del self.name[index]
            del self.link[index]
            del self.price[index]
            del self.url[index]
            del self.product_type[index]
        for element in self.price:
            numbers_str = re.findall(r'\d+\s*,\s*\d+', element)
            number1_str = numbers_str[0].replace(",", ".").replace(" ", "")
            number2_str = numbers_str[1].replace(",", ".").replace(" ", "")
            number1 = float(number1_str)
            number2 = float(number2_str)
            if number1 > number2:
                self.new_price.append(number1)
                self.old_price.append(number1+number2)
            else:
                self.new_price.append(number1)
                self.old_price.append(number2)
       
    def main(self):
            driver = webdriver.Chrome()
            for sector_url,div in tqdm(zip(self.urls.values(),self.urls.keys())):
                driver.get(sector_url)
                self.scroll_down(driver)
                html_content = driver.page_source                
                soup = BeautifulSoup(html_content, 'html.parser')
                product_titles = soup.find_all('h2', class_='h3 product-title')
                for title in product_titles:
                    self.product_type.append(div)
                    link_tag = title.find('a')
                    if link_tag:
                        link = link_tag.get('href')
                        product_name = link_tag.text
                        self.link.append(link)
                        self.extract_info_per_product(link,driver)
                        self.name.append(product_name)
            driver.get(self.link[0])
            html_content = driver.page_source
            self.save_html(html_content)      
            driver.quit()


if __name__ == "__main__":
    scraper = ScrapingMG()
    scraper.main()
    scraper.fix_info_df()
    data_frame=scraper.save_data_frame()
    print(data_frame.head())


        