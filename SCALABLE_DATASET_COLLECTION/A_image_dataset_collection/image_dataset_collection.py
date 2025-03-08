import os
import time
import requests
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from PIL import Image

labels = [
        "Dog", "Cat", "Pizza", "Burger", "Skyscraper", 
        "Car", "Bicycle", "Airplane", "Shirt", "Dress", 
        "Planet", "Tree", "Rose", "Ocean", "Mountain",  
        "Human Face", "Train", "Bridge", "Elephant", "Fireworks"
]
#setting up webdriver
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--headless")
driver = webdriver.Chrome(options=chrome_options)

dataset_path = "image_dataset"
os.makedirs(dataset_path, exist_ok=True)

metadata = []

def download_image(url,folder,filename):
        try:
                response = requests.get(url,timeout=5)
                if response.status_code == 200:
                        filepath = os.path.join(folder,filename)
                        with open(filepath, 'wb') as f:
                                f.write(response.content)

                        with Image.open(filepath) as img:
                                width, height = img.size
                                return filepath, width, height

        except Exception as e:
                print(e)
        return None, None, None

for label in labels:
        folder_path = os.path.join(dataset_path,label)
        os.makedirs(folder_path, exist_ok=True)

        search_url = f"https://www.google.com/search?q={label}+photo+-stock+-clipart&tbm=isch&tbs=isz:l"
        driver.get(search_url)
        time.sleep(2)

        body = driver.find_element(By.TAG_NAME, 'body')
        for _ in range(10):
                body.send_keys(Keys.PAGE_DOWN)
                time.sleep(4)

        images = driver.find_elements(By.CSS_SELECTOR, 'img')
        count = 0

        for img in images:
                if count>=50:
                        break
                src = img.get_attribute('src')
                if src and "http" in src:
                        filename = f"{label}_{count+1}.jpg"
                        filepath, width, height = download_image(src,folder_path,filename)
                        if filepath:
                                metadata.append([label,src,filepath,width,height])
                                count += 1

df = pd.DataFrame(metadata, columns=["label","url","filepath","width","height"])
df.to_csv(os.path.join(dataset_path,"image_metadata.csv"), index=False)

driver.quit()
print("Downloaded images successfully")