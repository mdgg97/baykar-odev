from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class NavbarTest:
    def __init__(self, driver):
        self.driver = driver
        self.base_url = "https://kariyer.baykartech.com/"

    def test_navbar(self):
        self.driver.get(self.base_url)
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "nav"))
        )
        navbar_links = self.driver.find_elements(By.CSS_SELECTOR, "nav a")
        for link in navbar_links:
            href = link.get_attribute("href")
            if href:
                self.driver.get(href)
                assert self.driver.title != "", f"Page for {href} did not load properly."

if __name__ == "__main__":
    driver = webdriver.Chrome()
    try:
        test = NavbarTest(driver)
        test.test_navbar()
    finally:
        driver.quit()
