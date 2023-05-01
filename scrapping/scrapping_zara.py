from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from tqdm import tqdm
import pandas as pd
import time
import json

class ScrapingZara:
    def __init__(self) -> None:
       self.urls ={"femme":"https://www.zara.com/tn/fr/femme-prix-speciaux-l1314.html?v1=2185209", 
                   "homme":"https://www.zara.com/tn/fr/homme-prix-speciaux-l806.html?v1=2203954",
                   "bebe-garcon":"https://www.zara.com/tn/fr/enfants-bebe-garcon-prix-speciaux-l69.html?v1=2194908",
                   "bebe fille": "https://www.zara.com/tn/fr/enfants-bebe-fille-prix-speciaux-l152.html?v1=2196579",
                   "garcon": "https://www.zara.com/tn/fr/enfants-garcon-prix-speciaux-l263.html?v1=2190481",
                   "fille": "https://www.zara.com/tn/fr/enfants-fille-prix-speciaux-l427.html?v1=2189631" }
       self.html_file = "output_zara.html"
       self.timer=10
       self.name=[]
       self.image_link=[]
       self.product_type=[]
       self.product_description=[]
       self.old_price=[]
       self.new_price=[]
       self.url=[]
       self.final_url=[]


    def scroll_down(self,driver):

        last_height = driver.execute_script("return document.body.scrollHeight")
        while True:
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(self.timer) 
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height :
                break
            last_height = new_height

    def extract_info_per_url(self,url,driver):
        driver.get(url)
        html_content = driver.page_source 
        soup = BeautifulSoup(html_content, 'html.parser')
        script_tag = soup.find('script', {'type': 'application/ld+json'})
        data = json.loads(script_tag.string)
        description = data[0]['description']
        image = data[0]['image'][0]
        name=data[0]['name']
        div1=soup.find('span', class_='price-current__amount')
        new_price=div1.text.strip()
        div=soup.find('span', class_='price-old__amount price__amount price__amount-old')
        ancien_prix= div.text.strip()
        self.old_price.append(ancien_prix)
        self.product_description.append(description)
        self.image_link.append(image)
        self.name.append(name)
        self.new_price.append(new_price)
        self.final_url.append(url)
        self.product_type.append("clothes")

    def save_data_frame(self):

        data = {
        'name': self.name,
        'old_price': self.old_price,
        'new_price': self.new_price,
        'image_link': self.image_link,
        'url':self.final_url,
        'desription': self.product_description,
        'product_type': self.product_type
        }
        df = pd.DataFrame(data)
        csv_file = "output_zara.csv"
        df.to_csv(csv_file, index=False)
        return(df)

    def save_html(self,content):
        soup = BeautifulSoup(content, "html.parser")
        pretty_html = soup.prettify()
        with open(self.html_file, "w", encoding="utf-8") as f:
            f.write(pretty_html)



    def convert_rows_for_df(self):
        for i, number in enumerate(self.old_price):
            self.old_price[i] = float(number[:-3].replace(',', '.'))
        for i, number in enumerate(self.new_price):
            self.new_price[i] = float(number[:-3].replace(',', '.')) 


    def main(self):
        driver = webdriver.Chrome()
        for key,value in self.urls.items():
            driver.get(value)
            self.scroll_down(driver)
            html_content = driver.page_source 
            soup = BeautifulSoup(html_content, 'html.parser')
            products = soup.find_all("a", class_="product-link _item product-grid-product-info__name link")
            for product in products:
                link = product["href"]
                self.url.append(link)
                
        for url in tqdm(self.url):
            try: 
                self.extract_info_per_url(url,driver)

            except Exception as e:
                print(e)
                print(url)
      
                continue
        driver.quit()
                  



if __name__ == "__main__":
    scraper = ScrapingZara()
    scraper.main()
    scraper.convert_rows_for_df()
    df=scraper.save_data_frame()
    pd.set_option('display.max_rows', None)  
    pd.set_option('display.expand_frame_repr', False)
    print(df.head())