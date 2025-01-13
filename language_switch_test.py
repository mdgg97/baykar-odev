class LanguageSwitchTest:
    def __init__(self, driver):
        self.driver = driver
        self.base_url = "https://kariyer.baykartech.com/"
        self.languages = {
            "TR": "Kariyer - Baykar",
            "EN": "Careers - Baykar",
        }

    def test_language_switch(self):
        self.driver.get(self.base_url)
        for lang_code, expected_title in self.languages.items():
            lang_button = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, f"//button[@lang='{lang_code}']"))
            )
            lang_button.click()
            WebDriverWait(self.driver, 10).until(
                EC.title_is(expected_title)
            )
            assert self.driver.title == expected_title, f"Language {lang_code} failed."

if __name__ == "__main__":
    driver = webdriver.Chrome()
    try:
        test = LanguageSwitchTest(driver)
        test.test_language_switch()
    finally:
        driver.quit()
