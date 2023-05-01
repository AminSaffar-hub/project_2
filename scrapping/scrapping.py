import pandas as pd
import time


class Scrapping:
    def __init__(self):
        self.name=[]
        self.image_link=[]
        self.product_type=[]
        self.product_description=[]
        self.old_price=[]
        self.new_price=[]
        self.url=[]

    def save_html(self, content):
        with open(self.html_file, "w", encoding="utf-8") as f:
            f.write(content)

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

    def scroll_down(self, driver):
        last_height = driver.execute_script("return document.body.scrollHeight")
        while True:
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(self.timer)
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height
    
    
