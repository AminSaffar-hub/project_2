"""
This script imports the scraping classes for various websites (Bershka, Cosmetique, Exist, MG, and Zara)
and combines the scraped data into a single pandas DataFrame. The resulting DataFrame is saved to a
CSV file named "output.csv" and printed to the console.

Classes Imported:
    ScrapingBershka: Scraper for the Bershka website.
    Scrapingcosme: Scraper for the Cosmetique website.
    ScrapingExist: Scraper for the Exist website.
    ScrapingMG: Scraper for the MG website.
    ScrapingZara: Scraper for the Zara website.

Functions:
    main(): Scrapes data from all the websites and combines the results into a single DataFrame.

Usage:
    Run the script to scrape the data and save it to the "output.csv" file. The final DataFrame will
    also be printed to the console.
"""
from backend.scrapping.scrapping_beauty_store import Scrappingbeautystore
from backend.scrapping.scrapping_bershka import ScrapingBershka
from backend.scrapping.scrapping_cosemetique import Scrapingcosme
from backend.scrapping.scrapping_exist import ScrapingExist
from backend.scrapping.scrapping_mg import ScrapingMG
from backend.scrapping.scrapping_zara import ScrapingZara
import time
import sys


def run_scrapping():
    """
    Scrapes data from Bershka, Cosmetique, Exist, MG, and Zara websites using their respective
    scraping classes. Combines the resulting DataFrames into a single DataFrame.

    Returns:
        pd.DataFrame: The combined DataFrame containing the scraped data from all websites.
    """
    scrapped_articles = []
    start_time = time.time()
    for klass in [ScrapingZara(), ScrapingBershka(), ScrapingMG(), ScrapingExist(), Scrapingcosme(), Scrappingbeautystore()]:
        scrapped_articles.append(klass.main())
        klass.save_data_to_db()
        sys.stdout.write(f"Finished running {klass.__class__.__name__}'s main function.\n")
        sys.stdout.flush()
    elapsed_time = time.time() - start_time
    print(f"Execution time: {elapsed_time:.2f} seconds")
