import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.wait import WebDriverWait
from pages.base_page import BasePage


class RegistrationPage(BasePage):
    """Page Object for Registration page"""
    
    # Locators
    FIRST_NAME_INPUT = (By.ID, "customer.firstName")
    LAST_NAME_INPUT = (By.ID, "customer.lastName")
    ADDRESS_INPUT = (By.ID, "customer.address.street")
    CITY_INPUT = (By.ID, "customer.address.city")
    STATE_INPUT = (By.ID, "customer.address.state")
    ZIP_INPUT = (By.ID, "customer.address.zipCode")
    PHONE_INPUT = (By.ID, "customer.phoneNumber")
    SSN_INPUT = (By.ID, "customer.ssn")
    USERNAME_INPUT = (By.ID, "customer.username")
    PASSWORD_INPUT = (By.ID, "customer.password")
    CONFIRM_PASSWORD_INPUT = (By.ID, "repeatedPassword")
    REGISTER_BUTTON = (By.XPATH, "//input[@value='Register']")
    
    ERROR_MESSAGES = (By.CLASS_NAME, "ng-binding")
    SUCCESS_MESSAGE = (By.XPATH, "//h1[contains(text(), 'Welcome')]")
    
    def __init__(self, driver: WebDriver, wait: WebDriverWait, base_url: str):
        super().__init__(driver, wait, base_url)
    
    @allure.step("Enter first name: {first_name}")
    def enter_first_name(self, first_name: str) -> "RegistrationPage":
        """Enter first name - chain method"""
        self.input_text(*self.FIRST_NAME_INPUT, first_name)
        return self
    
    @allure.step("Enter last name: {last_name}")
    def enter_last_name(self, last_name: str) -> "RegistrationPage":
        """Enter last name - chain method"""
        self.input_text(*self.LAST_NAME_INPUT, last_name)
        return self
    
    @allure.step("Enter address: {address}")
    def enter_address(self, address: str) -> "RegistrationPage":
        """Enter address - chain method"""
        self.input_text(*self.ADDRESS_INPUT, address)
        return self
    
    @allure.step("Enter city: {city}")
    def enter_city(self, city: str) -> "RegistrationPage":
        """Enter city - chain method"""
        self.input_text(*self.CITY_INPUT, city)
        return self
    
    @allure.step("Enter state: {state}")
    def enter_state(self, state: str) -> "RegistrationPage":
        """Enter state - chain method"""
        self.input_text(*self.STATE_INPUT, state)
        return self
    
    @allure.step("Enter zip code: {zip_code}")
    def enter_zip_code(self, zip_code: str) -> "RegistrationPage":
        """Enter zip code - chain method"""
        self.input_text(*self.ZIP_INPUT, zip_code)
        return self
    
    @allure.step("Enter phone number: {phone}")
    def enter_phone(self, phone: str) -> "RegistrationPage":
        """Enter phone number - chain method"""
        self.input_text(*self.PHONE_INPUT, phone)
        return self
    
    @allure.step("Enter SSN: {ssn}")
    def enter_ssn(self, ssn: str) -> "RegistrationPage":
        """Enter SSN - chain method"""
        self.input_text(*self.SSN_INPUT, ssn)
        return self
    
    @allure.step("Enter username: {username}")
    def enter_username(self, username: str) -> "RegistrationPage":
        """Enter username - chain method"""
        self.input_text(*self.USERNAME_INPUT, username)
        return self
    
    @allure.step("Enter password: {password}")
    def enter_password(self, password: str) -> "RegistrationPage":
        """Enter password - chain method"""
        self.input_text(*self.PASSWORD_INPUT, password)
        return self
    
    @allure.step("Enter confirm password: {password}")
    def enter_confirm_password(self, password: str) -> "RegistrationPage":
        """Enter confirm password - chain method"""
        self.input_text(*self.CONFIRM_PASSWORD_INPUT, password)
        return self
    
    @allure.step("Click register button")
    def click_register(self) -> "RegistrationPage":
        """Click register button - chain method"""
        self.click(*self.REGISTER_BUTTON)
        return self
    
    @allure.step("Fill registration form with valid data")
    def fill_registration_form(
        self,
        first_name: str = "John",
        last_name: str = "Doe",
        address: str = "123 Main St",
        city: str = "New York",
        state: str = "NY",
        zip_code: str = "12345",
        phone: str = "1234567890",
        ssn: str = "123-45-6789",
        username: str = "johndoe",
        password: str = "password123"
    ) -> "RegistrationPage":
        """
        Fill complete registration form using chain of calls
        Returns self for method chaining
        """
        return (
            self.enter_first_name(first_name)
            .enter_last_name(last_name)
            .enter_address(address)
            .enter_city(city)
            .enter_state(state)
            .enter_zip_code(zip_code)
            .enter_phone(phone)
            .enter_ssn(ssn)
            .enter_username(username)
            .enter_password(password)
            .enter_confirm_password(password)
        )
    
    @allure.step("Get error messages")
    def get_error_messages(self) -> list:
        """Get all error messages from the page"""
        try:
            errors = self.find_elements(*self.ERROR_MESSAGES)
            return [error.text for error in errors if error.text.strip()]
        except Exception:
            return []
    
    @allure.step("Check if success message is displayed")
    def is_success_message_displayed(self) -> bool:
        """Check if success message is displayed"""
        return self.is_element_visible(*self.SUCCESS_MESSAGE)
    
    @allure.step("Wait for success message")
    def wait_for_success_message(self) -> "RegistrationPage":
        """Wait for success message to appear"""
        self.wait_for_element_visible(*self.SUCCESS_MESSAGE)
        return self