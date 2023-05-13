from bs4 import BeautifulSoup
from selenium import webdriver
import pandas as pd

pre_process_prices = lambda a: float(a.replace("TND", "").replace(",", "."))
class Scrappingfatales:
    def __init__(self):
        self.urls = "https://www.fatales.tn/promotions"
        self.html_file = "output.html"
        self.timer = 10
        self.name = []
        self.image_link = []
        self.product_type = []
        self.product_description = []
        self.old_price = []
        self.new_price = []
        self.url = []

    def save_data_frame(self):
        print(len(self.name))
        print(len(self.old_price))
        print(len(self.new_price))
        print(len(self.url))
        print(len(self.image_link))
        print(len(self.product_description))
        print(len(self.product_type))
        data = {
        'name': self.name,
        'old_price': self.old_price,
        'new_price': self.new_price,
        'image_link':self.image_link,
        'url': self.url,
        'description': self.product_description,
        'product_type': self.product_type
        }
        df = pd.DataFrame(data)
        return(df)   
        
    def get_product_description(self, product_url, driver):
        driver.get(product_url)
        html_content = driver.page_source
        soup = BeautifulSoup(html_content, "html.parser")
        self.product_description.append(soup.find("div", itemprop= "description").text)

    def main(self):
        driver = webdriver.Chrome()
        driver.get(self.urls)
        html_content = driver.page_source
        soup = BeautifulSoup(html_content, "html.parser")
        page_indexes = soup.find_all("a", class_="js-search-link")
        number_of_pages = 0
        for page in page_indexes:
            try:
                page_index = int(page.text)
                if page_index > number_of_pages:
                    number_of_pages = page_index
            except Exception:
                pass
        for i in range(1, number_of_pages + 1):
            try:
                driver.get(self.urls + f"?page={i}")
                html_content = driver.page_source
                soup = BeautifulSoup(html_content, "html.parser")
                for article in soup.find_all("article", class_="product-miniature"):
                    self.image_link.append(article.find("img", class_="img-responsive")["src"])
                    self.name.append(article.find("a", class_="product-name").text)
                    try:
                        self.old_price.append(pre_process_prices(article.find("span", class_="regular-price").text))
                    except Exception:
                        self.old_price = None
                    self.new_price.append(pre_process_prices(article.find("span", class_="price product-price").text))
                    self.get_product_description(article.find("a", class_="product_img_link")['href'], driver=driver)
            except Exception:
                driver = webdriver.Chrome()
                continue
        driver.quit()
        df=self.save_data_frame()
        return(df)


if __name__ == "__main__":
    scrapper = Scrappingfatales()
    df=scrapper.main()
    print(df.head())
