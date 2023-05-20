from bs4 import BeautifulSoup
from selenium import webdriver
from tqdm import tqdm
import json
from backend.scrapping.scrapping import Scrapping
import requests
from selenium.webdriver.chrome.options import Options



class ScrapingZara(Scrapping):
    """
    A class to scrape Zara product information by extending the Scrapping base class.
    """

    def __init__(self) -> None:
        """
        Initialize the ScrapingZara object with the Zara product URLs and other settings.
        """
        Scrapping.__init__(self)
        self.urls = {
            "femme": "https://www.zara.com/tn/fr/femme-prix-speciaux-l1314.html?v1=2185209",
            "homme": "https://www.zara.com/tn/fr/homme-prix-speciaux-l806.html?v1=2203954",
            "bebe-garcon": "https://www.zara.com/tn/fr/enfants-bebe-garcon-prix-speciaux-l69.html?v1=2194908",
            "bebe fille": "https://www.zara.com/tn/fr/enfants-bebe-fille-prix-speciaux-l152.html?v1=2196579",
            "garcon": "https://www.zara.com/tn/fr/enfants-garcon-prix-speciaux-l263.html?v1=2190481",
            "fille": "https://www.zara.com/tn/fr/enfants-fille-prix-speciaux-l427.html?v1=2189631",
        }
        self._timer = 10
        self._intermidiate_url = []

    def extract_info_per_url(self, url):
        """
        Extracts product information for a given URL using the provided WebDriver.

        :param url: The product URL to scrape.
        :param driver: The WebDriver instance to use for scraping.
        """
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
        script_tag = soup.find("script", {"type": "application/ld+json"})
        data = json.loads(script_tag.string)
        description = data[0]["description"]
        image = data[0]["image"][0]
        name = data[0]["name"]
        div1 = soup.find("span", class_="price-current__amount")
        new_price = div1.text.strip()
        div = soup.find(
            "span", class_="price-old__amount price__amount price__amount-old"
        )
        ancien_prix = div.text.strip()
        self.old_price.append(ancien_prix)
        self.product_description.append(description)
        self.image_link.append(image)
        self.name.append(name)
        self.new_price.append(new_price)
        self.url.append(url)
        self.product_type.append("clothes")

    def convert_rows_for_df(self):
        """
        Converts the price values from strings to floats for the DataFrame.
        """
        for i, number in enumerate(self.old_price):
            self.old_price[i] = float(number[:-3].replace(",", "."))
        for i, number in enumerate(self.new_price):
            self.new_price[i] = float(number[:-3].replace(",", "."))

    def main(self):
        """
        The main method that drives the scraping process, extracts the product information, and saves it to a DataFrame.

        :return: The DataFrame containing the scraped product information.
        """
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        driver = webdriver.Chrome(options=chrome_options)
        for key, value in self.urls.items():
            driver.get(value)
            self.scroll_down(driver, self._timer)
            html_content = driver.page_source
            soup = BeautifulSoup(html_content, "html.parser")
            products = soup.find_all(
                "a", class_="product-link _item product-grid-product-info__name link"
            )
            for product in products:
                link = product["href"]
                self._intermidiate_url.append(link)
        for url in tqdm(self._intermidiate_url):
            try:
                self.extract_info_per_url(url)

            except Exception:
                continue
        driver.quit()
        self.convert_rows_for_df()
        df = self.save_data_frame()
        return df
