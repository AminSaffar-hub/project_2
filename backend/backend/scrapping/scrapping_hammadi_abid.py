from bs4 import BeautifulSoup
from selenium import webdriver
from tqdm import tqdm
from backend.scrapping.scrapping import Scrapping
import requests
from selenium.webdriver.chrome.options import Options



class scrappingHammadiAbid(Scrapping):
    """
    A class to scrape Hammadi Abid product information by extending the Scrapping base class.
    """

    def __init__(self) -> None:
        """
        Initialize the scrappingHammadiAbid object with the Hammadi Abid product URLs and other settings.
        """
        Scrapping.__init__(self)
        self.urls = {
            "homme": "https://www.ha.com.tn/homme.html?solde=true",
            "femme": "https://www.ha.com.tn/femme.html?solde=true",
            "enfant": "https://www.ha.com.tn/enfant.html?solde=true",
            "bebe": "https://www.ha.com.tn/bebe.html?solde=true",
        }
        self._timer = 2

    def convert_rows_for_df(self):
        """
        Converts the price values from strings to floats for the DataFrame.
        """
        for i, value in enumerate(self.old_price):
            self.old_price[i] = float(value)
        for i, value in enumerate(self.new_price):
            self.new_price[i] = float(value)

    def extract_info_per_url(self, url):
        """
        Extracts product information for a given URL using the provided WebDriver.

        :param url: The product URL to scrape.
        """
        html_content = requests.get(url)
        soup = BeautifulSoup(html_content.text, "html.parser")
        name = soup.find("meta", {"property": "og:title"})["content"]
        self.name.append(name)
        description = soup.find("meta", {"property": "og:description"})["content"]
        self.product_description.append(description)
        self.product_type.append("clothes")
        price = soup.find("meta", {"property": "product:price"})["content"]
        sale_price = soup.find("meta", {"property": "product:sale_price"})["content"]
        image_url = soup.find("meta", {"property": "og:image"})["content"]
        self.image_link.append(image_url)
        self.old_price.append(price)
        self.new_price.append(sale_price)

    def main(self):
        """
        The main method that drives the scraping process, extracts the product information, and saves it to a DataFrame.

        :return: The DataFrame containing the scraped product information.
        """
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        driver = webdriver.Chrome(option = chrome_options)
        for sector_url in list(self.urls.values()):
            driver.get(sector_url)
            self.scroll_down(driver, self._timer)
            html_content = driver.page_source
            soup = BeautifulSoup(html_content, "html.parser")
            for div in soup.find_all("div", class_="img-prod"):
                self.url.append(div.find("a")["href"])
        driver.quit()
        for url in tqdm(self.url):
            self.extract_info_per_url(url)
        self.convert_rows_for_df()
        df = self.save_data_frame()
        return df


if __name__ == "__main__":
    scraper = scrappingHammadiAbid()
    df = scraper.main()
    print(df)
