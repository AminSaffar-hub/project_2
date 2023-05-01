from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from tqdm import tqdm
import pandas as pd
import re 

class Scrapingcosme:
    def __init__(self) -> None:
       self.urls =["https://cosmetique.tn/promotions?page=","https://cosmetique.tn/countdown/Vente_Flash"]
       self.html_file = "output_cos_2.html"
       self.name=[]
       self.image_link=[]
       self.product_type=[]
       self.product_description=[]
       self.old_price=[]
       self.new_price=[]
       self.url=[]
    
    def save_data_frame(self):
        data = {
        'name': self.name,
        'old_price': self.old_price,
        'new_price': self.new_price,
        'image_link': self.image_link,
        'url':self.url,
        'desription': self.product_description,
        'product_type': self.product_type
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
        driver.get("https://cosmetique.tn/promotions")
        html_content = driver.page_source 
        soup = BeautifulSoup(html_content, 'html.parser')
        page_item=soup.find('div', class_="showing col-lg-4 text-center text-lg-left py-2")
        pattern = re.compile(r"\d+-\d+")
        match = pattern.search(page_item.text.strip())
        if match:
            _, last_number = match.group().split('-')
        for index in range(1,int(last_number)+1):
            driver.get( self.urls[0]+str(index))
            html_content = driver.page_source 
            soup = BeautifulSoup(html_content, 'html.parser')
            for h3 in soup.find_all('h3', class_='product-title h5 text-center overflow-hidden mt-2'):
                product_link = h3.find('a')['href']
                product_name = h3.find('a').text
                self.url.append(product_link)
                self.name.append(product_name)
            for div in soup.find_all('div', class_='product-description-short overflow-hidden hidden mb-2'):
                product_description= div.text.strip()
                self.product_description.append(product_description)
            for img in  soup.find_all('img', class_='product-img lazy'):
                image_src = img['data-src']
                self.image_link.append(image_src)
            for product in soup.find_all('div', class_='product-price-shipping'):
                old_price_element = product.find('span', class_='regular-price d-block')
                new_price_element = product.find('span', class_='price')
                if old_price_element and new_price_element:
                    old_price = old_price_element.text
                    new_price = new_price_element.text
                self.product_type.append("cosmetics")
                self.old_price.append(old_price)
                self.new_price.append(new_price)
        driver.quit()

    def convert_rows_for_df(self):
        for i, number in enumerate(self.old_price):
            self.old_price[i] = float(number[:-3].replace(',', '.'))
        for i, number in enumerate(self.new_price):
            self.new_price[i] = float(number[:-3].replace(',', '.'))

    def main(self):
        self.scrap_promotion()
        self.convert_rows_for_df()
        pd.set_option('display.max_rows', None)  
        pd.set_option('display.expand_frame_repr', False) 
 
if __name__ == "__main__":
    scraper = Scrapingcosme()
    scraper.main()
    data_frame=scraper.save_data_frame()
