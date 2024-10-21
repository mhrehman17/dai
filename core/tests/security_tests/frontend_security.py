import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import UnexpectedAlertPresentException
from selenium.webdriver.chrome.options import Options
from http import HTTPStatus
import requests

# Security Test Suite for Frontend Security Testing
class TestFrontendSecurity(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Set up Chrome options to include CSP and other necessary security configurations
        chrome_options = Options()
        chrome_options.add_argument("--headless")  # Run headless browser for testing
        cls.driver = webdriver.Chrome(service=Service(), options=chrome_options)
        cls.base_url = "http://localhost:8000"  # Replace with the appropriate base URL of your application

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()

    # Cross-Site Scripting (XSS) Testing
    def test_xss_vulnerabilities(self):
        urls_to_test = [
            f"{self.base_url}/agents",
            f"{self.base_url}/training",
            f"{self.base_url}/metrics"
        ]
        for url in urls_to_test:
            self.driver.get(url)
            try:
                # Test all input fields for XSS
                inputs = self.driver.find_elements(By.TAG_NAME, "input")
                for input_field in inputs:
                    input_field.send_keys('<script>alert("XSS")</script>')
                    input_field.send_keys(Keys.RETURN)
                    WebDriverWait(self.driver, 2).until(EC.alert_is_present())
                    # If an alert is found, fail the test
                    self.fail(f"XSS vulnerability found on page: {url}")
            except UnexpectedAlertPresentException:
                # If alert is present, XSS vulnerability is confirmed
                self.fail(f"XSS vulnerability detected on page: {url}")
            except Exception:
                pass  # No XSS vulnerability detected

    # Content Security Policy (CSP) Testing
    def test_content_security_policy(self):
        response = requests.get(self.base_url)
        csp_header = response.headers.get("Content-Security-Policy")
        self.assertIsNotNone(csp_header, "CSP header is not set for the application")
        self.assertIn("default-src 'self'", csp_header, "CSP policy is not restrictive enough")

    # Clickjacking Prevention Testing
    def test_clickjacking_protection(self):
        response = requests.get(self.base_url)
        x_frame_options = response.headers.get("X-Frame-Options")
        self.assertIsNotNone(x_frame_options, "X-Frame-Options header is missing")
        self.assertIn("DENY", x_frame_options, "Clickjacking protection is not configured correctly")

    # Session Management Testing
    def test_session_management(self):
        self.driver.get(self.base_url)
        # Test for session fixation
        login_field = self.driver.find_element(By.NAME, "username")
        password_field = self.driver.find_element(By.NAME, "password")
        login_field.send_keys("test_user")
        password_field.send_keys("test_password")
        password_field.send_keys(Keys.RETURN)
        # Verify that session is established
        cookies = self.driver.get_cookies()
        self.assertTrue(any(cookie for cookie in cookies if cookie["name"] == "sessionid"), "Session ID cookie is missing")

        # Test for improper session termination
        logout_button = self.driver.find_element(By.ID, "logout")
        logout_button.click()
        cookies_after_logout = self.driver.get_cookies()
        self.assertFalse(any(cookie for cookie in cookies_after_logout if cookie["name"] == "sessionid"), "Session was not properly terminated")

    # Data Encryption Testing
    def test_data_encryption(self):
        # Check that HTTPS is used for all scripts and API calls
        response = requests.get(self.base_url, verify=True)
        self.assertEqual(response.status_code, HTTPStatus.OK, "Website is not using HTTPS correctly")
        for script in self.driver.find_elements(By.TAG_NAME, "script"):
            src = script.get_attribute("src")
            if src:
                self.assertTrue(src.startswith("https://"), f"Insecure script source found: {src}")

if __name__ == "__main__":
    unittest.main()
