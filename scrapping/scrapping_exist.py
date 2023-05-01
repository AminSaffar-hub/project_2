from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from tqdm import tqdm
import pandas as pd
import re 


class ScrapingExist:
    def __init__(self) -> None:
       self.urls ="https://www.exist.com.tn/promotions?page=1"
       self.html_file = "output_exist_1.html"
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
        csv_file = "output_exist.csv"
        df.to_csv(csv_file, index=False)
        return(df)
    
    def save_html(self,content):
        soup = BeautifulSoup(content, "html.parser")
        pretty_html = soup.prettify()
        with open(self.html_file, "w", encoding="utf-8") as f:
            f.write(pretty_html)



    def extract_info_by_product(self,url,driver):
        driver.get(url)
        html_content = driver.page_source 
        soup = BeautifulSoup(html_content, 'html.parser')
        div_element = soup.find('div', class_='current-price')
        price_element = div_element.find('span', itemprop='price')
        price = float(price_element['content'])
        self.new_price.append(price)
        div=soup.find('div', class_='product-discount')
        old_price_element=div.find('span',class_="regular-price")
        old_price= old_price_element.text.strip()
        self.old_price.append(old_price)
        name_element=soup.find('h1', class_='h1-main productpage_title')
        name= name_element.text
        self.name.append(name)
        des_element=soup.find('div',itemprop="description")
        description=des_element.text.strip()
        self.product_description.append(description)
        img_tag = soup.find('img', {'class': 'thumb', 'itemprop': 'image'})
        large_image_url = img_tag['data-image-large-src']
        self.image_link.append(large_image_url)
        self.product_type.append("clothes")
    
    def convert_rows_for_df(self):
        for i, number in enumerate(self.old_price):
            self.old_price[i] = float(number[:-3].replace(',', '.'))


    def main(self):
        driver = webdriver.Chrome()
        driver.get(self.urls)
        html_content = driver.page_source 
        soup = BeautifulSoup(html_content, 'html.parser')
        pages= soup.find('div', class_='col-md-7')
        text= pages.text.strip()
        numbers = [int(num) for num in re.findall(r'\d+', text)]
        nuber_of_pages = max(numbers)
        for index in range(1,nuber_of_pages+1):
            url=self.urls[:-1]+str(index)
            driver.get(url)
            html_content = driver.page_source 
            soup = BeautifulSoup(html_content, 'html.parser')
            product_title_elements = soup.find_all('h3', class_='h3 product-title')
            for elem in product_title_elements:
                product_url = elem.find('a')['href']
                self.url.append(product_url)
        for url in tqdm(self.url):
            self.extract_info_by_product(url,driver)
        self.convert_rows_for_df()
        driver.quit()




        

if __name__ == "__main__":
    scraper = ScrapingExist()
    scraper.main()
    pd.set_option('display.max_rows', None)  
    pd.set_option('display.expand_frame_repr', False)
    df=scraper.save_data_frame()
    print(df.head())