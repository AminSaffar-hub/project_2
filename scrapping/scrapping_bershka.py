from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from tqdm import tqdm
import pandas as pd
import re
import time
from urllib.parse import urlsplit, urlunsplit


class ScrapingBershka:
    def __init__(self) -> None:
       self.urls ={"femme":"https://www.bershka.com/tn/femme/promotion-jusqu'%C3%A0--30%25-c1010473002.html","homme":"https://www.bershka.com/tn/homme/promotion-jusqu'%C3%A0--30%25-c1010477501.html"}
       self.html_file = "output_bershka.html"
       self.timer=20
       self.name=[]
       self.image_link=[]
       self.product_type=[]
       self.product_description=[]
       self.old_price=[]
       self.new_price=[]
       self.url=[]
    


    def scroll_down(self, driver):
        last_height = driver.execute_script("return document.body.scrollHeight")
        scroll_offset = 1000  

        while True:
            scroll_position = last_height - scroll_offset
            driver.execute_script(f"window.scrollTo(0, {scroll_position});")
            time.sleep(self.timer)
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height


    

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
        csv_file = "output_bershka.csv"
        df.to_csv(csv_file, index=False)
        return(df)
    
    def save_html(self,content):
        soup = BeautifulSoup(content, "html.parser")
        pretty_html = soup.prettify()
        with open(self.html_file, "w", encoding="utf-8") as f:
            f.write(pretty_html)



    def main(self):
            driver = webdriver.Chrome()
            for url in list(self.urls.values()):
                driver.get(url)
                self.scroll_down(driver)
                html_content = driver.page_source 
                #self.save_html(html_content)
                soup = BeautifulSoup(html_content, 'html.parser')
                grid_items = soup.find_all('li', class_='grid-item normal')
                for grid_item in grid_items:
                    image_tag=grid_item.find('img',class_='image-item')
                    parsed_url = urlsplit(image_tag["data-original"])
                    clean_url = urlunsplit((parsed_url.scheme, parsed_url.netloc, parsed_url.path, '', ''))
                    self.image_link.append(clean_url)
                    item_name=grid_item.find('div', class_="product-text")
                    name=item_name.text.strip()
                    self.name.append(name)
                    new_price_tag=grid_item.find('span',class_="current-price-elem--discounted current-price-elem")
                    new_price=new_price_tag.text.strip()
                    self.new_price.append(new_price)
                    old_price_tag=grid_item.find('span',class_="old-price-elem")
                    old_price=old_price_tag.text.strip()
                    self.old_price.append(old_price)
                    self.product_type.append("clothes")
                    self.product_description.append(" ")
                    link_tag=grid_item.find("a",class_="grid-card-link")
                    link="https://www.bershka.com"+link_tag["href"]
                    self.url.append(link)
            driver.quit()



if __name__ == "__main__":
     scrapper=ScrapingBershka()
     scrapper.main()
     df=scrapper.save_data_frame()

