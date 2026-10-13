import pytest
import allure
from pages.registration_page import RegistrationPage
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.wait import WebDriverWait
import random
import string


def generate_random_username(length: int = 8) -> str:
    """Generate random username"""
    return "test_" + ''.join(random.choices(string.ascii_lowercase + string.digits, k=length))


def generate_random_password(length: int = 10) -> str:
    """Generate random password"""
    return ''.join(random.choices(
        string.ascii_letters + string.digits + "!@#$%", 
        k=length
    ))


@allure.feature("Registration")
class TestRegistration:
    """Test class for user registration functionality"""
    
    @pytest.fixture(autouse=True)
    def setup(self, driver: WebDriver, wait: WebDriverWait, app_url: str):
        """Setup test fixtures"""
        self.driver = driver
        self.wait = wait
        self.app_url = app_url
        self.registration_page = RegistrationPage(driver, wait, app_url)
    
    @allure.story("Positive Registration")
    @allure.title("Successful user registration with valid data")
    @allure.description("Verify that user can successfully register with all valid data")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.positive
    @pytest.mark.smoke
    def test_positive_registration(self, target_browser: str, registration_url: str):
        """
        Positive test: Successful registration with valid data
        Uses chain of calls pattern
        """
        username = generate_random_username()
        password = generate_random_password()
        
        with allure.step(f"Navigate to registration page for {target_browser}"):
            self.registration_page.open(registration_url)
        
        with allure.step("Fill registration form with valid data"):
            self.registration_page.fill_registration_form(
                first_name="John",
                last_name="Doe",
                address="123 Main Street",
                city="New York",
                state="NY",
                zip_code="12345",
                phone="5551234567",
                ssn="123-45-6789",
                username=username,
                password=password
            ).click_register()
        
        with allure.step("Verify successful registration"):
            self.registration_page.wait_for_success_message()
            assert self.registration_page.is_success_message_displayed(), \
                "Success message should be displayed after registration"
    
    @allure.story("Negative Registration")
    @allure.title("Registration with empty first name")
    @allure.description("Verify that registration fails when first name is empty")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.negative
    def test_registration_empty_first_name(self, target_browser: str, registration_url: str):
        """
        Negative test: Registration with empty first name
        """
        with allure.step(f"Navigate to registration page for {target_browser}"):
            self.registration_page.open(registration_url)
        
        with allure.step("Fill form with empty first name"):
            self.registration_page.fill_registration_form(
                first_name="",  # Empty first name
                last_name="Doe",
                username=generate_random_username(),
                password=generate_random_password()
            ).click_register()
        
        with allure.step("Verify error message is displayed"):
            errors = self.registration_page.get_error_messages()
            assert len(errors) > 0, "Error message should be displayed"
            assert any("first name" in error.lower() for error in errors), \
                f"Error should mention first name. Errors: {errors}"
    
    @allure.story("Negative Registration")
    @allure.title("Registration with empty last name")
    @allure.description("Verify that registration fails when last name is empty")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.negative
    def test_registration_empty_last_name(self, target_browser: str, registration_url: str):
        """
        Negative test: Registration with empty last name
        """
        with allure.step(f"Navigate to registration page for {target_browser}"):
            self.registration_page.open(registration_url)
        
        with allure.step("Fill form with empty last name"):
            self.registration_page.fill_registration_form(
                first_name="John",
                last_name="",  # Empty last name
                username=generate_random_username(),
                password=generate_random_password()
            ).click_register()
        
        with allure.step("Verify error message is displayed"):
            errors = self.registration_page.get_error_messages()
            assert len(errors) > 0, "Error message should be displayed"
            assert any("last name" in error.lower() for error in errors), \
                f"Error should mention last name. Errors: {errors}"
    
    @allure.story("Negative Registration")
    @allure.title("Registration with empty username")
    @allure.description("Verify that registration fails when username is empty")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.negative
    def test_registration_empty_username(self, target_browser: str, registration_url: str):
        """
        Negative test: Registration with empty username
        """
        with allure.step(f"Navigate to registration page for {target_browser}"):
            self.registration_page.open(registration_url)
        
        with allure.step("Fill form with empty username"):
            self.registration_page.fill_registration_form(
                first_name="John",
                last_name="Doe",
                username="",  # Empty username
                password=generate_random_password()
            ).click_register()
        
        with allure.step("Verify error message is displayed"):
            errors = self.registration_page.get_error_messages()
            assert len(errors) > 0, "Error message should be displayed"
            assert any("username" in error.lower() for error in errors), \
                f"Error should mention username. Errors: {errors}"
    
    @allure.story("Negative Registration")
    @allure.title("Registration with empty password")
    @allure.description("Verify that registration fails when password is empty")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.negative
    def test_registration_empty_password(self, target_browser: str, registration_url: str):
        """
        Negative test: Registration with empty password
        """
        with allure.step(f"Navigate to registration page for {target_browser}"):
            self.registration_page.open(registration_url)
        
        with allure.step("Fill form with empty password"):
            self.registration_page.fill_registration_form(
                first_name="John",
                last_name="Doe",
                username=generate_random_username(),
                password=""  # Empty password
            ).click_register()
        
        with allure.step("Verify error message is displayed"):
            errors = self.registration_page.get_error_messages()
            assert len(errors) > 0, "Error message should be displayed"
            assert any("password" in error.lower() for error in errors), \
                f"Error should mention password. Errors: {errors}"
    
    @allure.story("Negative Registration")
    @allure.title("Registration with mismatched passwords")
    @allure.description("Verify that registration fails when password and confirm password don't match")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.negative
    def test_registration_password_mismatch(self, target_browser: str, registration_url: str):
        """
        Negative test: Registration with mismatched passwords
        """
        with allure.step(f"Navigate to registration page for {target_browser}"):
            self.registration_page.open(registration_url)
        
        with allure.step("Fill form with mismatched passwords"):
            self.registration_page.fill_registration_form(
                first_name="John",
                last_name="Doe",
                username=generate_random_username(),
                password="password123"
            ).enter_confirm_password("password456").click_register()  # Different password
        
        with allure.step("Verify error message is displayed"):
            errors = self.registration_page.get_error_messages()
            assert len(errors) > 0, "Error message should be displayed"
            assert any("password" in error.lower() for error in errors), \
                f"Error should mention password mismatch. Errors: {errors}"
    
    @allure.story("Negative Registration")
    @allure.title("Registration with duplicate username")
    @allure.description("Verify that registration fails when username already exists")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.negative
    def test_registration_duplicate_username(self, target_browser: str, registration_url: str):
        """
        Negative test: Registration with duplicate username
        Using a known existing username
        """
        with allure.step(f"Navigate to registration page for {target_browser}"):
            self.registration_page.open(registration_url)
        
        with allure.step("Fill form with duplicate username"):
            self.registration_page.fill_registration_form(
                first_name="John",
                last_name="Doe",
                username="john",  # Likely already exists
                password="password123"
            ).click_register()
        
        with allure.step("Verify error message about duplicate username"):
            errors = self.registration_page.get_error_messages()
            assert len(errors) > 0, "Error message should be displayed"
            assert any("username" in error.lower() or "exists" in error.lower() 
                      for error in errors), \
                f"Error should mention username exists. Errors: {errors}"


