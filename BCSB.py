from selenium import webdriver
import time
import os
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from itertools import zip_longest
import csv
import sys

options = Options()
options.add_argument('--ignore-certificate-errors')
options.add_argument('--ignore-ssl-errors')
options.add_argument('--no-sandbox')
options.add_argument("--remote-debugging-port=9222")
options.add_argument("--start-maximized")
options.add_argument("--headless")
options.add_argument('--disable-gpu')
options.add_argument("--window-size=1920,1080")
options.add_argument('--allow-running-insecure-content')
options.add_argument("--disable-extensions")
options.add_argument('--disable-dev-shm-usage')
options.add_argument("--allow-insecure-localhost")
options.add_argument(f"user-data-dir={os.path.abspath('selenium')}")
options.add_argument("--log-level=3")
options.add_argument('--disable-blink-features=AutomationControlled')
options.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.3538.77 Safari/537.36")


def BCSB():
    with open('keywords.txt', 'r') as f:
        KEYS = [line.rstrip('\n') for line in f]
    
    loginText = 'chunk voice thrive ugly doctor heavy embrace rose range divide cheese run'
    driver = webdriver.Chrome(ChromeDriverManager(cache_valid_range=30).install(), options=options)
    
    driver.get('https://bitclout.com/browse')
    time.sleep(3)
    
    try:
        loginPage = WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH, "//a[contains(text(), 'Login')]")))
        driver.execute_script("arguments[0].click();", loginPage)
        
        tabX = driver.window_handles[1]
        driver.close()
        driver.switch_to.window(tabX)
        time.sleep(1)
        
        login = WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH, "//textarea[@placeholder='Enter your secret phrase here.']")))
        login.send_keys(loginText)
        time.sleep(3)
        loadAccount = WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Load Account')]")))
        loadAccount.click()
        time.sleep(3)
    except:
        pass
    
    header = True
    
    Values = []
    curVal = 0
    while True:
        WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH, "//div/feed-post/div/a/div/div[2]/div[@class='roboto-regular mt-1']")))
        feedPosts = driver.find_elements_by_xpath("//div/feed-post/div/a/div/div[@class='w-100']")
        
        for feedPost in feedPosts[curVal:]:
            try:
                keys = []
                value = []
                
                text = feedPost.find_element_by_xpath(".//div[@class='roboto-regular mt-1']").text
                username = feedPost.find_element_by_xpath(".//div[1]/a").text
                userURL = feedPost.find_element_by_xpath(".//div[1]/a").get_attribute('href')
                for KEY in KEYS:
                    if KEY in text:
                        keys.append(KEY)
                        
                if len(keys) >= 1:
                    value = [username, userURL, text] + keys
                    if value not in Values:
                        Values.append(value)
                        
                        with open("output.csv", 'a+', encoding="utf-8-sig", newline='', errors='ignore') as myfile:
                            wr = csv.writer(myfile, dialect='excel')
                            if header == True:
                                wr.writerow(("Username", "Profile URL", "Post Text", "Keywords Found"))
                                header = False
                            wr.writerow(value)
            except Exception as e:
                print('Unexpected Error: ' + str(e))
                
        print('Number of posts:', len(feedPosts))
        print('Number of Values:', len(Values))
        
        loadMore = WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH, "//div[contains(text(), 'Load More')]")))
        driver.execute_script("arguments[0].scrollIntoView();", loadMore)
        driver.execute_script("arguments[0].click();", loadMore)
        time.sleep(1)
        
        curVal = len(feedPosts)
    
BCSB()
