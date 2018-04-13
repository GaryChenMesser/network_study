# fbfried.py
#
# This is a  crawler implemented by selenium, which can 
# scrape a given user's friend list and traverse outward
# to construct the friendship network. The network size
# can be tuned through the steps outward from the seed
# and the filtering conditions.

# Gary Chen
# 2018/04/13

from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import sys
from graph_tool.all import *
from collections import deque


class FacebookCrawler:
    LOGIN_URL = 'https://www.facebook.com/login.php?login_attempt=1&lwv=111'
    NTU = ['Taiwan University', '灣大學']
    EE = ['Electrical Engineering', 'Electrical engineering', 'electrical engineering', '電機']

    def __init__(self, login, password):
        chrome_options = webdriver.ChromeOptions()
        #prefs = {"download.default_directory" : "../../..//Downloads"}
        prefs = {"profile.default_content_setting_values.notifications": 2}
        chrome_options.add_experimental_option("prefs", prefs)
        chrome_driver = "/usr/lib/chromium-browser/chromedriver"

        self.driver = webdriver.Chrome(executable_path=chrome_driver, chrome_options=chrome_options)
        self.wait = WebDriverWait(self.driver, 10)

        self.login(login, password)

    def login(self, login, password):
        self.driver.get(self.LOGIN_URL)

        # wait for the login page to load
        self.wait.until(EC.visibility_of_element_located((By.ID, "email")))

        self.driver.find_element_by_id('email').send_keys(login)
        self.driver.find_element_by_id('pass').send_keys(password)
        self.driver.find_element_by_id('loginbutton').click()
        # wait for the main page to load
        self.wait.until(EC.visibility_of_element_located((By.ID, "userNav")))
        self.driver.find_element_by_id('userNav').click()
    
    def check_user(self):
        # navigate to "about" page
        self.wait.until(EC.visibility_of_element_located((By.XPATH, '//a[@data-tab-key="about"]')))
        self.driver.find_element_by_xpath('//a[@data-tab-key="about"]').click()
        
        # check whether this user is in NTUEE.
        self.wait.until(EC.visibility_of_element_located((By.XPATH, '//div[@class="_c24 _50f4"]/a')))
        about = self.driver.find_elements_by_xpath('//div[@class="_c24 _50f4"]/a')
        
        flag = 0
        
        for item in about:
            flag = 0
            for phrase in NTU:
                if phrase in item.text:
                    flag += 1
                    break
            
            for phrase in EE:
                if phrase in item.text:
                    flag += 1
                    break
            
            if flag == 2:
                return True
        
        return False
    
    def get_ref(self):
        try:
            return self.driver.find_element_by_xpath('//a[@class="_2nlw"]').get_attribute('href')
        except:
            print('Can only call get_ref in profile!')
    
    def get_user(self, href):
        self.driver.get(href)

    def _get_friends_list(self):
        #return self.driver.find_elements_by_css_selector(".friendBrowserNameTitle > a")
        return self.driver.find_elements_by_xpath('//div[@class="uiProfileBlockContent"]/div/div[2]/div/a')

    def get_friends(self):
        # navigate to "friends" page
        self.wait.until(EC.visibility_of_element_located((By.XPATH, '//a[@data-tab-key="friends"]')))
        self.driver.find_element_by_xpath('//a[@data-tab-key="friends"]').click()
        
        # click on all friends tab
        #self.wait.until(EC.visibility_of_element_located((By.XPATH, '//a[@name="ALL friends"]')))
        #self.driver.find_element_by_xpath('//a[@name="ALL friends"]')
        
        # wait for first friend
        self.wait.until(EC.visibility_of_element_located((By.XPATH, '//div[@class="uiProfileBlockContent"]/div/div[2]/div/a')))
        
        # continuous scroll until no more new friends loaded
        num_of_loaded_friends = len(self._get_friends_list())
        while True:
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            try:
                self.wait.until(lambda driver: len(self._get_friends_list()) > num_of_loaded_friends)
                num_of_loaded_friends = len(self._get_friends_list())
            except TimeoutException:
                break  # no more friends loaded

        return [friend.get_attribute('href') for friend in self._get_friends_list()]

class FriendGraph:
    G = Graph(directed=False)
    v_href = G.new_vertex_property('string') # record href
    v_visited = G.new_vertex_property('bool') # record visited or not
    v_deleted = G.new_vertex_property('bool') # record deleted or not
    
    def __init__(self, ref):
        index = self.G.add_vertex()
        self.v_href[index] = ref
        self.v_visited[index] = False
        self.v_deleted[index] = False
        self.cursor = 0
        self.href_dict = {v_href[index]: index}
    
    def check_visited(self, index):
        if index >= len(self.v_visited):
            print("index out of range\n")
            return False
        return v_visited[index]
        
    def check_deleted(self, index):
        if index >= len(self.v_deleted):
            print("index out of range\n")
            return False
        return v_deleted[index]
    
    def get_index(self, ref):
        if ref in self.href_dict.keys():
            return self.href_dict[ref]
        
        print("Unknown key\n")
        return -1
    
    def add_vertex(self, ref):
        index = self.G.add_vertex()
        self.v_href[index] = ref
        self.v_visited[index] = False
        self.v_deleted[index] = False
        self.href_dict = {v_href[index]: index}
    
    def visit(sef, ref):
        self.v_visited[self.href_dict[ref]] = True
    
    def delete(self, ref):
        self.v_deleted[self.href_dict[ref]] = True
    


if __name__ == '__main__':
    crawler = FacebookCrawler(login = sys.argv[1], password = sys.argv[2] + ' ' + sys.argv[3])
    last_deque = deque()
    graph = FriendGraph(crawler.get_ref())
    
    
    try:
        for step in range(sys.argv[4]):
            
        
        
            if len(old_deque) == 0:
                this_deque = deque(crawler.get_friends())
            
            while len(old_deque) > 0:
                user = old_pop()
                crawler.get_user(user)
                graph.visit(user)
                
                if not crawler.check_user():
                    graph.delete(user)
                    continue
                
                for friend in crawler.get_friends():
                    this_deque.append(friend)
            
            #old_deque = this_deque
            
        
        
    except:
        
