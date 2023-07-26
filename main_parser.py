import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import time
import re
from urllib.parse import unquote
import random
import json

headers = {
    "accept" : "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "user-agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 YaBrowser/23.7.0.2534 Yowser/2.5 Safari/537.36"
} 


def get_source_html(url):
    s = Service(executable_path="C:\\Users\\Andrew\\OneDrive\\Рабочий стол\\Python\\Selenium\\chromedriver\\chromedriver.exe")
    driver = webdriver.Chrome(service=s)

    driver.maximize_window()

    try:
        driver.get(url=url)
        time.sleep(3)

        while True:
            find_more_element = driver.find_element(By.CLASS_NAME, "catalog-button-showMore")

            if driver.find_elements(By.CLASS_NAME, "button-show-more"):
                with open("source-page.html", "w", encoding="utf-8") as file:
                    file.write(driver.page_source)
                break
            else:
                actions = ActionChains(driver)
                actions.move_to_element(find_more_element).perform()
                # driver.find_element(By.CLASS_NAME,"button-show-more").click()
                
                time.sleep(3)
                

    except Exception as _ex:
        print(_ex)
    finally:
        driver.close()
        driver.quit()   

def get_items_urls(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        src = file.read()
    soup = BeautifulSoup(src, "lxml")
    items_divs = soup.find_all("div", class_="minicard-item__info")

    urls = []

    for item in items_divs:
        
        item_url = item.find("a", class_="js-item-url").get("href")
        urls.append(item_url)

    with open("item_urls.txt", "w", encoding='utf-8') as file:
        for url in urls:
            file.write(f"{url}\n")

    return "[INFO] Urls collected successfully!"

def get_data(file_path):

    with open(file_path) as file:
        urls_list = file.readlines()
    
        clear_list = []
        for url in urls_list:
            url = url.strip()
            clear_list.append(url)
        # print(clear_list)
    result_list = []
    url_count = len(urls_list)
    count = 1

    for url in clear_list:
        response = requests.get(url=url, headers=headers)
        soup = BeautifulSoup(response.text,"lxml")

        try:
            item_name = soup.find("span",{"itemprop":"name"}).text.strip()
        except Exception as _ex:
            item_name = None

        item_phones_list = []

        try:
            item_phones = soup.find("div", class_="service-phones-list").find_all("a", class_="js-phone-number")
            for phone in item_phones:
                item_phone = phone.get("href").split(":")[-1].strip()
                item_phones_list.append(item_phone)
        except Exception as _ex:
            item_phones_list = None

        try:
            item_address = soup.find("address", class_="iblock").text.strip()
        except Exception as _ex:
            item_address = None

        try:
            item_site = soup.find(text=re.compile("Сайт|Официальный сайт")).find_next().text.strip()
        except Exception as _ex:
            item_site = None

        social_network_list = []
        try:
            item_social_networks = soup.find(text=re.compile("Страница в соцсетях")).find_next().find_all("a")

            for sn in item_social_networks:
                sn_url = sn.get("href")
                # режем не красивую ссылку с редиректами на прямую
                sn_url = unquote(sn_url.split("?to=")[1].split("&")[0])
                social_network_list.append(sn_url)
        except Exception as _ex:
            social_network_list = None

        result_list.append(
            {
                "item_name":item_name,
                "item_url":url,
                "item_phone_list":item_phones_list,
                "item_address":item_address,
                "item_site":item_site,
                "social_network_list":social_network_list,
            }
        )

        time.sleep(random.randrange(2,5))
        # print (item_name,item_phones_list,item_address)
        if count%10 == 0:
            time.sleep(random.randrange(5,7))
        print(f"[+] Processed: {count}/{url_count}")
        count +=1


    with open ("parce_result.json","w") as file:
        json.dump(result_list, file, indent=4, ensure_ascii=False)
        
    return "[INFO] Data collected successfully!"



def main():
    # get_source_html(url="https://spb.zoon.ru/medical/")
    # print(get_items_urls(file_path="C:\\Users\Andrew\\OneDrive\\Рабочий стол\\Python\\Selenium\\chromedriver\\source-page.html"))
    print(get_data(file_path="C:\\Users\\Andrew\\OneDrive\\Рабочий стол\\Python\\Selenium\\chromedriver\\item_urls.txt"))

if __name__ == "__main__":
    main()