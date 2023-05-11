from bs4 import BeautifulSoup
from selenium import webdriver
from scrapping import Scrapping


class Scrappingbeautystore(Scrapping):
    def __init__(self) -> None:
        """
        A class to scrape product information from the Beautystore website by extending the Scrapping base class.
        """
        Scrapping.__init__(self)
        """
        Initialize the ScrapingBershka object with the Beautystore product URLs.
       """
        self.urls = {"promotion": "https://beautystore.tn/164-promos"}

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
        driver = webdriver.Chrome()
        driver.get(self.urls["promotion"])
        html_content = driver.page_source
        promotions_sections = BeautifulSoup(html_content, "html.parser")
        navigation_bar = promotions_sections.find("ul", class_="page-list")
        all_promotions_pages = navigation_bar.find_all("a", class_="js-search-link")
        for promotion_page_link in all_promotions_pages:
            driver.get(promotion_page_link["href"])
            html_content = driver.page_source
            promotions_page = BeautifulSoup(html_content, "html.parser")
            for article in promotions_page.find_all(
                "article", class_="product-miniature"
            ):
                self.product_description.append(
                    article.find("div", class_="product-description").text.strip()
                )
                try:
                    self.old_price.append(
                        article.find("span", class_="regular-price").text.strip()
                    )
                except Exception:
                    self.old_price.append(
                        article.find("span", class_="price").text.strip()
                    )
                self.new_price.append(article.find("span", class_="price").text.strip())
                self.image_link.append(article.find("img")["src"])
                self.name.append(article.find("h1", class_="product-title").text)
                self.product_type.append("cosmetics")
            for a_tag in promotions_page.find_all(
                "a", class_="thumbnail product-thumbnail"
            ):
                href = a_tag.get("href")
                self.url.append(href)

        self.convert_rows_for_df()
        df = self.save_data_frame()
        return df
