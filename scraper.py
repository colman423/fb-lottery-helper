URL_POST = "https://www.facebook.com/groups/NCCUSTUDENT/permalink/2057386644307431/"
URL_HOME = "http://www.facebook.com"
COMMENT_RULES = {'TAGS': 0, 'TEXT': ""}
LIKE_NEED = True
DRIVER_PATH = '/Applications/chromedriver'


import cookie_helper
from helper import *
from pyquery import PyQuery as pq
from selenium import webdriver
from selenium.common.exceptions import *

def is_legal_comment_content(content, tag=0, text=""):
    try:
        content.text().lower().index(text.lower())
    except:
        return False
    tagged = len(content('.profileLink'))
    return tagged>=tag


chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("prefs", {"profile.managed_default_content_settings.images": 2})
driver = webdriver.Chrome(DRIVER_PATH, options=chrome_options)

command = get_input("select an option by typing number\n1: login manually\n2: login by cookie file\n", ['1', '2'])
driver.implicitly_wait(500)
driver.get(URL_HOME)

if command=='1':
    tmp = get_input("press any key after you logined.  ")
    if get_input("do you want to save login session as a cookie file? [y/n]  ", ['y', 'Y', 'n', 'N']) in ['y','Y']:
        cookie_helper.save(driver)
    
elif command=='2':
    cookie_helper.load(driver)

driver.get(URL_POST)

posts = driver.find_element_by_css_selector('#content_container #pagelet_group_mall')
post = posts.find_element_by_css_selector('._4-u2._4-u8')
post_wrapper = post.find_element_by_css_selector('.userContentWrapper')
content = post_wrapper.find_element_by_css_selector('div._1dwg._1w_m._q7o')
comment_like_share_wrapper = post_wrapper.find_element_by_css_selector('form.commentable_item')

def get_legal_comment_list():
    tags_need = COMMENT_RULES['TAGS']
    text_need = COMMENT_RULES['TEXT']
    comment_wrapper = comment_like_share_wrapper.find_element_by_css_selector('.UFIList')

    while True:
        if pq(comment_wrapper.get_attribute('innerHTML'))('.UFIPagerLink'):
            more_link = comment_wrapper.find_element_by_css_selector('.UFIPagerLink')
            more_link.click()
            try:
                while pq(more_link.get_attribute('innerHTML'))('span[role="progressbar"]'):
                    pass
            except StaleElementReferenceException:
                pass
        else:
            break

    comment_pq = pq(comment_wrapper.get_attribute('innerHTML'))
    comments = comment_pq('.UFIComment:not(.UFIPartialBorder)')
    print(f'total {len(comments)} comments')

    legal_comment_list = []
    for com in comments.items():
        comment_content = com('.UFICommentBody')
        if is_legal_comment_content(comment_content, tag=tags_need, text=text_need):
            comment_text = comment_content.text()
            actor_ele = com('.UFICommentActorName')
            actor_url = get_clean_url(actor_ele.attr('href'))
            actor_name = actor_ele.text()
            legal_comment_list.append((actor_name, actor_url, comment_text))
        else:
            print(comment_content.text())
    return legal_comment_list

def get_legal_like_list():
    like_share_wrapper = comment_like_share_wrapper.find_element_by_css_selector('._37uu ._3399')
    like_share_pq = pq(like_share_wrapper.get_attribute('innerHTML'))
    like_link = like_share_pq('._1vaq a._2x4v').attr('href')
    driver.get("https://www.facebook.com"+like_link)

    motion_wrapper_list = driver.find_element_by_css_selector('._4bl7._4k2o')

    while pq(motion_wrapper_list.get_attribute('innerHTML'))('.uiMorePagerPrimary'):
        try:
            more_link = motion_wrapper_list.find_element_by_css_selector('.uiMorePagerPrimary')
            more_link.click()
            time.sleep(1)
        except WebDriverException:
            pass

    legal_motion_list = []
    motion_wrapper_pq = pq(motion_wrapper_list.get_attribute('innerHTML'))
    motion_actor_list = motion_wrapper_pq('.fwb.fcb a')
    for actor in motion_actor_list.items():
        actor_url = get_clean_url(actor.attr('href'))
        actor_name = actor.text()
        legal_motion_list.append((actor_name, actor_url))
    
    print(f"total {len(legal_motion_list)} likes")
    return legal_motion_list


legal_list = get_legal_comment_list()
if LIKE_NEED:
    legal_like_list = get_legal_like_list()

    legal_list_new = []
    for comment in legal_list:
        for like in legal_like_list:
            if comment[1] == like[1]:
                legal_list_new.append(comment)
                legal_like_list.remove(like)

    legal_list = legal_list_new

print(len(legal_list))
print(legal_list)