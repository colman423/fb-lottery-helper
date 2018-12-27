import cookie_helper
from helper import *
from pyquery import PyQuery as pq
from selenium import webdriver
from selenium.common.exceptions import *
from config import config

URL_HOME = "http://www.facebook.com"


def run(post_url, comment_rules, need_like):
    driver = init_driver()      # 打開一個chrome driver
    get_post_page(driver, post_url)     # 前往那篇貼文

    comment_like_share_wrapper = get_comment_like_share_wrapper(driver)     # 選取貼文外面的div
    comment_people_list = get_comment_people_list(driver, comment_like_share_wrapper, comment_rules)    # 爬取留言符合的人
    if need_like:       # 如果須按讚
        like_people_list = get_like_people_list(driver, comment_like_share_wrapper)     # 爬取有按讚的人們
    else:               # 如果不用按讚
        like_people_list = []       # 那就算了

    driver.quit()       # 東西都拿到了，你沒有利用價值了，關掉
    return like_people_list, comment_people_list    # return給剛剛叫我做事的東西


def init_driver():
    chrome_options = webdriver.ChromeOptions()      # 額外選項
    chrome_options.add_experimental_option("prefs", {       # 不要顯示圖片，不然要等好久ㄇㄉ
        "profile.managed_default_content_settings.images": 2
    })
    driver = webdriver.Chrome(config.driver_path, options=chrome_options)   # driver路徑以及額外選項
    driver.get(URL_HOME)            # 前往www.facebook.com
    return driver

def get_post_page(driver, post_url):
    # login_by_keyboard(driver)           # 第一次使用，請選擇這個
    login_by_cookie(driver)         # 之後請選擇這個，自動登入

    try:
        driver.get(post_url)        # 前往那篇貼文看看
    except WebDriverException as e: 
        error_msg = e.msg
        if "Cannot navigate to invalid URL" in error_msg:   # url錯了，前往不了
            raise Exception("INVALID_FACEBOOK_URL")

def get_comment_like_share_wrapper(driver):
    posts = driver.find_element_by_css_selector('#content_container #pagelet_group_mall')   # 只是css selector拆成好幾行而已
    post = posts.find_element_by_css_selector('._4-u2._4-u8')
    post_wrapper = post.find_element_by_css_selector('.userContentWrapper')
    comment_like_share_wrapper = post_wrapper.find_element_by_css_selector('form.commentable_item')
    return comment_like_share_wrapper

def get_comment_people_list(driver, comment_like_share_wrapper, comment_rules):     # 爬取留言符合的人
    print("get_comment_people_list", comment_like_share_wrapper)
    tags_need = comment_rules['TAGS']       # how many tags need in comment
    text_need = comment_rules['TEXT']       # what text need in comment
    comment_wrapper = comment_like_share_wrapper.find_element_by_css_selector('._3w53') # get comment wrapper from prev wrapper
    # print(comment_wrapper)

    while True:     # click "load more" to load all comments
        if pq(comment_wrapper.get_attribute('innerHTML'))('._4sxd'):    # if there's "load more" in page
            more_link = comment_wrapper.find_element_by_css_selector('._4sxd')  # select link
            more_link.click()           # click it
            try:
                while pq(more_link.get_attribute('innerHTML'))('span[role="progressbar"]'):    # busy-waiting for comment loading
                    pass
            except StaleElementReferenceException:  # busy-waiting until progressbar not found, click "load more" again
                pass
        else:
            break

    comment_pq = pq(comment_wrapper.get_attribute('innerHTML'))     # all dymanic is fucking done, use pyquery
    comments = comment_pq('._4eez')             # select all comments
    print( "total {} comments".format( len(comments) ) )

    comment_people_list = []            # legal comment people
    for com in comments.items():            # for all comments
        comment_content = com('._3l3x')             # get its content
        if is_legal_comment_content(comment_content, tag=tags_need, text=text_need):    # check if it's legal comment
            print(comment_content.text(), "LEGAL!")
            comment_text = comment_content.text()       # get its text
            actor_ele = com('._6qw4')                   # get commentor's element
            actor_url = get_clean_url(actor_ele.attr('href'))   # get commentor's url
            actor_name = actor_ele.text()               # get commentor's name
            actor_time = com('.livetimestamp').attr('title')    # get comment time
            comment_people_list.append((actor_name, actor_url, comment_text, actor_time))  # push those things into legal comment people
        else:
            print(comment_content.text(), "ILLEGAL!")
    return comment_people_list      # all is done, return this fucking dope shit skr skr

def get_like_people_list(driver, comment_like_share_wrapper):       # get people who like this post
    print("get_like_people_list", comment_like_share_wrapper)
    like_share_wrapper = comment_like_share_wrapper.find_element_by_css_selector('._3vum')      # get like wrapper from prev wrapper
    like_share_pq = pq(like_share_wrapper.get_attribute('innerHTML'))           # use pq to get a href
    like_link = like_share_pq('._66lg a').attr('href')
    driver.get("https://www.facebook.com"+like_link)            # driver go to that page

    like_wrapper_list = driver.find_element_by_css_selector('._4bl7._4k2o')

    while pq(like_wrapper_list.get_attribute('innerHTML'))('.uiMorePagerPrimary'):  # while there's "load more" btn
        try:
            more_link = like_wrapper_list.find_element_by_css_selector('.uiMorePagerPrimary')
            more_link.click()       # click it
            time.sleep(1)           # wait for 1 sec
        except WebDriverException:      # ok, all people is visiable
            pass

    like_people_list = []       # legal like people
    like_wrapper_pq = pq(like_wrapper_list.get_attribute('innerHTML'))  # use pyquery
    like_actor_list = like_wrapper_pq('.fwb.fcb a')         # selector to all people
    for actor in like_actor_list.items():
        actor_url = get_clean_url(actor.attr('href'))       # get liker's profile url
        actor_name = actor.text()                           # get liker's name
        like_people_list.append((actor_name, actor_url))    # push into list

    print(f"total {len(like_people_list)} likes")
    # print(like_people_list)
    return like_people_list


def login_by_keyboard(driver):
    input("press any key after you logined. ")
    cookie_helper.save(driver)
    pass
def login_by_cookie(driver):
    cookie_helper.load(driver)

def is_legal_comment_content(content, tag=0, text=""):
    if not content.text():      # if its fake comment
        return False
    content_half = full_to_half(content.text().lower())     # change to lowercase and half
    text_half = full_to_half(text.lower())              # u 2
    if not text_half in content_half:               # check if this comment has specific text
        return False                                    # if no, 88
    tagged = len(content('a'))                      # check if this comment tag enough people
    return tagged >= tag                                # return answer