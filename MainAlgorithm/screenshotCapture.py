import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from PIL import Image
import io
import logging

# Configure logging
logging.basicConfig(filename='ScreenshotError.log', level=logging.ERROR)

# Set up Chrome options
chrome_options = Options()
# Run Chrome in headless mode
chrome_options.add_argument("--headless") 
# Disable the GPU 
chrome_options.add_argument("--disable-gpu")
# Disable the sandbox
chrome_options.add_argument("--no-sandbox")
# Disable the DevShmUsage
chrome_options.add_argument("--disable-dev-shm-usage")

# Install and Initialize WebDriver using webdriver_manager (This will not require pre-downloading the chrome driver)
driver = webdriver.Chrome(service=Service(executable_path=ChromeDriverManager().install()), options=chrome_options)
driver.maximize_window()

def capture_full_page_screenshot(url, output_file):
    try:
        driver.get(url)
        
        # Wait for the page to load completely (adjust the timeout as needed)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "body")))


        # Handle WebDriverException (e.g., net::ERR_NAME_NOT_RESOLVED)
        if "ERR_NAME_NOT_RESOLVED" in driver.page_source:
            print(f"Error: {url} could not be resolved. Skipping...")
            return

        # Get the page height
        page_height = driver.execute_script("return document.body.scrollHeight")

        # Set the initial viewport height
        viewport_height = driver.execute_script("return window.innerHeight")

        # Calculate the number of viewport captures needed
        num_captures = (page_height + viewport_height - 1) // viewport_height

        # Capture and stitch the screenshots
        screenshots = []

        # for i in range(num_captures):
        #     screenshot = driver.get_screenshot_as_png()
        #     screenshots.append(Image.open(io.BytesIO(screenshot)))
        #     driver.execute_script(f"window.scrollTo(0, {viewport_height * (i + 1)});")

        #     time.sleep(2)

        for i in range(0, page_height, viewport_height):
            driver.execute_script(f"window.scrollTo(0, {i});")
            time.sleep(2)  # Adjust sleep time as needed
            screenshot = driver.get_screenshot_as_png()
            screenshots.append(Image.open(io.BytesIO(screenshot)))

        # Stitch the screenshots vertically
        full_page_screenshot = Image.new("RGB", (screenshots[0].width, page_height))
        y_offset = 0

        for screenshot in screenshots:
            full_page_screenshot.paste(screenshot, (0, y_offset))
            y_offset += screenshot.height

        # Save the full-page screenshot
        full_page_screenshot.save(output_file)

    except WebDriverException as e:
        # Log the WebDriverException
        logging.error(f"WebDriverException while processing URL: {url}. Error: {str(e)}")
    except Exception as e:
        # Log other exceptions
        logging.error(f"Exception while processing URL: {url}. Error: {str(e)}")
    finally:
        driver.quit()

# Example usage:
# if __name__ == "__main__":
#     capture_full_page_screenshot('https://example.com', 'output.png')