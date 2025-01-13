from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.wait import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions as EC


class BaykarCareerTest:
    def __init__(self, driver_path):
        # Initialize WebDriver
        options = Options()
        options.add_argument("--start-maximized")
        self.driver = webdriver.Chrome(service=Service(driver_path), options=options)
        self.wait = WebDriverWait(self.driver, 10)

    def open_site(self, url):
        self.driver.get(url)

    def test_navbar(self):
        print("Testing Navbar (Dynamic)...")
        navbar_elements = self.driver.find_elements(By.CSS_SELECTOR, "nav a")
        for element in navbar_elements:
            href = element.get_attribute("href")  # Ensure it's a valid link
            if href:
                self._click_and_verify(element)

    def test_language_switching(self):
        print("Testing Language Switching (Static)...")
        supported_languages = ["Türkçe", "English"]  # Statik olarak tanımlandı
        for language in supported_languages:
            language_button = self.driver.find_element(By.XPATH, f"//button[text()='{language}']")
            language_button.click()
            self.wait.until(
                EC.text_to_be_present_in_element((By.TAG_NAME, "html"), language)
            )
            print(f"Language '{language}' verified successfully.")

    def test_position_filtering(self):
        print("Testing Position Filtering (Dynamic)...")
        self.wait.until(EC.element_to_be_clickable((By.ID, "filter"))).click()
        
        # Extracting available departments dynamically
        department_dropdown = Select(self.driver.find_element(By.ID, "department"))
        available_departments = [option.text for option in department_dropdown.options]
        print(f"Available departments: {available_departments}")
        
        # Select a specific department
        department_dropdown.select_by_visible_text("Web Yazılım")
        
        # Perform position search
        position_search = self.driver.find_element(By.ID, "position-search")
        position_search.send_keys("Test Uzmanı")
        position_search.send_keys(Keys.RETURN)
        
        # Verify results
        job_titles = self.driver.find_elements(By.CSS_SELECTOR, ".job-title")
        for title in job_titles:
            assert "Test Uzmanı" in title.text, f"Unexpected title: {title.text}"
        print("Position filtering verified successfully.")

    def _click_and_verify(self, element):
        actions = ActionChains(self.driver)
        actions.move_to_element(element).click().perform()
        self.wait.until(EC.presence_of_element_located((By.TAG_NAME, "h1")))
        print(f"Verified page for: {element.text}")
        self.driver.back()  # Navigate back to the main page

    def quit(self):
        self.driver.quit()


# Usage
if __name__ == "__main__":
    driver_path = "/path/to/chromedriver"  # Replace with your ChromeDriver path
    test = BaykarCareerTest(driver_path)

    try:
        # Open the site
        test.open_site("https://kariyer.baykartech.com/")

        # Run tests
        test.test_navbar()
        test.test_language_switching()
        test.test_position_filtering()

    except Exception as e:
        print(f"An error occurred: {e}")

    finally:
        test.quit()
