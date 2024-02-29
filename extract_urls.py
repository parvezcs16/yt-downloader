from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
def extract_video_urls(url, class_name):
    driver = webdriver.Chrome()
    driver.get(url)

    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.TAG_NAME, 'body')))

    last_height = driver.execute_script("return document.body.scrollHeight")
    retries = 100  # Number of retries

    while retries>0:
        # retries -= 1

        driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.END)
        time.sleep(4)  # Increase the sleep duration

        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            retries -= 1
        else:
            retries = 100  # Reset retries if successful
            last_height = new_height
        # driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.END)
        # time.sleep(2)  # You may need to adjust the sleep duration

        # new_height = driver.execute_script("return document.body.scrollHeight")
        # if new_height == last_height:
        #     break

        # last_height = new_height

    page_source = driver.page_source
    driver.quit()

    soup = BeautifulSoup(page_source, 'html.parser')
    video_elements = soup.find_all('a', {'class': class_name, 'href': True})

    video_urls = ['https://www.youtube.com' + element['href'] for element in video_elements]

    return video_urls

# Example usage:
target_url = 'https://www.youtube.com/@EvilAmityt/shorts'
video_class_name = 'yt-simple-endpoint inline-block style-scope ytd-thumbnail'  # Replace with the actual class name of the video elements
video_urls = extract_video_urls(target_url, video_class_name)

for index, url in enumerate(video_urls, start=1):
    print(f"Video {index}: {url}")
