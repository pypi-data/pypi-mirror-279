import unittest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from time import sleep
from src import solve_captcha 

class TestCaptchaSolverIntegration(unittest.TestCase):

    def setUp(self):
        options = Options()
        options.add_experimental_option('prefs', {'intl.accept_languages': 'en'})
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        self.driver = webdriver.Chrome(options=options)

    def tearDown(self):
        self.driver.quit()

    def test_solve_recaptcha_integration(self):
        try:
            self.driver.get("https://www.google.com/recaptcha/api2/demo")
            sleep(2)  # Wait for page to load
        except Exception as e:
            self.fail(f"Error navigating to page: {e}")

        try:
            captcha = None
            iframes = self.driver.find_elements(By.TAG_NAME, "iframe")
            for iframe in iframes:
                if iframe.get_attribute("src").startswith("https://www.google.com/recaptcha/api2/anchor"):
                    captcha = iframe
                    break
            if not captcha:
                raise Exception("Captcha iframe not found")
        except Exception as e:
            self.fail(f"Error finding captcha iframe: {e}")

        try:
            solve_captcha(self.driver, captcha)
        except Exception as e:
            self.fail(f"Error solving captcha: {e}")

if __name__ == "__main__":
    unittest.main()
