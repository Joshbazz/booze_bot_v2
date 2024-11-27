import os
import time
import random
import logging
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from html_parser import parse_whiskey_html

# Configure logging
logs_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'logs')
os.makedirs(logs_dir, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(message)s',
    handlers=[
        logging.FileHandler(os.path.join(logs_dir, "scraper.log")),
        logging.StreamHandler()
    ]
)

class WhiskeyScraper:
    def __init__(self):
        """Initialize the WhiskeyScraper class."""
        self.driver = None
        self.wait = None
        
    def setup_driver(self, headless=False):
            """Set up Selenium WebDriver with required options."""
            chrome_options = Options()
            
            # Basic configuration
            chrome_options.add_argument("--start-maximized")
            chrome_options.add_argument("--window-size=1920,1080")
            
            # Anti-detection measures
            chrome_options.add_argument("--disable-blink-features=AutomationControlled")
            chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
            chrome_options.add_experimental_option("useAutomationExtension", False)
            
            # User agent and headers
            chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
            chrome_options.add_argument("accept=text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8")
            chrome_options.add_argument("accept-language=en-US,en;q=0.5")
            
            # Security configurations
            chrome_options.add_argument("--ignore-certificate-errors")
            chrome_options.add_argument("--allow-insecure-localhost")
            
            if headless:
                chrome_options.add_argument("--headless=new")
                chrome_options.add_argument("--disable-gpu")
                chrome_options.add_argument("--no-sandbox")
                chrome_options.add_argument("--disable-dev-shm-usage")

            try:
                # Explicitly specify Chrome path and use absolute path for ChromeDriver
                driver_path = "/usr/local/bin/chromedriver"
                
                # Create Service object with explicit path
                service = Service(executable_path=driver_path)
                
                # Instantiate Chrome WebDriver with explicit service
                self.driver = webdriver.Chrome(
                    service=service,
                    options=chrome_options
                )
                
                # Increase timeout and add connection retries
                self.driver.set_page_load_timeout(30)  # 30 seconds page load timeout
                
                # Set up WebDriverWait for explicit waits with increased timeout
                self.wait = WebDriverWait(self.driver, 15)
                
                # Additional anti-detection measures
                self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
                
            except Exception as e:
                logging.error(f"Failed to initialize Chrome driver: {e}")
                # Add more detailed error logging
                logging.error(f"Driver path: {driver_path}")
                raise

    def scrape_page_once(self):
        """Scrape the whiskey release page once."""
        if not self.driver:
            self.setup_driver(headless=True)
            
        try:
            # Navigate to main page with explicit wait
            self.driver.get("http://www.finewineandgoodspirits.com/")
            time.sleep(2)  # Allow initial page load
            
            # Handle age verification popup with explicit wait
            try:
                age_verification_xpath = "/html/body/div[1]/header/section/div[3]/div[3]/div/div/div/div/div[3]/button"
                self.wait_and_click(By.XPATH, age_verification_xpath)
            except Exception as e:
                logging.warning(f"Age verification handling failed: {e}")

            # Navigate to whiskey release page
            try:
                dropdown_xpath = '//*[@id="root"]/header/section/div[3]/div[1]/section[2]/div[1]/section/div/section/div[4]/div'
                dropdown = self.wait.until(EC.presence_of_element_located((By.XPATH, dropdown_xpath)))
                
                actions = ActionChains(self.driver)
                actions.move_to_element(dropdown).perform()
                
                whiskey_link = self.wait.until(
                    EC.presence_of_element_located((By.XPATH, "//a[@href='whiskey-release/whiskey-release']"))
                )
                whiskey_link.click()
                
            except Exception as e:
                logging.warning(f"Navigation failed, trying direct URL: {e}")
                self.driver.get("http://www.finewineandgoodspirits.com/whiskey-release/whiskey-release")

            # Get and save the page content
            html_content = self.driver.page_source
            timestamp = datetime.now().strftime("%m/%d/%y %H:%M:%S")

            # Save HTML to the data directory
            data_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data')
            os.makedirs(data_dir, exist_ok=True)

            file_path = os.path.join(data_dir, 'whiskey_page.html')
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(html_content)

            logging.info(f"HTML content saved to 'whiskey_page.html' at {timestamp}")

            # Parse HTML content
            logging.info("Parsing HTML data...")
            parse_whiskey_html(html_content)
            logging.info(f"HTML data parsed at {timestamp}")
            
        except Exception as e:
            logging.error(f"Scraping failed: {e}")
            
        finally:
            if self.driver:
                self.driver.quit()
                self.driver = None

    def start_scraper(self, iterations=6, min_sleep=60, max_sleep=90):
        """
        Start the scraper loop for multiple iterations.
        
        Args:
            iterations (int): Number of scraping iterations.
            min_sleep (int): Minimum time (in seconds) to sleep between scrapes.
            max_sleep (int): Maximum time (in seconds) to sleep between scrapes.
        """
        logging.info(f"Starting scraper with {iterations} iterations...")
        for i in range(iterations):
            try:
                logging.info(f"Starting iteration {i+1}/{iterations}")
                self.scrape_page_once()
                
                if i < iterations - 1:  # Skip sleep after the last iteration
                    sleep_time = random.randint(min_sleep, max_sleep)
                    logging.info(f"Sleeping for {sleep_time} seconds before next iteration...")
                    time.sleep(sleep_time)
                    
            except Exception as e:
                logging.error(f"Error in iteration {i+1}: {e}")
                continue  # Continue to next iteration even if current one fails
                
        logging.info("Scraping iterations completed")