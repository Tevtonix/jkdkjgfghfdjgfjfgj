import allure
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from typing import Optional, List
import logging

logger = logging.getLogger(__name__)


class BasePage:
    """Base page class for all page objects"""
    
    def __init__(self, driver: WebDriver, wait: WebDriverWait, base_url: str):
        self.driver = driver
        self.wait = wait
        self.base_url = base_url
    
    @allure.step("Open URL: {url}")
    def open(self, url: str) -> "BasePage":
        """Open URL and return self for chain calls"""
        self.driver.get(url)
        return self
    
    @allure.step("Get current URL")
    def get_current_url(self) -> str:
        """Get current page URL"""
        return self.driver.current_url
    
    @allure.step("Find element by locator")
    def find_element(self, by: str, value: str):
        """Find element with explicit wait"""
        try:
            return self.wait.until(EC.presence_of_element_located((by, value)))
        except TimeoutException:
            logger.error(f"Element not found: {by}={value}")
            raise
    
    @allure.step("Find elements by locator")
    def find_elements(self, by: str, value: str) -> List:
        """Find multiple elements with explicit wait"""
        try:
            return self.wait.until(EC.presence_of_all_elements_located((by, value)))
        except TimeoutException:
            logger.error(f"Elements not found: {by}={value}")
            return []
    
    @allure.step("Click element: {by}={value}")
    def click(self, by: str, value: str) -> "BasePage":
        """Click element and return self for chain calls"""
        element = self.find_element(by, value)
        element.click()
        return self
    
    @allure.step("Input text: {text} to element: {by}={value}")
    def input_text(self, by: str, value: str, text: str) -> "BasePage":
        """Input text to element and return self for chain calls"""
        element = self.find_element(by, value)
        element.clear()
        element.send_keys(text)
        return self
    
    @allure.step("Get text from element: {by}={value}")
    def get_text(self, by: str, value: str) -> str:
        """Get text from element"""
        element = self.find_element(by, value)
        return element.text
    
    @allure.step("Get attribute {attr} from element: {by}={value}")
    def get_attribute(self, by: str, value: str, attr: str) -> Optional[str]:
        """Get attribute from element"""
        element = self.find_element(by, value)
        return element.get_attribute(attr)
    
    @allure.step("Check if element is visible: {by}={value}")
    def is_element_visible(self, by: str, value: str) -> bool:
        """Check if element is visible"""
        try:
            element = self.wait.until(EC.visibility_of_element_located((by, value)))
            return element.is_displayed()
        except (TimeoutException, NoSuchElementException):
            return False
    
    @allure.step("Wait for element to be visible: {by}={value}")
    def wait_for_element_visible(self, by: str, value: str, timeout: int = 10) -> "BasePage":
        """Wait for element to be visible and return self for chain calls"""
        self.wait.until(EC.visibility_of_element_located((by, value)))
        return self
    
    @allure.step("Wait for element to be clickable: {by}={value}")
    def wait_for_element_clickable(self, by: str, value: str, timeout: int = 10) -> "BasePage":
        """Wait for element to be clickable and return self for chain calls"""
        self.wait.until(EC.element_to_be_clickable((by, value)))
        return self
    
    @allure.step("Wait for URL to contain: {expected_url_part}")
    def wait_for_url_contains(self, expected_url_part: str, timeout: int = 10) -> "BasePage":
        """Wait for URL to contain specific text and return self for chain calls"""
        self.wait.until(EC.url_contains(expected_url_part))
        return self
    
    @allure.step("Wait for URL to be: {expected_url}")
    def wait_for_url_to_be(self, expected_url: str, timeout: int = 10) -> "BasePage":
        """Wait for URL to be exact match and return self for chain calls"""
        self.wait.until(EC.url_to_be(expected_url))
        return self