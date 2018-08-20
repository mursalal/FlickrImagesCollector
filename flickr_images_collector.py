from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from requests import get
import os
import time

binary = FirefoxBinary('/home/user_name/firefox/firefox')
driver = webdriver.Firefox(firefox_binary=binary)
#webdriver.DesiredCapabilities.PHANTOMJS['phantomjs.page.customHeaders.Accept-Language'] = 'en-EN'
#driver = webdriver.PhantomJS()
driver.get("https://www.flickr.com/signin")
driver.find_element_by_id('login-username').send_keys('login')
driver.find_element_by_id('login-signin').click()
driver.find_element_by_id('login-passwd').send_keys('password')
driver.find_element_by_id('login-signin').click()
print "sleeping"
time.sleep(5)


def collect_links(keyword):
    driver.get("https://www.flickr.com/search/?text=" + keyword + "&view_all=1")
    links = set()
    #sf = driver.find_element_by_id("search-field")
    #sf.send_keys(keyword)
    #sf.send_keys(Keys.RETURN)
    #driver.find_element_by_class_name('view-more-link').click()
    #driver.find_element_by_class_name('thumbs').click()

    pictures = driver.find_elements_by_class_name("overlay")
    photos_div = driver.find_element_by_id("search-unified-content")
    len_of_pics = len(pictures)
    count = 0

    while len(pictures) < 5000:
        print len(pictures)
        len_of_pics = len(pictures)
        if count == 100:
            break
        photos_div.send_keys(Keys.END)
        pictures = driver.find_elements_by_class_name("overlay")
        try:
            driver.find_element_by_class_name("infinite-scroll-load-more").click()
        except:
            pass
        if len_of_pics == len(pictures):
            count += 1
        else:
            for k in range(len_of_pics, len(pictures)):
                try:
                    links.add(pictures[k].get_attribute("href") + 'sizes/l' + '\n')
                except:
                    break

    f = open(keyword + '.txt', 'w')
    for i in links:
        f.write(i)


def download_photos(keyword):
    if os.path.isdir(keyword) is False:
        os.mkdir(keyword)
    srcs = open(keyword + '.txt', 'r').read().split()
    count = 0
    for index, s in enumerate(srcs):
        if count < 0:
            count += 1
            continue
        print index
        driver.get(s)
        retries = 0
        while True:
            retries += 1
            try:
                el = driver.find_element_by_id('allsizes-photo')
            except:
                if retries == 5:
                    break
                continue
            break
        if retries == 5:
            continue
        if os.path.isfile(keyword + '/' + keyword + '_' + str(index) + '.jpg'):
            continue
        with open(keyword + '/' + keyword + '_' + str(index) + '.jpg', "wb") as f:
            response = get(el.find_element_by_tag_name('img').get_attribute("src"))
            f.write(response.content)

keywords = ['google', 'bmw', 'citroen', 'chanel', 'lacoste']

for keyword in keywords:
    collect_links(keyword)
    download_photos(keyword)


