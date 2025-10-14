import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import pandas as pd

# Flipkart reviews page URL
REVIEWS_URL = "https://www.flipkart.com/kotty-solid-women-scoop-neck-brown-t-shirt/product-reviews/itm26123255bf277?pid=TSHHFSNGJ7RYXFHZ&lid=LSTTSHHFSNGJ7RYXFHZLZKBXT&marketplace=FLIPKART"
def setup_driver():
    """Sets up Selenium WebDriver."""
    service = Service(ChromeDriverManager().install())
    options = webdriver.ChromeOptions()
    # options.add_argument('--headless')  # Uncomment to run headless
    options.add_argument('--disable-gpu')
    options.add_argument('--window-size=1920,1080')
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/5.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
    driver = webdriver.Chrome(service=service, options=options)
    return driver

def scrape_flipkart_reviews(reviews_url):
    """Scrapes all reviews from Flipkart by automatically following pagination."""
    driver = setup_driver()
    all_reviews = []

    print(f"Navigating to reviews page: {reviews_url}")
    driver.get(reviews_url)

    page_num = 1
    while True:
        print(f"Scraping page {page_num}...")

        try:
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "cPHDOP"))
            )
        except TimeoutException:
            print("Content did not load in time. Ending scrape.")
            break

        soup = BeautifulSoup(driver.page_source, 'html.parser')
        review_blocks = soup.find_all('div', class_='cPHDOP')

        if not review_blocks:
            print("No review blocks found. The website structure may have changed.")
            break

        for block in review_blocks:
            review_text_element = block.find('div', class_='ZmyHeo')
            if review_text_element:
                all_reviews.append(review_text_element.get_text(strip=True))

        # --- Check for "Next" button ---
        try:
            next_button = driver.find_element(By.XPATH, "//a/span[text()='Next']")
            driver.execute_script("arguments[0].click();", next_button)
            time.sleep(2)  # Wait for the next page to load
            page_num += 1
        except NoSuchElementException:
            print("Reached the last page of reviews.")
            break

    driver.quit()
    return all_reviews

# Run scraper
print("Starting Flipkart review scraper...")
scraped_reviews = scrape_flipkart_reviews(REVIEWS_URL)

if scraped_reviews:
    print(f"\nSuccessfully scraped {len(scraped_reviews)} reviews.")
    df = pd.DataFrame(scraped_reviews, columns=['review_text'])
    print(df.head(10))
   # Save the DataFrame to a CSV file
    output_filename = 'reviews.csv'
    df.to_csv(output_filename, index=False, encoding='utf-8')
    print(f"\nSaved all reviews to '{output_filename}'")
else:
    print("\nNo reviews were scraped.")


