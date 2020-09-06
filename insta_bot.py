#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import time
import random
import re
from selenium import webdriver
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException



username = input('Enter Instagram username/email: ')
password = input('Enter Instagram password: ')

hashtag = []
with open('hashtags.txt', 'r') as filereader:
    hashtag_list = [random_hashtag.rstrip() for random_hashtag in filereader.readlines()]
    tag = random.choice(hashtag_list)
    print('Current Hashtag : ' + tag)


profile = webdriver.FirefoxProfile()
driver = webdriver.Firefox(firefox_profile=profile)
driver.set_window_size(700, 900)


"""login in to Instagram"""
def login():
    driver.get("https://www.instagram.com/")
    time.sleep(10)
    login_button = driver.find_element_by_xpath("/html/body/div[1]/section/main/article/div[2]/div[1]/div/form/div/div[3]")
    login_button.click()
    time.sleep(10)
    username_field = driver.find_element_by_xpath("//input[@name='username']")
    username_field.clear()
    username_field.send_keys(username)
    password_field = driver.find_element_by_xpath("//input[@name='password']")
    password_field.clear()
    password_field.send_keys(password)
    password_field.send_keys(Keys.RETURN)
    time.sleep(10)


'''Like Photo'''
def like_photo():
    driver.get("https://www.instagram.com/explore/tags/" + tag + "/")
    time.sleep(10)

    # gathering photos
    pic_hrefs = []
    for i in range(1, 7):
        try:
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)
            # get tags
            hrefs_in_view = driver.find_elements_by_tag_name('a')
            # finding relevant hrefs
            hrefs_in_view = [elem.get_attribute('href') for elem in hrefs_in_view
                             if '.com/p/' in elem.get_attribute('href')]
            # building list of unique photos
            [pic_hrefs.append(href) for href in hrefs_in_view if href not in pic_hrefs]
            # print("Check: pic href length " + str(len(pic_hrefs)))
        except Exception:
            continue

    # Liking photos
    unique_photos = len(pic_hrefs)
    print('Pictures to Like: ' + str(unique_photos))
    for pic_href in pic_hrefs:
        driver.get(pic_href)
        time.sleep(2)
        #driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        try:
            time.sleep(random.randint(28, 48))
            like_button = driver.find_element_by_xpath('//*[@id="react-root"]/section/main/div/div[1]/article/div[3]/section[1]/span[1]/button')
            like_button.click()
            for second in reversed(range(0, random.randint(38, 58))):
                print_same_line("#" + tag + ': unique photos left: ' + str(unique_photos)
                                + " | Sleeping " + str(second))
                time.sleep(1)
        except Exception as e:
            time.sleep(2)
        unique_photos -= 1


def main():
    login()
    like_photo()
    time.sleep(10)
    driver.quit()




if __name__ == '__main__':
    main()
