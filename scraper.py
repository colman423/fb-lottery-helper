URL_HOME = "http://www.facebook.com"
DRIVER_PATH = '/Applications/chromedriver'


import cookie_helper
from helper import *
from pyquery import PyQuery as pq
from selenium import webdriver
from selenium.common.exceptions import *

class Scraper:
    def __init__(self, url_post, comment_rules, like_need):
        self.URL_POST = url_post
        self.COMMENT_RULES = comment_rules
        self.LIKE_NEED = like_need

    def run(self):
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_experimental_option("prefs", {"profile.managed_default_content_settings.images": 2})
        self.driver = webdriver.Chrome(DRIVER_PATH, options=chrome_options)

        # command = get_input("select an option by typing number\n1: login manually\n2: login by cookie file\n", ['1', '2'])
        # self.driver.implicitly_wait(500)
        # self.driver.get(URL_HOME)

        # if command=='1':
        #     tmp = get_input("press any key after you logined.  ")
        #     if get_input("do you want to save login session as a cookie file? [y/n]  ", ['y', 'Y', 'n', 'N']) in ['y','Y']:
        #         cookie_helper.save(self.driver)
            
        # elif command=='2':
        #     cookie_helper.load(self.driver)
        self.driver.implicitly_wait(500)
        self.driver.get(URL_HOME)
        cookie_helper.load(self.driver)
        try:
            self.driver.get(self.URL_POST)
        except WebDriverException as e:
            error_msg = e.msg
            if "Cannot navigate to invalid URL" in error_msg:
                raise Exception("INVALID_FACEBOOK_URL")
            # print(e.keys())

        posts = self.driver.find_element_by_css_selector('#content_container #pagelet_group_mall')
        post = posts.find_element_by_css_selector('._4-u2._4-u8')
        post_wrapper = post.find_element_by_css_selector('.userContentWrapper')
        content = post_wrapper.find_element_by_css_selector('div._1dwg._1w_m._q7o')
        comment_like_share_wrapper = post_wrapper.find_element_by_css_selector('form.commentable_item')

        legal_list = self.get_legal_comment_list(comment_like_share_wrapper)

        if self.LIKE_NEED:
            legal_like_list = self.get_legal_like_list(comment_like_share_wrapper)

            legal_list_new = []
            for comment in legal_list:
                for like in legal_like_list:
                    if comment[1] == like[1]:
                        legal_list_new.append(comment)
                        legal_like_list.remove(like)
                        break

            legal_list = legal_list_new

        self.driver.quit()
        print(len(legal_list))
        print(legal_list)
        return legal_list


  
    def get_legal_comment_list(self, comment_like_share_wrapper):
        print("get_legal_comment_list", comment_like_share_wrapper)
        tags_need = self.COMMENT_RULES['TAGS']
        text_need = self.COMMENT_RULES['TEXT']
        comment_wrapper = comment_like_share_wrapper.find_element_by_css_selector('._3w53')
        # print(comment_wrapper)

        while True:
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
        print(f'total {len(comments)} comments')

        legal_comment_list = []
        for com in comments.items():
            comment_content = com('._3l3x')
            if is_legal_comment_content(comment_content, tag=tags_need, text=text_need):
                print(comment_content.text(), "LEGAL!!!")
                comment_text = comment_content.text()
                actor_ele = com('._6qw4')
                actor_url = get_clean_url(actor_ele.attr('href'))
                actor_name = actor_ele.text()
                legal_comment_list.append((actor_name, actor_url, comment_text))
            else:
                print(comment_content.text())
        return legal_comment_list

    def get_legal_like_list(self, comment_like_share_wrapper):
        print("get_legal_like_list", comment_like_share_wrapper)
        like_share_wrapper = comment_like_share_wrapper.find_element_by_css_selector('._3vum')
        like_share_pq = pq(like_share_wrapper.get_attribute('innerHTML'))
        like_link = like_share_pq('._66lg a').attr('href')
        self.driver.get("https://www.facebook.com"+like_link)

        motion_wrapper_list = self.driver.find_element_by_css_selector('._4bl7._4k2o')

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
        print(legal_motion_list)
        return legal_motion_list


def is_legal_comment_content(content, tag=0, text=""):
    try:
        if not content.text():
            raise ValueError
        content.text().lower().index(text.lower())
    except:
        return False
    tagged = len(content('a'))
    return tagged>=tag
