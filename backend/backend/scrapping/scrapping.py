import pandas as pd
import time
from bs4 import BeautifulSoup
from backend.models import Article


class Scrapping:
    """
    A base class for web scraping, providing common functionality for
    scraping websites and storing the extracted information.

    Attributes:
        urls (dict): A dictionary of URLs to scrape.
        name (list): A list of product names.
        image_link (list): A list of image links for the products.
        product_type (list): A list of product types.
        product_description (list): A list of product descriptions.
        old_price (list): A list of old prices for the products.
        new_price (list): A list of new prices for the products.
        url (list): A list of product URLs.
        _scrappers (list): A list of child scraper instances.
        _data_frame (pd.DataFrame): A pandas DataFrame to store the scraped data.
        _html_file (str): The name of the output HTML file.

    Methods:
        save_html(content): Saves the HTML content to a file.
        save_data_frame(): Saves the scraped data as a pandas DataFrame.
        scroll_down(driver, timer): Scrolls down a webpage to load more content.
    """

    def __init__(self):
        self.urls = {}
        self.name = []
        self.image_link = []
        self.product_type = []
        self.product_description = []
        self.old_price = []
        self.new_price = []
        self.url = []
        self._scrappers = []
        self._data_frame = pd.DataFrame()
        self._html_file = "output.html"
        self._api_url = "http://localhost:8000/api/promotions"

    def save_html(self, content):
        """
        Saves the HTML content to a file.

        Args:
            content (str): The HTML content to save.
        """
        soup = BeautifulSoup(content, "html.parser")
        pretty_html = soup.prettify()
        with open(self._html_file, "w", encoding="utf-8") as f:
            f.write(pretty_html)

    def save_data_frame(self):
        """
        Saves the scraped data as a pandas DataFrame.

        Returns:
            pd.DataFrame: A DataFrame containing the scraped data.
        """
        data = {
            "name": self.name,
            "old_price": self.old_price,
            "new_price": self.new_price,
            "image_link": self.image_link,
            "url": self.url,
            "desription": self.product_description,
            "product_type": self.product_type,
        }
        df = pd.DataFrame(data)
        return df

    def scroll_down(self, driver, timer):
        """
        Scrolls down a webpage to load more content.

        Args:
            driver (webdriver): A Selenium webdriver instance.
            timer (int): The number of seconds to wait between scrolling.
        """

        last_height = driver.execute_script("return document.body.scrollHeight")
        while True:
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(timer)
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height

    def save_data_to_db(self):
        """
        Saves data to database by posting to the /api/promotions endpoint
        """
        for name, old_price, new_price, url, image_link, product_type, description in zip(
            self.name,
            self.old_price,
            self.new_price,
            self.url,
            self.image_link,
            self.product_type,
            self.product_description
        ):
            Article.objects.create(
                name=name,
                old_price=old_price,
                new_price=new_price,
                url=url,
                image_link=image_link,
                description=description,
                type=product_type,
            )
