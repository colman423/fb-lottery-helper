import time
from urllib.parse import urlparse

def get_input(text, valid_value=[]):
    while True:
        command = input(text)
        try:
            if(command in valid_value or valid_value==[]):
                return command
            else:
                raise ValueError
        except ValueError:
            print("pls enter valid option")

def get_clean_url(url):
    o = urlparse(url)
    clean = o.scheme + "://" + o.netloc + o.path
    if o.path=="/profile.php":
        id = o.query.split('&')[0]
        clean += '?'+id
    return clean

def scrollBottom(driver, val=0, mode="INFINITE", pause_time=0.5):

    if mode=="INFINITE":
        # Get scroll height
        last_height = driver.execute_script("return document.body.scrollHeight")

        while True:
            # Scroll down to bottom
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

            # Wait to load page
            time.sleep(pause_time)

            # Calculate new scroll height and compare with last scroll height
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height
            
    elif mode=="HEIGHT":
        # Get scroll height
        height = driver.execute_script("return document.body.scrollHeight")

        while height < val:
            # Scroll down to bottom
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            # Wait to load page
            time.sleep(pause_time)
            # Calculate new scroll height and compare with last scroll height
            height = driver.execute_script("return document.body.scrollHeight")

    elif mode=="COUNT":
        for i in range(val):
            # Scroll down to bottom
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            # Wait to load page
            time.sleep