from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import time
from fake_useragent import UserAgent

# url = "https://stackoverflow.com/"

useragent = UserAgent()

options = webdriver.ChromeOptions()
# options.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36")
options.add_argument(f"user-agent={useragent.random}")

# options.add_argument("--proxy-server=138.128.91.65:8000")

s = Service(executable_path="C:\\Users\\Andrew\\OneDrive\\Рабочий стол\\Python\\Selenium\\chromedriver\\chromedriver.exe",
            options=options)
driver = webdriver.Chrome(service=s)
driver.proxy("138.128.91.65:8000")

try:
    # driver.get(url="https://whatismybrowser.com/detect/what-is-my-user-agent")
    # time.sleep(5)

    driver.get("https://2ip.ru")
    time.sleep(5)

    # driver.get(url=url)
    # time.sleep(5)

    # driver.get_screenshot_as_file("1.png")
    # time.sleep(5)
except Exception as ex:
    print(ex)
finally:
    driver.close()
    driver.quit()