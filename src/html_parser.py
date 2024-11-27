import os
import json
from bs4 import BeautifulSoup
import logging

# Configure logging to match the scraper's configuration
logs_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'logs')
os.makedirs(logs_dir, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(message)s',
    handlers=[
        logging.FileHandler(os.path.join(logs_dir, "parser.log")),
        logging.StreamHandler()
    ]
)

def parse_whiskey_html(html_content=None):
    """
    Parse the whiskey release HTML content and extract whiskey information.
    Can accept either raw HTML content as a string or read from the saved HTML file.
    """
    try:
        # If no HTML content is provided, read from the saved file
        if html_content is None:
            data_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data')
            html_file_path = os.path.join(data_dir, 'whiskey_page.html')
            
            if not os.path.exists(html_file_path):
                logging.error(f"HTML file not found at {html_file_path}")
                return None
                
            logging.info(f"Reading HTML from {html_file_path}")
            with open(html_file_path, 'r', encoding='utf-8') as f:
                html_content = f.read()

        # Create BeautifulSoup object from the HTML content
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # Find all whiskey cards/items
        whiskey_titles = soup.find_all('h4', class_='card_title_name')
        
        if not whiskey_titles:
            logging.warning("No whiskey titles found in the HTML content")
            
        # List to store all whiskey data
        whiskey_data = []
        
        # Extract data from each whiskey item
        for title in whiskey_titles:
            try:
                # Get the parent card element
                card = title.find_parent('div', class_='card')  # Adjust class name if needed
                
                # Initialize whiskey info dictionary
                whiskey_info = {
                    'name': title.text.strip(),
                    'price': None,
                    'availability_type': None,
                    'store_availability': None,
                    'quantity_available': None,
                    'limit': None
                }
                
                # Extract price
                price_elem = card.find('span', class_='card__price-amount')
                if price_elem:
                    whiskey_info['price'] = price_elem.text.strip()
                
                # Extract online availability
                online_label = card.find('p', class_='online-available-label')
                if online_label:
                    whiskey_info['availability_type'] = online_label.text.strip()
                
                # Extract store availability
                store_avail = card.find('div', class_='availability-label')
                if store_avail:
                    whiskey_info['store_availability'] = store_avail.find('p').text.strip() if store_avail.find('p') else None
                
                # Extract quantity available
                avail_info = card.find('div', class_='availability-info')
                if avail_info:
                    quantity_text = avail_info.find('p')
                    if quantity_text:
                        whiskey_info['quantity_available'] = quantity_text.text.strip()
                
                # Extract limit information
                limit_elem = card.find('p', class_='limited-text')
                if limit_elem:
                    whiskey_info['limit'] = limit_elem.text.strip()
                
                whiskey_data.append(whiskey_info)
                
            except Exception as e:
                logging.error(f"Error processing whiskey card: {e}")
                continue
        
        # Construct the file path to save the JSON in the data directory
        data_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data')
        os.makedirs(data_dir, exist_ok=True)
        json_file_path = os.path.join(data_dir, 'whiskey_data.json')
        
        # Save to JSON file
        with open(json_file_path, 'w', encoding='utf-8') as f:
            json.dump(whiskey_data, f, indent=2)
        
        logging.info(f"Found {len(whiskey_data)} whiskey items")
        logging.info(f"Data saved to {json_file_path}")
        
        return whiskey_data
        
    except TypeError as e:
        logging.error(f"Error encoding data to JSON: {e}")
        return None
        
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")
        return None
        
    finally:
        logging.info("Parsing operation completed")