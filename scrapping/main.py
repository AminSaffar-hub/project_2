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

from scrapping_bershka import ScrapingBershka
from scrapping_cosemetique import Scrapingcosme
from scrapping_exist import ScrapingExist
from scrapping_mg import ScrapingMG
from scrapping_zara import ScrapingZara
import pandas as pd
import time
import sys


def main():
    """
    Scrapes data from Bershka, Cosmetique, Exist, MG, and Zara websites using their respective
    scraping classes. Combines the resulting DataFrames into a single DataFrame.

    Returns:
        pd.DataFrame: The combined DataFrame containing the scraped data from all websites.
    """
    zara = ScrapingZara()
    Bershka = ScrapingBershka()
    mg = ScrapingMG()
    exist = ScrapingExist()
    cosmetique = Scrapingcosme()
    df_Bershka = Bershka.main()
    sys.stdout.write("Finished running Bershka's main function.\n")
    sys.stdout.flush()
    df_cos = cosmetique.main()
    sys.stdout.write("Finished running Cosmetique's main function.\n")
    sys.stdout.flush()
    df_exist = exist.main()
    sys.stdout.write("Finished running Exist's main function.\n")
    sys.stdout.flush()
    df_mg = mg.main()
    sys.stdout.write("Finished running Mg's main function.\n")
    sys.stdout.flush()
    df_zara = zara.main()
    sys.stdout.write("Finished running Zara's main function.\n")
    sys.stdout.flush()
    result_df = pd.concat(
        [df_mg, df_Bershka, df_zara, df_exist, df_cos], ignore_index=True
    )
    return result_df


if __name__ == "__main__":
    start_time = time.time()
    final_df = main()
    elapsed_time = time.time() - start_time
    final_df.to_csv("output.csv", index=False, encoding="utf-8")
    sys.stdout.write("Data successfully saved to output.csv\n")
    sys.stdout.flush()
    print(f"Execution time: {elapsed_time:.2f} seconds")
    print(final_df)
