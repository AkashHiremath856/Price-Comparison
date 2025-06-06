from bs4 import BeautifulSoup
import requests
import undetected_chromedriver as uc
import time
from django.conf import settings
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
import re
from selenium_stealth import stealth


prefs = {
    "profile.default_content_setting_values.geolocation": 2,    # Block location
    "profile.default_content_setting_values.notifications": 2,  # Block notifications
    "profile.default_content_setting_values.media_stream_mic": 2,   # Block mic
    "profile.default_content_setting_values.media_stream_camera": 2  # Block camera
}

options = uc.ChromeOptions()
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
options.add_argument('--disable-gpu')
options.add_experimental_option("prefs", prefs)

driver = uc.Chrome(options=options)

stealth(driver,
        languages=["en-US", "en"],
        vendor="Google Inc.",
        platform="Win32",
        webgl_vendor="Intel Inc.",
        renderer="Intel Iris OpenGL Engine",
        fix_hairline=True,
        )


def flipkart(name):
    global flipkart
    name1 = name.replace(" ","+")
    flipkart=f'https://www.flipkart.com/search?q={name1}&otracker=search&otracker1=search&marketplace=FLIPKART&as-show=off&as=off'
    driver.get(f'https://www.flipkart.com/search?q={name1}&otracker=search&otracker1=search&marketplace=FLIPKART&as-show=off&as=off')

    print("\nSearching in flipkart....")

    driver.implicitly_wait(5)

    res = driver.page_source
    soup = BeautifulSoup(res,'html.parser')
    
    datas=soup.select("img[loading='eager']")[2]

    parents = datas.find_parents()

    d={}

    price = None
    for parent in parents:
        if '₹' in parent.text:
            price = parent.text.strip()
            break

    match = re.search(r'₹[\d,]+', str(price))

    d['name']=datas['alt']
    d['image']=datas['src']
    d['price']= match.group() if match else None

    print("Flipkart:")
    print(d['name'])
    print(d['price'])
    print("---------------------------------")
        
    return d['price'], d['name'], d['image'], flipkart
    

def amazon(name):
        try:
            amazon_link=f'https://www.amazon.in/s?k={name}'

            driver.get(amazon_link)

            WebDriverWait(driver, 20).until(
                EC.visibility_of_element_located((By.CLASS_NAME, "sg-col-inner"))
            )

            r=driver.find_element(By.CLASS_NAME,'s-image')

            d={}

            d['image']=r.get_attribute('src')

            d['name']=r.get_attribute('alt')

            prices=driver.find_element(By.CLASS_NAME,'a-price-whole')

            match = re.search(r'\d+(?:\.\d+)?',prices.text.replace(',',""))
            d['price']=match.group()

            
            print("Amazon:")
            print(d['name'])
            print(d['price'])
            print("---------------------------------")
        
            return d['price'], d['name'], d['image'], amazon_link        
                

        except:
            print("Amazon: No product found!")
            print("---------------------------------")
            amazon_price = '0'
            amazon_name = '0'
            amazon_link = '0'
            amazon_image = '0'

        return amazon_price, amazon_name[0:50], amazon_image, amazon_link



def gadgetsnow(name):
    try:
        link=f'https://shop.gadgetsnow.com/mtkeywordsearch?SEARCH_STRING={name}'

        driver.get(link)

        WebDriverWait(driver,15).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, "div.product-img-align"))
        )

        res = driver.page_source

        soup = BeautifulSoup(res,'html.parser')

        product_div = soup.find('div', class_='product-img-align')

        data = product_div.find('img') if product_div else None

        d={}

        d['name']=data['alt']
        d['image']=data['src']
        d['price']=soup.find("div",class_='price-details').find_next('span').get_text().strip().replace('`','')

        print("Gadget Snow:")
        print(d['name'])
        print(d['price'])
        print("---------------------------------")

        return d['price'], d['name'], d['image'], link

    except:
        print("GadgetSnow: No product found!")
        print("---------------------------------")
        gadgetsnow_price = '0'
        gadgetsnow_name = '0'
        gadgetsnow_image = '0'
        gadgetsnow_link = '0'
    return gadgetsnow_price, gadgetsnow_name[0:50], gadgetsnow_image, gadgetsnow_link



def croma(name):
    try:
        croma_link=f"https://www.croma.com/searchB?q={name}%3Arelevance&text={name}"

        driver.get(croma_link)

        WebDriverWait(driver, 20).until(
            EC.visibility_of_element_located((By.CLASS_NAME, "product-list"))
        )

        d={}

        products = driver.find_elements(By.TAG_NAME, "img")[1]
        d['image']=products.get_attribute('src')

        product_titles = driver.find_elements(By.CLASS_NAME, "product-title")[0]

        link = product_titles.find_element(By.TAG_NAME, "a")
        d['name']=link.text

        prices = driver.find_elements(By.CLASS_NAME, "plp-srp-new-amount")[0]
        match = re.search(r'\d+(?:\.\d+)?',prices.text.replace(',',""))
        d['price']=match.group()

        
        print("Croma:")
        print(d['name'])
        print(d['price'])
        print("---------------------------------")

        return d['price'], d['name'], d['image'], croma_link
    

    except:
        print("Croma: No product found!")
        print("---------------------------------")
        croma_price = '0'
        croma_name = '0'
        croma_image = '0'
        croma_link = '0'
    return croma_price, croma_name[0:50], croma_image, croma_link
    
    
    
def reliance(name):
    try:
        reliance_link=f"https://www.reliancedigital.in/products?q={name}"
        
        driver.get(reliance_link)

        WebDriverWait(driver,15).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, "div.content"))
                    )

        res = driver.page_source

        soup = BeautifulSoup(res,'html.parser')

        product_div = soup.find("a",class_='product-card-image')

        driver.get(f"https://www.reliancedigital.in{product_div['href']}")

        WebDriverWait(driver,15).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, "img.fy__img"))
                    )

        WebDriverWait(driver,15).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, "div.product-price"))
                    )

        res = driver.page_source

        soup = BeautifulSoup(res,'html.parser')

        data=soup.find('img',class_='pdp-image')

        d={}

        d['name']=data['alt']
        d['image']=data['src']
        prices=soup.find('div',class_='product-price').get_text().replace(',','')
        match = re.search(r'\d+(?:\.\d+)?',prices )
        d['price']=match.group()

        print("Reliance Digital:")
        print(d['name'])
        print(d['price'])
        print("---------------------------------")
    
        return d['price'],d['name'],d['image'],reliance_link

    except:
        print("Reliance: No product found!")
        print("---------------------------------")
        reliance_price = '0'
        reliance_image = '0'
        reliance_name = '0'
        reliance_link = '0'
    return reliance_price, reliance_name[0:50], reliance_image, reliance_link

def convert(a):
    b=a.replace(" ",'')
    c=b.replace("INR",'')
    d=c.replace(",",'')
    d=d.replace("`",'')
    f=d.replace("₹",'')
    g=int(float(f))
    return g