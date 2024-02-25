from bs4 import BeautifulSoup
import requests
import csv
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

HEADERS = ({'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:123.0) Gecko/20100101 Firefox/123.0', 'Accept-Language': 'en-US, en;q=0.5'})

def extract_amazon_info(url, H):
    response = requests.get(url, headers=H)
    soup = BeautifulSoup(response.text, 'html.parser')


    product_name_element = soup.find("span", attrs={'id': 'productTitle'})
    if product_name_element:
        product_name = product_name_element.get_text(strip=True)
    else:
        product_name = "Product Name Not Found"

    store_name = "Amazon"  

    price_element = soup.find("span", attrs={'class': 'a-size-medium a-color-price'})
    if price_element:
        price = price_element.get_text(strip=True)
    else:
        price = "Price Not Found"

    return {'product_name': product_name, 'store_name': store_name, 'price': price}



def search_google_shopping(product_name, max_price):
    driver = webdriver.Chrome()
    driver.get("https://www.google.com/shopping")
    search_bar = driver.find_element(By.NAME, "q")
    search_bar.send_keys(product_name)
    search_bar.send_keys(Keys.RETURN)
    time.sleep(5)
    time.sleep(10)

    product_listings = []
    name_tags = driver.find_elements(By.CSS_SELECTOR, '.tAxDx')
    href_tags = driver.find_elements(By.CSS_SELECTOR, '.shntl')
    price_tags = driver.find_elements(By.CSS_SELECTOR, '.QIrs8')
    for name_tag, href_tag, price_tag in zip(name_tags, href_tags, price_tags):
        product_name = name_tag.text
        href = href_tag.get_attribute('href')
        price = price_tag.text
        product_listings.append({'product_name': product_name, 'href': href, 'price': price_tag })
    return product_listings


def export_to_csv(data):
    with open('product_listings.csv', mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=['product_name', 'href', 'price'])
        writer.writeheader()
        for item in data:
            writer.writerow({'product_name': item['product_name'], 'href': item['href'], 'price': item['price']})


if __name__ == "__main__":
    amazon_url = 'https://www.amazon.in/Apple-iPhone-Plus-128GB-Product/dp/B0BDK2FSZ5/ref=sr_1_2?dib=eyJ2IjoiMSJ9.o3kzGI7TOjTJ4wOaa1rxwz2JsTyjg_jNmyH-I6F67bDzcYMXAcLk-pnUuQmdkS0Rbqzc5yU0V25aSKzM-ZkHhksm2m_XDRRTrXj6hjoYLnBGtXX7N_dHdzJNvdRfiMrXoUfmU-IqLTGO8rEPo8fGMYS7OUg4iPfn0QS6b04u6IAKLqh4-aHAKovQrpcDbsXggwNB7RkJv4JsD6jbyLzd2OQYE7Xcdam_Lit6ZvJobTI.zxA3McodvsrwVbi9SwfFedB8QPvhNpuZDTX3fXnfKGI&dib_tag=se&keywords=iPhone&qid=1708853428&sr=8-2-spons&sp_csd=d2lkZ2V0TmFtZT1zcF9hdGY&psc=1'
    product_info = extract_amazon_info(amazon_url, HEADERS)
    print(product_info)
    filtered_listings = search_google_shopping(product_info['product_name'], product_info['price'])
    filtered_listings = search_google_shopping("iPhone", "$1000")
    export_to_csv(filtered_listings)
