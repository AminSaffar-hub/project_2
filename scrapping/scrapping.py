import pandas as pd
import time


class Scrapping:
    def __init__(self):
        self.urls = []
        self.html_file = "output.html"
        self.timer = 10
        self.name = []
        self.link = []
        self.product_type = []
        self.price = []
        self.url = []

    def save_html(self, content):
        with open(self.html_file, "w", encoding="utf-8") as f:
            f.write(content)

    def save_data_frame(self):
        print(len(self.name), len(self.link), len(self.product_type))
        data = {
            "name": self.name,
            "link": self.link,
            "product_type": self.product_type,
            "price": self.price,
            "link_image": self.url,
        }
        df = pd.DataFrame(data)
        csv_file = "output_mg.csv"
        df.to_csv(csv_file, index=False)
        return df

    def scroll_down(self, driver):
        last_height = driver.execute_script("return document.body.scrollHeight")
        while True:
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(self.timer)
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height
