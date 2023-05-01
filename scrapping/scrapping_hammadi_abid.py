import json
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from tqdm import tqdm
import pandas as pd
import time
import requests

# from scrapping.scrapping import Scrapping

promotion_api_url = "http://127.0.0.1:8000/api/promotions"


class Scrapping:
    def __init__(self):
        self.urls = []
        self.html_file = "output.html"
        self.timer = 10
        self.name = []
        self.image_link = []
        self.product_type = []
        self.product_description = []
        self.old_price = []
        self.new_price = []
        self.url = []

    def save_html(self, content):
        with open(self.html_file, "w", encoding="utf-8") as f:
            f.write(
                content,
            )

    def save_data_frame(self):
        data = {
            "name": self.name,
            "old_price": self.old_price,
            "new_price": self.new_price,
            "image link": self.image_link,
            "url": self.url,
            "desription": self.product_description,
        }
        df = pd.DataFrame(data)
        csv_file = "output_mg.csv"
        df.to_csv(csv_file, index=False)
        return df

    def save_data_to_db(self):
        for name, original_price, reduced_price, location, image in zip(
            self.name, self.old_price, self.new_price, self.url, self.image_link
        ):
            print(name, original_price, reduced_price, location, image)
            promotion_data = {
                "name": name,
                "original_price": 0,
                "reduced_price": 0,
                "location": location,
                "image": image,
                "sector": "clothes"
            }
            headers = {'content-type': 'application/json'}

            requests.post(url=promotion_api_url, data=json.dumps(promotion_data))

    def scroll_down(self, driver):
        last_height = driver.execute_script("return document.body.scrollHeight")
        while True:
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(self.timer)
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height


class scrappingHammadiAbid(Scrapping):
    def __init__(self) -> None:
        Scrapping.__init__(self)
        genders = ["homme", "femme", "enfant", "bebe"]
        self.urls = [
            f"https://www.ha.com.tn/{gender}.html?solde=true" for gender in genders
        ]
        self.timer = 1
        print(self.urls)

    def main(self):
        driver = webdriver.Chrome()
        for sector_url in tqdm(self.urls):
            driver.get(sector_url)
            self.scroll_down(driver)
            html_content = driver.page_source
            scraper.save_html(html_content)
            soup = BeautifulSoup(html_content, "html.parser")
            for div in soup.find_all("div", class_="allinfoallprod leftinfoallprod"):
                self.name.append(div.text.strip())
            for span in soup.find_all("span", class_="nv-prix"):
                self.new_price.append(span.text.strip())
            for span in soup.find_all("span", class_="anc-prix"):
                self.old_price.append(span.text.strip())
            for div in soup.find_all("div", class_="img-prod"):
                self.url.append(div.find("a")["href"])
            for img in soup.find_all("img", class_="b-lazy b-loaded"):
                self.image_link.append(img["src"])
            self.product_type = self.product_description = [
                "" for _ in range(len(self.name))
            ]
        driver.quit()


if __name__ == "__main__":
    scraper = scrappingHammadiAbid()
    scraper.main()
    data_frame = scraper.save_data_to_db()
