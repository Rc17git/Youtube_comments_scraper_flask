from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from io import StringIO
import time
import csv
from datetime import datetime

def scrape_youtube_comments_to_csv(video_url, scroll_count):
    # Set up Chrome in headless mode
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')
    driver = webdriver.Chrome(options=chrome_options)

    try:
        # Navigate to the YouTube video
        driver.get(video_url)

        # Scroll down to load more comments
        for _ in range(scroll_count):
            driver.execute_script("window.scrollTo(0, document.documentElement.scrollHeight);")
            time.sleep(2)  # Adjust the sleep time based on your network speed

        # Get the HTML content
        html_content = driver.page_source

        # Parse HTML with BeautifulSoup
        soup = BeautifulSoup(html_content, 'html.parser')

        # Extract comments (adjust the selector as needed)
        comments = soup.find_all('yt-formatted-string', {'id': 'content-text'})

        # Generate a unique filename with a timestamp
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        csv_filename = f'comments_{timestamp}.csv'

        # Create a string buffer to store CSV content
        csv_buffer = StringIO()

        csv_writer = csv.writer(csv_buffer)
        csv_writer.writerow(['Comment'])
        for comment in comments:
            csv_writer.writerow([comment.text.strip()])

        return csv_buffer.getvalue()

    except Exception as e:
        # Handle the error as needed
        print(f"An error occurred: {e}")

    finally:
        # Close the browser window in all cases
        driver.quit()
