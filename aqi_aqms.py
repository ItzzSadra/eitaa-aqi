from __future__ import annotations

from time import sleep

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By


AQMS_URL = "https://aqms.doe.ir/App/"


def get_aqi(city: str) -> str | None:
    """
    Retrieve the AQI value for the given city from the AQMS website.

    Returns the raw AQI text (e.g. "42"). The caller is responsible
    for converting it to an integer and handling errors.
    """
    options = Options()
    driver = webdriver.Chrome(options=options)

    try:
        driver.get(AQMS_URL)
        sleep(0.5)

        city_menu = driver.find_element(By.CLASS_NAME, "province")
        city_menu.click()
        print("Opened city menu")
        sleep(0.7)

        city_button = driver.find_element(
            By.XPATH,
            f"//button[contains(@class, 'mat-menu-item') and contains(text(), ' {city} ')]",
        )
        city_button.click()
        print(f"Selected city: {city}")
        sleep(2)

        value = driver.find_element(
            By.XPATH,
            "//*[@id[starts-with(., 'highcharts-')]]/div/div[1]/span/div/span[1]",
        ).text
        print("AQI value retrieved from page")

        return value
    finally:
        driver.quit()


if __name__ == "__main__":
    city_aqi = get_aqi("اصفهان")
    if city_aqi is not None:
        print(f"AQI in Isfahan: {city_aqi}")
