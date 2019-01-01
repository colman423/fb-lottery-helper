import pickle

def save(driver, path="./config/.cookie"):
    with open(path, 'wb') as filehandler:
        pickle.dump(driver.get_cookies(), filehandler)

def load(driver, path="./config/.cookie"):
    try:
        with open(path, 'rb') as cookiesfile:
            cookies = pickle.load(cookiesfile)
            for cookie in cookies:
                driver.add_cookie(cookie)
    except:
        print("ERROR: 沒有.cookie檔！")
        raise Exception("NO_COOKIE_FILE")
