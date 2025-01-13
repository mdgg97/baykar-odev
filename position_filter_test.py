class PositionFilterTest:
    def __init__(self, driver):
        self.driver = driver
        self.base_url = "https://kariyer.baykartech.com/"

    def test_position_filter(self, department, position_keyword):
        self.driver.get(self.base_url)
        department_dropdown = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.ID, "departmentDropdown"))
        )
        department_dropdown.click()

        department_option = self.driver.find_element(By.XPATH, f"//option[text()='{department}']")
        department_option.click()

        search_box = self.driver.find_element(By.ID, "positionSearchBox")
        search_box.send_keys(position_keyword)

        search_button = self.driver.find_element(By.ID, "searchButton")
        search_button.click()

        result_title = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".position-title"))
        ).text

        assert position_keyword.lower() in result_title.lower(), "Search result does not match."

if __name__ == "__main__":
    driver = webdriver.Chrome()
    try:
        test = PositionFilterTest(driver)
        test.test_position_filter("Yazılım", "Mühendis")
    finally:
        driver.quit()
