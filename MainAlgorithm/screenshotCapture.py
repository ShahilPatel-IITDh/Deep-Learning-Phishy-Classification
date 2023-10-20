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


def capture_full_page_screenshot(url, screenshotFile):

    print("code entered the screenshot capture function")

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

    print("driver initialized")
    
    try:
        driver.get(url)

        time.sleep(10)

        # Handle WebDriverException (e.g., net::ERR_NAME_NOT_RESOLVED)
        if "ERR_NAME_NOT_RESOLVED" in driver.page_source:
            print(f"Error: {url} could not be resolved. Skipping...")
            return
        
        # Get the page height
        page_height = driver.execute_script("return document.body.scrollHeight")

        # Set the initial viewport height
        viewport_height = driver.execute_script("return window.innerHeight")

        # Capture and stitch the screenshots
        screenshots = []

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
        full_page_screenshot.save(screenshotFile)

    except WebDriverException as e:
        # Log the WebDriverException
        logging.error(f"WebDriverException while processing URL: {url}. Error: {str(e)}")
    except Exception as e:
        # Log other exceptions
        logging.error(f"Exception while processing URL: {url}. Error: {str(e)}")

    finally:
        driver.quit()

    print("Code exited the screenshot capture function")

# Example usage:
# if __name__ == "__main__":
#     capture_full_page_screenshot('https://example.com', 'output.png')