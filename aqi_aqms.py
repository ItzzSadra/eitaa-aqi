from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep
from selenium.webdriver.chrome.options import Options


def get_aqi(city: str) -> int | None:
    options = Options()
    driver = webdriver.Chrome(options=options)
    # Open Google
    driver.get("https://aqms.doe.ir/App/")
    sleep(2)
    elem = driver.find_element(By.CLASS_NAME, "province")
    elem.click()
    print("opened menu")
    sleep(2)
    btn = driver.find_element(
        By.XPATH, f"//button[contains(@class, 'mat-menu-item') and contains(text(), ' {city} ')]"
    )
    btn.click()
    print("clicked city")
    sleep(1)
    value = driver.find_element(
        By.XPATH, "//*[@id[starts-with(., 'highcharts-')]]/div/div[1]/span/div/span[1]"
    ).text
    print("got value")

    driver.quit()

    return value

if __name__ == "__main__":
    city_aqi = get_aqi("اصفهان")
    if city_aqi is not None:
        print(f"AQI in Isfahan: {city_aqi}")
