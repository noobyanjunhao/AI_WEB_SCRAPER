#python3 -m pip install selenium

from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time
import os
from datetime import datetime

# Function to close common pop-ups
def close_popups(driver):
    try:
        close_buttons = driver.find_elements(By.XPATH, "//*[contains(text(), 'close') or contains(text(), 'Close') or contains(text(), 'x') or contains(text(), 'X')]")
        for button in close_buttons:
            button.click()
            time.sleep(1)
    except Exception as e:
        print(f"Could not close the pop-up: {str(e)}")

# Function to remove overlays
def remove_overlays(driver):
    try:
        driver.execute_script("""
            var overlays = document.querySelectorAll('div[role="dialog"], div[role="alert"], div[class*="modal"], div[class*="popup"]');
            overlays.forEach(function(overlay) {
                overlay.remove();
            });
        """)
        time.sleep(1)
    except Exception as e:
        print(f"Could not remove overlays: {str(e)}")

def fill_zip_code_generic(driver, zip_code="10001", input_xpath='//*[@id="pie-store-finder-modal-search-field"]', button_selector="#sf-search-icon"):
    """
    Generic function to fill in a zip code in a pop-up.
    
    Parameters:
    - driver: Selenium WebDriver instance.
    - zip_code: The zip code to enter.
    - input_xpath: XPath of the zip code input field.
    - button_selector: CSS selector of the button to submit the zip code.
    """
    try:
        # Wait until the input is visible and enabled
        zip_input = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, input_xpath))
        )
        
        # Enter the zip code
        zip_input.clear()
        zip_input.send_keys(zip_code)
        
        # Wait until the button is clickable
        submit_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, button_selector))
        )
        submit_button.click()
        
        print("Zip code filled and submitted.")
        time.sleep(3)  # Wait for the page to reload with updated information

    except (NoSuchElementException, TimeoutException) as e:
        print(f"Could not find zip code input or submit button: {str(e)}")
    except ElementNotInteractableException:
        print("Element found but not interactable; retrying...")
        time.sleep(2)  # Small delay before retrying
        fill_zip_code_generic(driver, zip_code, input_xpath, button_selector)  # Retry the function



from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import time

def scroll_and_click_load_more(driver, max_scrolls=20):
    scroll_pause_time = 2  # Time to wait after each scroll
    screen_height = driver.execute_script("return window.innerHeight")
    scroll_position = 0
    total_height = driver.execute_script("return document.body.scrollHeight")
    scrolls = 0

    while scrolls < max_scrolls:
        # Scroll down by one screen size
        driver.execute_script(f"window.scrollTo(0, {scroll_position + screen_height});")
        time.sleep(scroll_pause_time)  # Allow time for new content to load
        
        # Update scroll position
        scroll_position += screen_height
        scrolls += 1

        # Check if the page height has changed (i.e., more content loaded)
        new_total_height = driver.execute_script("return document.body.scrollHeight")

        # If the page has not loaded more content, break the loop
        if new_total_height == total_height:
            # Look for the "Load More" button using its specific `data-qa` attribute or class
            try:
                load_more_button = driver.find_element(By.CSS_SELECTOR, 'button[data-qa="srch-grd-ld-btn"]')
                if load_more_button:
                    load_more_button.click()  # Click the "Load More" button
                    print(f"'Load More' button clicked.")
                    time.sleep(3)  # Wait for new content to load
                    # Update the total height after loading more content
                    total_height = driver.execute_script("return document.body.scrollHeight")
            except NoSuchElementException:
                # If no more "Load More" button is found, stop scrolling
                print("No more 'Load More' button found.")
                break
        else:
            # If more content is loaded, update total height and continue scrolling
            total_height = new_total_height

    print("Finished scrolling and loading more content.")

# Function to take screenshots per screen-sized portion
def capture_full_page_screenshots(url, base_output_folder='screenshots'):
    # Set up the Chrome options for headless mode
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("--disable-popup-blocking")
    chrome_options.add_argument("--disable-notifications")

    # Path to the ChromeDriver (Ensure it is in your PATH or provide full path)
    driver_path = '/usr/local/bin/chromedriver'  # Replace with your ChromeDriver path
    service = ChromeService(driver_path)
    
    # Initialize the WebDriver
    driver = webdriver.Chrome(service=service, options=chrome_options)
    
    # Load the webpage
    driver.get(url)
    
    # Wait for the page to load fully
    time.sleep(3)
    
    # Call the pop-up closing and overlay removal functions
    close_popups(driver)
    remove_overlays(driver)
    
    # Create a unique output folder with a timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_folder = os.path.join(base_output_folder, f"screenshots_{timestamp}")
    
    # Ensure the output directory exists
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    # Get the initial height of the viewport
    screen_height = driver.execute_script("return window.innerHeight")
    scroll_pause_time = 1  # Time to wait between scrolls
    
    # Start taking screenshots for each screen size portion
    screenshots = []
    scroll_position = 0
    part = 1
    
    scroll_and_click_load_more(driver)

    #get back to the top of the page
    driver.execute_script("window.scrollTo(0, 0);")
    time.sleep(scroll_pause_time)
    
    while True:
        # Save the screenshot for the current viewport
        output_path = f"{output_folder}/screenshot_part_{part}.png"
        driver.save_screenshot(output_path)
        screenshots.append(output_path)
        print(f"Screenshot part {part} saved at {output_path}")
        
        # Scroll down by one screen size
        driver.execute_script(f"window.scrollBy(0, {screen_height});")
        time.sleep(scroll_pause_time)  # Wait for content to load after scrolling
        
        # Recalculate total height after scrolling
        new_scroll_position = driver.execute_script("return window.pageYOffset;")
        new_total_height = driver.execute_script("return document.body.scrollHeight")
        
        # Break if no more content is loaded
        if new_scroll_position + screen_height >= new_total_height:
            break
        
        # Update scroll position
        scroll_position = new_scroll_position
        part += 1

    # Close the browser
    driver.quit()
    
    return screenshots

# Example usage
url = "https://www.starmarket.com/aisle-vs/beverages/bestsellers.html"
screenshot_paths = capture_full_page_screenshots(url)
