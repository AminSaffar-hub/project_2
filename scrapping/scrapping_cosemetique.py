from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from tqdm import tqdm
import pandas as pd
import time
import re 
from tqdm import tqdm
class Scrapingcosme:
    def __init__(self) -> None:
       self.urls =["https://cosmetique.tn/promotions","https://cosmetique.tn/countdown/Vente_Flash"]
       self.html_file = "output_cos_1.html"
       self.name=[]
       self.image_link=[]
       self.product_type=[]
       self.product_description=[]
       self.old_price=[]
       self.new_price=[]
       self.url=[]
    
    def save_data_frame(self):
        #print(len(self.name))
        #print(len(self.old_price))
        #print(len(self.new_price))
        #print(len(self.image_link))
        #print(len(self.url))
        #print(len(self.product_description))
        data = {
        'name': self.name,
        'old_price': self.old_price,
        'new_price': self.new_price,
        'image link': self.image_link,
        'url':self.url,
        'desription': self.product_description
        }
        df = pd.DataFrame(data)
        csv_file = "output_cos.csv"
        df.to_csv(csv_file, index=False)
        return(df)
    def save_html(self,content):
            with open(self.html_file, "w", encoding="utf-8") as f:
                f.write(content)
    def scrap_promotion(self):
        driver = webdriver.Chrome()
        driver.get(self.urls[0])
        html_content = driver.page_source 
        soup = BeautifulSoup(html_content, 'html.parser')
        for h3 in soup.find_all('h3', class_='product-title h5 text-center overflow-hidden mt-2'):
            product_link = h3.find('a')['href']
            product_name = h3.find('a').text
            self.url.append(product_link)
            self.name.append(product_name)
            print(product_name)
        for div in soup.find_all('div', class_='product-description-short overflow-hidden hidden mb-2'):
            product_description= div.text.strip()
            self.product_description.append(product_description)
        for img in  soup.find_all('img', class_='product-img lazy'):
            image_src = img['src']
            self.image_link.append(image_src)
        for product in soup.find_all('div', class_='product-price-shipping'):
            old_price_element = product.find('span', class_='regular-price d-block')
            new_price_element = product.find('span', class_='price')
            if old_price_element and new_price_element:
                old_price = old_price_element.text
                new_price = new_price_element.text
            self.old_price.append(old_price)
            self.new_price.append(new_price)



    def main(self):
        driver = webdriver.Chrome()
        driver.get(self.urls[1])
        html_content = driver.page_source
        self.save_html(html_content) 


    
if __name__ == "__main__":
    scraper = Scrapingcosme()
    scraper.main()
    #data_frame=scraper.save_data_frame()
    #print(data_frame)