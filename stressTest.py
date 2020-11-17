# Google Chrome Driver:
# https://sites.google.com/a/chromium.org/chromedriver/downloads

from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import requests
import time
import sys

# Configuring Presets Options for Browser
options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")
options.add_argument("--headless")
options.add_argument("--use-fake-device-for-media-stream")
options.add_argument("--use-fake-ui-for-media-stream")
options.add_argument("--ignore-certificate-errors")
options.add_argument("--ignore-ssl-errors")
options.add_argument('--no-sandbox')
options.add_argument("--use-file-for-fake-video-capture=/root/stressTest/rec_10.y4m")

# Select the number of participants per VideoRoom
#rooms = int(input("Enter the number of room: "))
#ps = int(input("Enter the number of participants by room: "))
#t = int(input("Enter the test time in minutes: "))
rooms = int(sys.argv[1])
ps = int(sys.argv[2])
t = int(sys.argv[3])

t = t * 60
i = 0
n = 1

# Setting up the Chrome Driver
browser = webdriver.Chrome('/root/stressTest/chromedriver', options=options)

# Log starting information 

print('**** Starting Script ****')
print('**** Starting Video Room ****')

# Select option and clicking the register button
i = 0
n = 1
while n <= ps:
    n = n + 1
    r = 1
    while r <= rooms:
        i = i + 1
        r = r + 1
        browser.execute_script("window.open('https://janus-dev.maestroconference.com/videoroomtest.html', "+str(i)+")")
        browser.switch_to.window(browser.window_handles[i])
        time.sleep(3)
        browser.find_element_by_xpath('//h1/button').click()
        time.sleep(2)
        y = 0
        while y == 0:
            try:
                y = 1
                browser.switch_to.window(browser.window_handles[i])
                browser.find_element_by_xpath('//select/option['+str(r)+']').click()
                room_name = browser.find_element_by_xpath('//select/option['+str(r)+']').text
                browser.find_element_by_xpath('//*[@id="username"]').send_keys('AvalogicsTest' + str(i))
                browser.find_element_by_xpath('//*[@id="register"]').click()
            except:
                y = 0
                print("  - Error when selecting option, will try again.")
                time.sleep(10)
        time.sleep(10)
        print('*** AvalogicsTest ' + str(i) + ' Joined in '+ room_name + '***')

time.sleep(t)

# Clicking the STOP button and close tab
while i >= 0:
    try:
        browser.switch_to.window(browser.window_handles[i])
        i = i - 1
        browser.find_element_by_xpath('//h1/button').click()
        time.sleep(5)
        browser.close()
        print('*** Close AvalogicsTest ' + str(i) + ' ***')
    except:
        browser.close()
        print('*** Close ' + str(i) + ' ***')

