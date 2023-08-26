import re

import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from tqdm import tqdm

from backend.scrapping.scrapping import Scrapping


class ScrapingMG(Scrapping):
    """
    A class to scrape product information from the MG website by extending
    the Scrapping base class.
    """

    def __init__(self) -> None:
        """
        Initialize the ScrapingMG object with the MG product URLs and other settings.
        """

        Scrapping.__init__(self)

        self.urls = {
            "food": "https://mg.tn/61-promotion",
            "self-care": "https://mg.tn/64-promotion",
            "appliances": "https://mg.tn/67-promotion",
        }
        self._price = []
        self._timer = 10

    def extract_info_per_product(self, link):
        """
        Extracts product information for a given product URL using the provided WebDriver.

        :param link: The product URL to scrape.
        """
        html_content = requests.get(link)
        soup = BeautifulSoup(html_content.text, "html.parser")
        has_discount_divs = soup.find_all("div", class_="has-discount")
        meta_tag = soup.find("meta", property="og:image")

        if meta_tag:
            image_url = meta_tag["content"]
            self.image_link.append(image_url)
        else:
            self.image_link.append("Element not found")
        text_ = ""
        if not has_discount_divs:
            text_ = "no prices"
        else:
            for div in has_discount_divs:
                cleaned_text = " ".join(div.text.split())
                text_ = text_ + cleaned_text
        self._price.append(text_)
        outer_div = soup.find("div", {"class": "product-information"})
        if outer_div:
            target_div = outer_div.find(
                "div", {"class": "rte-content product-description"}
            )
            if target_div:
                text = target_div.get_text(strip=True)
                self.product_description.append(text)
            else:
                self.product_description.append("")
        else:
            self.product_description.append("")

    def fix_info_df(self):
        """
        Removes products without prices and formats the price information for the DataFrame.
        """
        no_price_indices = [
            i for i, price in enumerate(self._price) if price == "no prices"
        ]
        for index in sorted(no_price_indices, reverse=True):
            del self.name[index]
            del self.url[index]
            del self._price[index]
            del self.image_link[index]
            del self.product_type[index]
            del self.product_description[index]
        for element in self._price:
            numbers_str = re.findall(r"\d+\s*,\s*\d+", element)
            number1_str = numbers_str[0].replace(",", ".").replace(" ", "")
            number2_str = numbers_str[1].replace(",", ".").replace(" ", "")
            number1 = float(number1_str)
            number2 = float(number2_str)
            if number1 > number2:
                self.new_price.append(number1)
                self.old_price.append(number1 + number2)
            else:
                self.new_price.append(number1)
                self.old_price.append(number2)

    def main(self):
        """
        The main method that drives the scraping process, extracts the product information,
        and saves it to a DataFrame.

        :return: The DataFrame containing the scraped product information.
        """
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        driver = webdriver.Chrome(option=chrome_options)
        for sector_url, div in tqdm(zip(self.urls.values(), self.urls.keys())):
            driver.get(sector_url)
            self.scroll_down(driver, self._timer)
            html_content = driver.page_source
            soup = BeautifulSoup(html_content, "html.parser")
            product_titles = soup.find_all("h2", class_="h3 product-title")
            for title in product_titles:
                self.product_type.append(div)
                link_tag = title.find("a")
                if link_tag:
                    link = link_tag.get("href")
                    product_name = link_tag.text
                    self.url.append(link)
                    self.extract_info_per_product(link)
                    self.name.append(product_name)
        driver.quit()
        self.fix_info_df()
        df = self.save_data_frame()
        return df
