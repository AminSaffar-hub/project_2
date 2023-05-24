from bs4 import BeautifulSoup
from selenium import webdriver
import re
from backend.scrapping.scrapping import Scrapping
from selenium.webdriver.chrome.options import Options


class Scrapingcosme(Scrapping):
    """
    A class to scrape product information from the Cosmetique website by extending
    the Scrapping base class.
    """

    def __init__(self) -> None:
        """
        Initialize the Scrapingcosme object with the Cosmetique product URLs.
        """

        Scrapping.__init__(self)

        self.urls = {
            "promotion": "https://cosmetique.tn/promotions?page=",
            "vente flash": "https://cosmetique.tn/countdown/Vente_Flash",
        }

    def convert_rows_for_df(self):
        """
        Converts the price values from strings to floats for the DataFrame.
        """
        for i, number in enumerate(self.old_price):
            self.old_price[i] = float(number[:-3].replace(",", "."))
        for i, number in enumerate(self.new_price):
            self.new_price[i] = float(number[:-3].replace(",", "."))

    def scrap_promotion(self):
        """
        Scrapes the promotional product information from the Cosmetique website using a WebDriver.
        """
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        driver = webdriver.Chrome(option=chrome_options)
        driver.get("https://cosmetique.tn/promotions")
        html_content = driver.page_source
        soup = BeautifulSoup(html_content, "html.parser")
        page_item = soup.find(
            "div", class_="showing col-lg-4 text-center text-lg-left py-2"
        )
        pattern = re.compile(r"\d+-\d+")
        match = pattern.search(page_item.text.strip())
        if match:
            _, last_number = match.group().split("-")
        for index in range(1, int(last_number) + 1):
            driver.get(self.urls["promotion"] + str(index))
            html_content = driver.page_source
            soup = BeautifulSoup(html_content, "html.parser")
            for h3 in soup.find_all(
                "h3", class_="product-title h5 text-center overflow-hidden mt-2"
            ):
                product_link = h3.find("a")["href"]
                product_name = h3.find("a").text
                self.url.append(product_link)
                self.name.append(product_name)
            for div in soup.find_all(
                "div", class_="product-description-short overflow-hidden hidden mb-2"
            ):
                product_description = div.text.strip()
                self.product_description.append(product_description)
            for img in soup.find_all("img", class_="product-img lazy"):
                image_src = img["data-src"]
                self.image_link.append(image_src)
            for product in soup.find_all("div", class_="product-price-shipping"):
                old_price_element = product.find("span", class_="regular-price d-block")
                new_price_element = product.find("span", class_="price")
                if old_price_element and new_price_element:
                    old_price = old_price_element.text
                    new_price = new_price_element.text
                self.product_type.append("cosmetics")
                self.old_price.append(old_price)
                self.new_price.append(new_price)
        driver.quit()

    def main(self):
        """
        The main method that drives the scraping process, extracts the product information,
        and saves it to a DataFrame.

        :return: The DataFrame containing the scraped product information.
        """
        self.scrap_promotion()
        self.convert_rows_for_df()
        df = self.save_data_frame()
        return df
