import urllib
import urllib.request
from bs4 import BeautifulSoup
from urllib.parse import urlsplit
import os
import random
import requests
import re
import eel
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ExifTags
import time
import wget
from selenium import webdriver
import chromedriver_autoinstaller
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from creds import *

chromedriver_autoinstaller.install()

eel.init('fypApp')

SAVE_FOLDER = '.\images'

if not os.path.exists(SAVE_FOLDER): #Creates a directory for images to be saved if directory already doesn not exist
    os.mkdir(SAVE_FOLDER)


#Static Scraper

@eel.expose
def make_soup(url, headers):                             
    r = requests.get(url = url, headers = headers)
    soupdata = BeautifulSoup(r.text, 'html.parser')   #Function to pass a request to the inputted URL

    counter = 0

    for img in soupdata.findAll('img'):
        base_url = "{0.scheme}://{0.netloc}".format(urlsplit(url)) #Gets the base name of a url to create full path to the image
        temp = img.get('src')
        image_name = str(counter)
        counter+=1
        print(img)
        
        if temp[:1]=='/':
            image = base_url + temp
        else:
            image = temp

        full_name = SAVE_FOLDER + '/' + image_name + '.jpg'
        
        with open(full_name, 'wb') as f:  #Writes the images to the specified files path
            im = requests.get(image)
            f.write(im.content)
            print ('Writing: ', full_name)
    eel.successMessage()


#Instagram Scraper

@eel.expose
def InstagramScraper(url, keyword):
    if keyword == '':
        keyword = '#londonlife'

    driver = webdriver.Chrome()

    driver.get(url)
    username= WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='username']")))
    password= WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='password']")))

    Accept = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[text()='Accept']"))).click()

    username.clear()
    password.clear()
    username.send_keys(InstagramUsername)
    password.send_keys(InstagramPassword)

    log_in = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']"))).click()

    Not_Now = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[text()='Not Now']"))).click()
    Not_Now2 = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[text()='Not Now']"))).click()

    time.sleep(3)
    
    searchbox= WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//input[@placeholder='Search']")))
    searchbox.clear()
    searchbox.send_keys(keyword)

    time.sleep(2)

    searchbox.send_keys(Keys.ENTER)
    time.sleep(1)
    searchbox.send_keys(Keys.ENTER)

    driver.execute_script("window.scrollTo(0,4000);")

    time.sleep(5)
    images = driver.find_elements_by_tag_name('img')
    images= [image.get_attribute('src') for image in images]

    counter = 0

    for image in images:
        save_as = SAVE_FOLDER + '/' + keyword + str(counter) + '.jpg'
        wget.download(image, save_as)
        counter+= 1
    driver.close()
    eel.successMessage()


#Behance Scraper

@eel.expose
def BehanceScraper(url, keyword):
    if keyword == '':
        keyword = 'Behance'

    driver = webdriver.Chrome()
    driver.get(url)
    driver.maximize_window()

    time.sleep(5)

    Search = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="site-content"]/div/header/div[1]/div/div/form/label/input')))

    time.sleep(5)

    Search.send_keys('Harvind Sokhal')

    time.sleep(5)

    Search.send_keys(Keys.ENTER)

    time.sleep(3)

    Project = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="site-content"]/div/div[1]/div/div[1]/div/div/ul/li/div'))).click()

    time.sleep(5)

    driver.execute_script("window.scrollTo(0,4000);")

    time.sleep(2)

    images = driver.find_elements_by_tag_name('img')
    images= [image.get_attribute('src') for image in images]
    counter = 0

    for image in images:
        save_as = SAVE_FOLDER + '/' + keyword + str(counter) + '.jpg'
        wget.download(image, save_as)
        counter+= 1
    driver.close()
    eel.successMessage()


#Pinterest Scraper

@eel.expose
def PinterestScraper(url, keyword):
    if keyword == '':
        keyword = '@harvind_sokhal'
    driver = webdriver.Chrome()
    driver.get(url)

    time.sleep(3)
    LogIn = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/div[1]/div/div/div/div[1]/div[1]/div[2]/div[2]/button'))).click()
    username= WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="email"]')))
    password= WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='password']")))

    username.clear()
    password.clear()
    username.send_keys(PinterestUsername)
    password.send_keys(PineterestPassword)

    log_in = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']"))).click()

    time.sleep(5)

    searchbox= WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="searchBoxContainer"]/div/div/div[2]/input')))
    searchbox.clear()
    
    searchbox.send_keys(keyword)

    time.sleep(5)

    searchbox.send_keys(Keys.ENTER)
    time.sleep(1)
    searchbox.send_keys(Keys.ENTER)

    profile = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="HeaderContent"]/div/div/div/div[2]/div/div/div/div[6]/div[4]'))).click()

    time.sleep(10)

    targetimages = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="__PWS_ROOT__"]/div[1]/div[2]/div/div/div/div[3]/div/div[1]/div/div/div/div/div[1]/a/div/div[1]'))).click()


    driver.execute_script("window.scrollTo(0,4000);")

    time.sleep(5)

    images = driver.find_elements_by_tag_name('img')
    images= [image.get_attribute('src') for image in images]

    counter = 0

    for image in images:
        save_as = SAVE_FOLDER + '/' + keyword + str(counter) + '.jpg'
        wget.download(image, save_as)
        counter+= 1
    driver.close()
    eel.successMessage()

#Flickr Scraper

