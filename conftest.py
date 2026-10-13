import pytest
import allure
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import os
from typing import Generator
import logging

logger = logging.getLogger(__name__)


@pytest.fixture(scope="session")
def app_url(request) -> str:
    """Fixture for getting app URL with CLI override capability"""
    return request.config.getoption("--app-url") or "https://parabank.parasoft.com"


@pytest.fixture(scope="session")
def selenium_grid_url(request) -> str:
    """Fixture for getting Selenium Grid URL with CLI override capability"""
    return request.config.getoption("--selenium-grid-url") or "http://localhost:4444/wd/hub"


def pytest_addoption(parser):
    """Add custom command line options with unique names to avoid plugin conflicts"""
    parser.addoption(
        "--app-url",
        action="store",
        default="https://parabank.parasoft.com",
        help="Base URL for the application under test"
    )
    parser.addoption(
        "--selenium-grid-url",
        action="store",
        default="http://localhost:4444/wd/hub",
        help="Selenium Grid URL for remote execution"
    )
    parser.addoption(
        "--test-browser",
        action="store",
        default="chrome",
        help="Browser to use for testing: chrome or firefox"
    )


@pytest.fixture(params=["chrome", "firefox"], scope="function")
def target_browser(request) -> str:
    """Fixture for multi-browser support (unique name to avoid playwright conflicts)"""
    cli_browser = request.config.getoption("--test-browser")
    if cli_browser:
        return cli_browser.lower()
    return request.param


@pytest.fixture(scope="function")
def driver(request, target_browser: str, selenium_grid_url: str) -> Generator[WebDriver, None, None]:
    """
    Fixture for creating and managing WebDriver instance.
    Supports multi-browser testing and remote execution.
    Implicit wait is set to 0 as required.
    """
    driver_instance = None
    
    try:
        if target_browser == "chrome":
            options = ChromeOptions()
            options.add_argument("--start-maximized")
            options.add_argument("--disable-gpu")
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-dev-shm-usage")
            options.add_argument("--window-size=1920,1080")
        elif target_browser == "firefox":
            options = FirefoxOptions()
            options.add_argument("--start-maximized")
        else:
            raise ValueError(f"Unsupported browser: {target_browser}")
        
        # Try to use remote WebDriver (Selenium Grid), fallback to local
        try:
            driver_instance = webdriver.Remote(
                command_executor=selenium_grid_url,
                options=options
            )
            logger.info(f"Connected to Selenium Grid at {selenium_grid_url}")
        except Exception as grid_error:
            logger.warning(f"Selenium Grid not available, using local browser: {grid_error}")
            if target_browser == "chrome":
                driver_instance = webdriver.Chrome(options=options)
            else:
                driver_instance = webdriver.Firefox(options=options)
        
        # Set implicit wait to 0 as required by the task
        driver_instance.implicitly_wait(0)
        driver_instance.set_page_load_timeout(30)
        
        yield driver_instance
        
    finally:
        if driver_instance:
            driver_instance.quit()


@pytest.fixture(scope="function")
def wait(driver: WebDriver) -> WebDriverWait:
    """Fixture for explicit waits"""
    return WebDriverWait(driver, timeout=10, poll_frequency=0.5)


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    Hook for capturing screenshots and logs on test failure.
    Attaches them to Allure report automatically.
    """
    outcome = yield
    report = outcome.get_result()
    
    if report.when == "call" and report.failed:
        # Get driver from fixture if available
        driver = None
        for fixture in item.funcargs.values():
            if hasattr(fixture, 'get_screenshot_as_png'):
                driver = fixture
                break
        
        if driver:
            with allure.step("Taking screenshot on failure"):
                try:
                    screenshot = driver.get_screenshot_as_png()
                    allure.attach(
                        screenshot,
                        name="screenshot_on_failure",
                        attachment_type=allure.attachment_type.PNG
                    )
                except Exception as e:
                    logger.error(f"Failed to take screenshot: {e}")
            
            with allure.step("Capturing browser logs"):
                try:
                    log_types = driver.log_types
                    for log_type in log_types:
                        logs = driver.get_log(log_type)
                        if logs:
                            log_content = "\n".join([str(log) for log in logs])
                            allure.attach(
                                log_content,
                                name=f"browser_{log_type}_logs",
                                attachment_type=allure.attachment_type.TEXT
                            )
                except Exception as e:
                    logger.error(f"Failed to get browser logs: {e}")
            
            with allure.step("Capturing page source"):
                try:
                    page_source = driver.page_source
                    allure.attach(
                        page_source,
                        name="page_source_on_failure",
                        attachment_type=allure.attachment_type.HTML
                    )
                except Exception as e:
                    logger.error(f"Failed to get page source: {e}")


@pytest.fixture(scope="function")
def registration_url(app_url: str) -> str:
    """Fixture for registration page URL"""
    return f"{app_url}/register.do"