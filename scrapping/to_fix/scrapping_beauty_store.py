from bs4 import BeautifulSoup
from selenium import webdriver
from tqdm import tqdm
import pandas as pd 


class Scrappingbeautystore:
    def __init__(self) -> None:
       self.urls ="https://beautystore.tn/164-promos"
       self.html_file = "output_cos_2.html"
       self.name=[]
       self.image_link=[]
       self.product_type=[]
       self.product_description=[]
       self.old_price=[]
       self.new_price=[]
       self.url=[]
    def save_data_frame(self):
        print(len(self.name))
        print(len(self.old_price))
        print(len(self.new_price))
        #print(len(self.url))
        print(len(self.image_link))
        print(len(self.product_description))
        print(len(self.product_type))
        data = {
        'name': self.name,
        'old_price': self.old_price,
        'new_price': self.new_price,
        'image_link': self.image_link,
        #'url':self.url,
        'desription': self.product_description,
        'product_type': self.product_type
        }
        df = pd.DataFrame(data)
        return(df)
    

    def scrap_promotion(self):
        driver = webdriver.Chrome()
        driver.get(self.urls)
        html_content = driver.page_source
        promotions_sections = BeautifulSoup(html_content, 'html.parser')
        navigation_bar = promotions_sections.find('ul', class_='page-list')
        all_promotions_pages = navigation_bar.find_all('a', class_='js-search-link')
        for promotion_page_link in all_promotions_pages:
            driver.get(promotion_page_link['href'])
            html_content = driver.page_source
            promotions_page = BeautifulSoup(html_content, 'html.parser')
            for article  in promotions_page.find_all('article', class_='product-miniature'):
                self.product_description.append(article.find('div', class_='product-description').text)
                try:
                    self.old_price.append(article.find('span', class_='regular-price').text)
                except Exception:
                    self.old_price.append(None)
                self.new_price.append(article.find('span', class_='price').text)
                self.image_link.append(article.find('img')['src'])
                self.name.append(article.find('h1', class_='product-title').text)
                self.product_type.append("cosmetics")
        df=self.save_data_frame()
        return(df)

if __name__ == '__main__':
    scrapper = Scrappingbeautystore()
    df=scrapper.scrap_promotion()
    print(df.head())
    print(scrapper.product_description)