@allure.feature("Registration - Additional Tests")
class TestRegistrationEdgeCases:
    """Additional edge case tests for registration"""
    
    @pytest.fixture(autouse=True)
    def setup(self, driver: WebDriver, wait: WebDriverWait, app_url: str):
        """Setup test fixtures"""
        self.driver = driver
        self.wait = wait
        self.app_url = app_url
        self.registration_page = RegistrationPage(driver, wait, app_url)
    
    @allure.story("Edge Cases")
    @allure.title("Registration with special characters in name")
    @allure.description("Verify registration handles special characters in names")
    @allure.severity(allure.severity_level.MINOR)
    @pytest.mark.negative
    def test_registration_special_characters_in_name(self, target_browser: str, registration_url: str):
        """
        Negative test: Registration with special characters
        """
        with allure.step(f"Navigate to registration page for {target_browser}"):
            self.registration_page.open(registration_url)
        
        with allure.step("Fill form with special characters in name"):
            self.registration_page.fill_registration_form(
                first_name="John@123",  # Special characters
                last_name="Doe",
                username=generate_random_username(),
                password=generate_random_password()
            ).click_register()
        
        with allure.step("Verify error or success (depends on validation)"):
            # Either error or success is acceptable
            errors = self.registration_page.get_error_messages()
            success = self.registration_page.is_success_message_displayed()
            assert len(errors) > 0 or success, \
                "Should either show error or succeed"