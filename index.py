
import requests
from bs4 import BeautifulSoup
import lxml
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException, ElementNotInteractableException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from time import sleep

GOOGLE_FORM = "https://forms.gle/8ZsxgL9WmHe8yFYu5"

for n in range(1, 20, 1):
    try:
        if n == 1:
            URL = "https://www.zillow.com/homes/for_rent/1-_beds/?searchQueryState=%7B%22pagination%22%3A%7B%7D%2C" \
                  "%22usersSearchTerm%22%3Anull%2C%22mapBounds%22%3A%7B%22west%22%3A-122.56276167822266%2C%22east%22%3A-122" \
                  ".30389632177734%2C%22south%22%3A37.69261345230467%2C%22north%22%3A37.857877098316834%7D%2C%22isMapVisible%22" \
                  "%3Atrue%2C%22filterState%22%3A%7B%22fr%22%3A%7B%22value%22%3Atrue%7D%2C%22fsba%22%3A%7B%22value%22%3Afalse%7D" \
                  "%2C%22fsbo%22%3A%7B%22value%22%3Afalse%7D%2C%22nc%22%3A%7B%22value%22%3Afalse%7D%2C%22cmsn%22%3A%7B%22value%22" \
                  "%3Afalse%7D%2C%22auc%22%3A%7B%22value%22%3Afalse%7D%2C%22fore%22%3A%7B%22value%22%3Afalse%7D%2C%22pmf%22%3A%7B" \
                  "%22value%22%3Afalse%7D%2C%22pf%22%3A%7B%22value%22%3Afalse%7D%2C%22mp%22%3A%7B%22max%22%3A3000%7D%2C%22price" \
                  "%22%3A%7B%22max%22%3A872627%7D%2C%22beds%22%3A%7B%22min%22%3A1%7D%7D%2C%22isListVisible%22%3Atrue%2C%22mapZoom" \
                  "%22%3A12%7D "
        else:
            URL = f"https://www.zillow.com/homes/for_rent/1-_beds/{n}_p/?searchQueryState=%7B%22pagination%22%3A%7B" \
                       f"%22currentPage%22%3A{n}%7D%2C%22mapBounds%22%3A%7B%22west%22%3A-122.63417281103516%2C%22east%22%3A-122" \
                       ".23248518896484%2C%22south%22%3A37.675224399132766%2C%22north%22%3A37.87522324852078%7D%2C%22mapZoom%22" \
                       "%3A12%2C%22isMapVisible%22%3Atrue%2C%22filterState%22%3A%7B%22price%22%3A%7B%22max%22%3A872627%7D%2C" \
                       "%22beds%22%3A%7B%22min%22%3A1%7D%2C%22fore%22%3A%7B%22value%22%3Afalse%7D%2C%22mp%22%3A%7B%22max%22" \
                       "%3A3000%7D%2C%22auc%22%3A%7B%22value%22%3Afalse%7D%2C%22nc%22%3A%7B%22value%22%3Afalse%7D%2C%22fr%22%3A" \
                       "%7B%22value%22%3Atrue%7D%2C%22fsbo%22%3A%7B%22value%22%3Afalse%7D%2C%22cmsn%22%3A%7B%22value%22%3Afalse" \
                       "%7D%2C%22fsba%22%3A%7B%22value%22%3Afalse%7D%7D%2C%22isListVisible%22%3Atrue%7D "

        HEADERS = {"Accept-Language": "en-US,en;q=0.9",
                   "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                                 "Chrome/98.0.4758.102 Safari/537.36"}

        chrome_path = "C:\Development\chromedriver_win32\chromedriver.exe"
        service = Service(chrome_path)
        options = webdriver.ChromeOptions()
        options.add_argument("--incognito")
        options.add_argument("start-maximized")

        response = requests.get(url=URL, headers=HEADERS)
        zillow = response.text
        soup = BeautifulSoup(zillow, "lxml")

        links = soup.find_all(name="a", class_="list-card-link")
        h_links = [link.get("href") for link in links]
        house_links = []
        for h_link in h_links:
            if "https" not in h_link:
                house_links.append(f"https://www.zillow.com{h_link}")
            else:
                house_links.append(h_link)
        addresses = soup.find_all(name="address", class_="list-card-addr")
        house_addresses = [address.getText().split(" | ")[-1] for address in addresses]
        prices = soup.find_all(name="div", class_="list-card-price")
        house_prices = [price.getText() for price in prices]
        house_links = list(dict.fromkeys(house_links))

        driver = webdriver.Chrome(service=service, options=options)
        driver.get(GOOGLE_FORM)

        for i in range(len(house_links)):
            address_q = driver.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div[1]/input')
            price_q = driver.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[2]/div/div/div[2]/div/div[1]/div/div[1]/input')
            link_q = driver.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[3]/div/div/div[2]/div/div[1]/div/div[1]/input')
            submit = driver.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[3]/div[1]/div[1]/div')
            address_q.send_keys(house_addresses[i])
            price_q.send_keys(house_prices[i])
            link_q.send_keys(house_links[i])
            submit.click()
            sleep(1)
            submit_new = driver.find_element(By.XPATH, '/html/body/div[1]/div[2]/div[1]/div/div[4]/a')
            submit_new.click()
            sleep(2)
        print(f"Page {n} Completed")
        sleep(3)

    except IndexError:
        print("You're out of Pages")
        break
