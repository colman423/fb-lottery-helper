import cookie_helper
from helper import *
from pyquery import PyQuery as pq
from selenium import webdriver
from selenium.common.exceptions import *
from config import config

URL_HOME = "http://www.facebook.com"


def run(post_url, comment_rules, need_like):
    driver = init_driver()
    get_post_page(driver, post_url)

    comment_like_share_wrapper = get_comment_like_share_wrapper(driver)
    comment_people_list = get_comment_people_list(driver, comment_like_share_wrapper, comment_rules)
    if need_like:
        like_people_list = get_like_people_list(driver, comment_like_share_wrapper)
    else:
        like_people_list = []

    driver.quit()
    return like_people_list, comment_people_list


def init_driver():
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_experimental_option("prefs", {
        "profile.managed_default_content_settings.images": 2
    })
    driver = webdriver.Chrome(config.driver_path, options=chrome_options)
    driver.get(URL_HOME)
    return driver

def get_post_page(driver, post_url):
    # login_by_keyboard()
    login_by_cookie(driver)

    try:
        driver.get(post_url)
    except WebDriverException as e:
        error_msg = e.msg
        if "Cannot navigate to invalid URL" in error_msg:
            raise Exception("INVALID_FACEBOOK_URL")

def get_comment_like_share_wrapper(driver):
    posts = driver.find_element_by_css_selector('#content_container #pagelet_group_mall')
    post = posts.find_element_by_css_selector('._4-u2._4-u8')
    post_wrapper = post.find_element_by_css_selector('.userContentWrapper')
    comment_like_share_wrapper = post_wrapper.find_element_by_css_selector('form.commentable_item')
    return comment_like_share_wrapper

def get_comment_people_list(driver, comment_like_share_wrapper, comment_rules):
    print("get_comment_people_list", comment_like_share_wrapper)
    tags_need = comment_rules['TAGS']
    text_need = comment_rules['TEXT']
    comment_wrapper = comment_like_share_wrapper.find_element_by_css_selector('._3w53')
    # print(comment_wrapper)

    while True:     # click "load more" to load all comments
        if pq(comment_wrapper.get_attribute('innerHTML'))('._4sxd'):
            more_link = comment_wrapper.find_element_by_css_selector('._4sxd')
            more_link.click()
            try:
                while pq(more_link.get_attribute('innerHTML'))('span[role="progressbar"]'):
                    pass
            except StaleElementReferenceException:
                pass
        else:
            break

    comment_pq = pq(comment_wrapper.get_attribute('innerHTML'))
    comments = comment_pq('._4eez')
    print( "total {} comments".format( len(comments) ) )

    comment_people_list = []
    for com in comments.items():
        comment_content = com('._3l3x')
        if is_legal_comment_content(comment_content, tag=tags_need, text=text_need):
            print(comment_content.text(), "LEGAL!")
            comment_text = comment_content.text()
            actor_ele = com('._6qw4')
            actor_url = get_clean_url(actor_ele.attr('href'))
            actor_name = actor_ele.text()
            actor_time = com('.livetimestamp').attr('title')
            comment_people_list.append((actor_name, actor_url, comment_text, actor_time))
        else:
            print(comment_content.text(), "ILLEGAL!")
    return comment_people_list

def get_like_people_list(driver, comment_like_share_wrapper):
    print("get_like_people_list", comment_like_share_wrapper)
    like_share_wrapper = comment_like_share_wrapper.find_element_by_css_selector('._3vum')
    like_share_pq = pq(like_share_wrapper.get_attribute('innerHTML'))
    like_link = like_share_pq('._66lg a').attr('href')
    driver.get("https://www.facebook.com"+like_link)

    like_wrapper_list = driver.find_element_by_css_selector('._4bl7._4k2o')

    while pq(like_wrapper_list.get_attribute('innerHTML'))('.uiMorePagerPrimary'):
        try:
            more_link = like_wrapper_list.find_element_by_css_selector('.uiMorePagerPrimary')
            more_link.click()
            time.sleep(1)
        except WebDriverException:
            pass

    like_people_list = []
    like_wrapper_pq = pq(like_wrapper_list.get_attribute('innerHTML'))
    like_actor_list = like_wrapper_pq('.fwb.fcb a')
    for actor in like_actor_list.items():
        actor_url = get_clean_url(actor.attr('href'))
        actor_name = actor.text()
        like_people_list.append((actor_name, actor_url))

    print(f"total {len(like_people_list)} likes")
    # print(like_people_list)
    return like_people_list


def login_by_cookie(driver):
    cookie_helper.load(driver)

def is_legal_comment_content(content, tag=0, text=""):
    try:
        if not content.text():
            raise ValueError
        content.text().lower().index(text.lower())
    except:
        return False
    tagged = len(content('a'))
    return tagged >= tag
