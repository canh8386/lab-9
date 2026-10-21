import os
from pathlib import Path
import tempfile

import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait


def _find_chromedriver() -> str | None:
    """Find an explicitly configured or locally cached ChromeDriver.

    Using a local driver avoids Selenium Manager attempting a network download
    in restricted/offline test environments.
    """
    configured = os.getenv("CHROMEDRIVER")
    if configured and Path(configured).is_file():
        return configured

    cache_root = Path.home() / ".cache" / "selenium" / "chromedriver"
    cached = sorted(
        cache_root.glob("**/chromedriver.exe"),
        key=lambda path: path.stat().st_mtime,
        reverse=True,
    )
    return str(cached[0]) if cached else None


@pytest.fixture
def driver():
    options = Options()
    chrome_binary = os.getenv(
        "CHROME_BINARY",
        r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    )
    if Path(chrome_binary).is_file():
        options.binary_location = chrome_binary
    if os.getenv("HEADLESS", "0") == "1":
        options.add_argument("--headless=new")
    options.add_argument(f"--user-data-dir={tempfile.mkdtemp(prefix='saucedemo-chrome-')}")
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--no-sandbox")
    options.add_argument("--window-size=1366,900")

    driver_path = _find_chromedriver()
    service = Service(executable_path=driver_path) if driver_path else Service()
    browser = webdriver.Chrome(service=service, options=options)
    browser.set_page_load_timeout(30)
    browser.get("https://www.saucedemo.com/")
    yield browser
    browser.quit()


@pytest.fixture
def wait(driver):
    return WebDriverWait(driver, 15)
