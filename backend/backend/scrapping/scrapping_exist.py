from bs4 import BeautifulSoup
from selenium import webdriver
from tqdm import tqdm
import re
from backend.scrapping.scrapping import Scrapping
import requests


class ScrapingExist(Scrapping):
    """
    A class to scrape product information from the Exist website by extending the Scrapping base class.
    """

    def __init__(self) -> None:
        """
        Initialize the ScrapingExist object with the Exist product URLs.
        """
        Scrapping.__init__(self)
        self.urls = {"clothes": "https://www.exist.com.tn/promotions?page=1"}

    def convert_rows_for_df(self):
        """
        Converts the price values from strings to floats for the DataFrame.
        """
        for i, number in enumerate(self.old_price):
            self.old_price[i] = float(number[:-3].replace(",", "."))

    def extract_info_by_product(self, url, driver):
        """
        Extracts product information for a given product URL using the provided WebDriver.

        :param url: The product URL to scrape.
        :param driver: The WebDriver instance to use for scraping.
        """
        try:
            html_content = requests.get(url)
            soup = BeautifulSoup(html_content.text, "html.parser")
        except Exception:
            driver.get(url)
            html_content = driver.page_source
            soup = BeautifulSoup(html_content, "html.parser")
        div_element = soup.find("div", class_="current-price")
        price_element = div_element.find("span", itemprop="price")
        price = float(price_element["content"])
        self.new_price.append(price)
        div = soup.find("div", class_="product-discount")
        old_price_element = div.find("span", class_="regular-price")
        old_price = old_price_element.text.strip()
        self.old_price.append(old_price)
        name_element = soup.find("h1", class_="h1-main productpage_title")
        name = name_element.text
        self.name.append(name)
        des_element = soup.find("div", itemprop="description")
        description = des_element.text.strip()
        self.product_description.append(description)
        img_tag = soup.find("img", {"class": "thumb", "itemprop": "image"})
        large_image_url = img_tag["data-image-large-src"]
        self.image_link.append(large_image_url)
        self.product_type.append("clothes")

    def main(self):
        """
        The main method that drives the scraping process, extracts the product information, and saves it to a DataFrame.

        :return: The DataFrame containing the scraped product information.
        """
        driver = webdriver.Chrome()
        driver.get(self.urls["clothes"])
        html_content = driver.page_source
        soup = BeautifulSoup(html_content, "html.parser")
        pages = soup.find("div", class_="col-md-7")
        text = pages.text.strip()
        numbers = [int(num) for num in re.findall(r"\d+", text)]
        nuber_of_pages = max(numbers)
        for index in range(1, nuber_of_pages + 1):
            url = self.urls["clothes"][:-1] + str(index)
            driver.get(url)
            html_content = driver.page_source
            soup = BeautifulSoup(html_content, "html.parser")
            product_title_elements = soup.find_all("h3", class_="h3 product-title")
            for elem in product_title_elements:
                product_url = elem.find("a")["href"]
                self.url.append(product_url)
        for url in tqdm(self.url):
            self.extract_info_by_product(url, driver)
        self.convert_rows_for_df()
        driver.quit()
        df = self.save_data_frame()
        return df