def flickerscraper(keyword, imagecount, driver):
    
    counter = 0
    imagecounter = 0
    
    while imagecounter < imagecount:
        finddownload = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/div/div[2]/div/div[5]/div[3]'))).click()
        time.sleep(2)
        imagelinks = driver.find_element_by_xpath('//li[@class="Original"]//a')
        image = imagelinks.get_attribute('href')
        save_as = SAVE_FOLDER + '/' + keyword + str(counter) + '.jpg'
        wget.download(image, save_as)
        time.sleep(5)
        background = driver.find_element_by_xpath('//div[@class="fluid-droparound-overlay  transparent "]')
        actiontwo = webdriver.common.action_chains.ActionChains(driver)
        actiontwo.move_to_element_with_offset(background, 5, 5)
        actiontwo.click()
        actiontwo.perform()
        time.sleep(5)
        nextimage = driver.find_element_by_xpath('//a[@class="navigate-target navigate-next"]')
        action = webdriver.common.action_chains.ActionChains(driver)
        action.move_to_element_with_offset(nextimage, 5, 5)
        action.click()
        action.perform()
        counter+= 1
        imagecounter+=1
    
    time.sleep(7)
    previmage = driver.find_element_by_xpath('//a[@class="navigate-target navigate-prev"]')
    action = webdriver.common.action_chains.ActionChains(driver)
    action.move_to_element_with_offset(previmage, 5, 5)
    action.click()
    action.perform()
    time.sleep(2)
    nextimage = driver.find_element_by_xpath('//a[@class="navigate-target navigate-next"]')
    action = webdriver.common.action_chains.ActionChains(driver)
    action.move_to_element_with_offset(nextimage, 5, 5)
    action.click()
    action.perform()
    time.sleep(2)
    finddownload = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/div/div[2]/div/div[5]/div[3]'))).click()
    time.sleep(2)
    imagelinks = driver.find_element_by_xpath('//li[@class="Original"]//a')
    image = imagelinks.get_attribute('href')
    save_as = SAVE_FOLDER + '/' + keyword + str(counter) + '.jpg'
    wget.download(image, save_as)

    driver.close()
    eel.successMessage()


@eel.expose
def getToFlickr(url, keyword):
    if keyword == '':
        keyword = 'Harvind Sokhal'

    driver = webdriver.Chrome()
    driver.get(url)
    driver.maximize_window()
    
    signin = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/div/div[1]/div/div[3]/div/ul[2]/li[2]/a'))).click()

    username = driver.find_element_by_id('login-email')

    username.send_keys(FlickrUsername)
    time.sleep(2)
    username.send_keys(Keys.ENTER)

    password = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, 'login-password')))
    password.send_keys(FlickrPassword)
    time.sleep(2)
    password.send_keys(Keys.ENTER)
    
    driver.implicitly_wait(10)
    time.sleep(5)

    cookiesForm = WebDriverWait(driver,10).until(EC.frame_to_be_available_and_switch_to_it((By.XPATH,'//iframe[@title="TrustArc Cookie Consent Manager"]')))
    accpetButton = WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.XPATH,"//a[@class='acceptAll']"))).click()
    
    time.sleep(2)

    Searchbox = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="search-field"]')))

    time.sleep(2)

    Searchbox.send_keys(keyword)

    time.sleep(2)

    Searchbox = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/div/div[1]/div/div[3]/div/ul[2]/li[1]/div/div/ul/li[2]/div'))).click()

    time.sleep(2)

    fullProfile = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/div/div[3]/div/div[2]/div/div/div[1]/a'))).click()
    imagecount = driver.find_element_by_xpath('//p[@class="metadata-item photo-count"]').text
    finalcount = int(imagecount[0]) - 1
    print(finalcount)

    time.sleep(2)

    imageone = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/div/div[4]/div[2]/div[2]/div[1]'))).click()
    

    flickerscraper(keyword, finalcount, driver)
        
def get_decimal_from_dms(value, ref):
    d = value[0]
    m = value[1]
    s = value[2]

    if ref in ['S', 'W']:
        d = -d
        m = -m
        s = -s

    return d + (m / 60.0) + (s / 3600.0)

def get_dateTime(image):
    pil_exif = Image.open(image)
    if not pil_exif:
        raise ValueError("No EXIF metadata found")

    exif = {ExifTags.TAGS[k]: v for k, v in pil_exif._getexif().items() if k in ExifTags.TAGS}

    Date = exif['DateTimeOriginal'][0:10]
    Date = Date.replace(':', '/')
    Time = exif['DateTimeOriginal'][11:20]
    
    eel.setImageDate('Date taken: '+Date)
    eel.setImageTime('Time taken: '+Time)
    
    

def get_cords(dict):
    
    lat = get_decimal_from_dms(dict['GPSLatitude'], dict['GPSLatitudeRef'])
    long = get_decimal_from_dms(dict['GPSLongitude'], dict['GPSLongitudeRef'])
    
    eel.setImageLocation('Location of image: '+str(lat)+ ', ' + str(long))
    
   
@eel.expose
def get_exif(image):

    pil_exif = Image.open(image)
    if not pil_exif:
        raise ValueError("No EXIF metadata found")

    exif = {ExifTags.TAGS[k]: v for k, v in pil_exif._getexif().items() if k in ExifTags.TAGS}
    
    gps_all = {}
    for key in exif['GPSInfo'].keys():
        decoded_value = ExifTags.GPSTAGS.get(key)
        gps_all[decoded_value] = exif['GPSInfo'][key]

    get_cords(gps_all) 
    return(gps_all)

@eel.expose
def selectImage():
    root = tk.Tk()
    filename = filedialog.askopenfilename(initialdir='./images')
    eel.setImageName('Image selected: '+filename)
    if filename == '':
        pass
        root.withdraw()
    dateTime = get_dateTime(filename)
    exif = get_exif(filename)
    root.withdraw()


eel.start('index.html', size=(800, 600))