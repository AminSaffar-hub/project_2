from bs4 import BeautifulSoup
from selenium import webdriver
import time
from urllib.parse import urlsplit, urlunsplit
from scrapping import Scrapping


class ScrapingBershka(Scrapping):
    """
    A class to scrape product information from the Bershka website by extending the Scrapping base class.
    """

    def __init__(self) -> None:
        """
        Initialize the ScrapingBershka object with the Bershka product URLs.
        """
        Scrapping.__init__(self)
        
        self.urls = {
            "femme": "https://www.bershka.com/tn/femme/promotion-jusqu'%C3%A0--30%25-c1010473002.html",
            "homme": "https://www.bershka.com/tn/homme/promotion-jusqu'%C3%A0--30%25-c1010477501.html",
        }
        self._timer = 20

    def convert_rows_for_df(self):
        """
        Converts the price values from strings to floats for the DataFrame.
        """
        for i, number in enumerate(self.old_price):
            self.old_price[i] = float(number[:-3])
        for i, number in enumerate(self.new_price):
            self.new_price[i] = float(number[:-3])

    def scroll_down_Bershka(self, driver, timer):
        """
        Scrolls down the Bershka webpage in the given WebDriver to load more products.

        :param driver: The WebDriver instance used for scraping.
        :param timer: The time (in seconds) to wait for the webpage to load more products.
        """
        last_height = driver.execute_script("return document.body.scrollHeight")
        scroll_offset = 1000

        while True:
            scroll_position = last_height - scroll_offset
            driver.execute_script(f"window.scrollTo(0, {scroll_position});")
            time.sleep(timer)
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height

    def main(self):
        """
        The main method that drives the scraping process, extracts the product information, and saves it to a DataFrame.

        :return: The DataFrame containing the scraped product information.
        """
        driver = webdriver.Chrome()
        for url in list(self.urls.values()):
            driver.get(url)
            self.scroll_down_Bershka(driver, self._timer)
            html_content = driver.page_source
            soup = BeautifulSoup(html_content, "html.parser")
            grid_items = soup.find_all("li", class_="grid-item normal")
            for grid_item in grid_items:
                image_tag = grid_item.find("img", class_="image-item")
                parsed_url = urlsplit(image_tag["data-original"])
                clean_url = urlunsplit(
                    (parsed_url.scheme, parsed_url.netloc, parsed_url.path, "", "")
                )
                self.image_link.append(clean_url)
                item_name = grid_item.find("div", class_="product-text")
                name = item_name.text.strip()
                self.name.append(name)
                new_price_tag = grid_item.find(
                    "span", class_="current-price-elem--discounted current-price-elem"
                )
                new_price = new_price_tag.text.strip()
                self.new_price.append(new_price)
                old_price_tag = grid_item.find("span", class_="old-price-elem")
                old_price = old_price_tag.text.strip()
                self.old_price.append(old_price)
                self.product_type.append("clothes")
                self.product_description.append(" ")
                link_tag = grid_item.find("a", class_="grid-card-link")
                link = "https://www.bershka.com" + link_tag["href"]
                self.url.append(link)
        driver.quit()
        self.convert_rows_for_df()
        df = self.save_data_frame()
        return df
