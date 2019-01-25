from os import environ
from bs4 import BeautifulSoup as soup
import datetime as dt
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException

event_list = []
delay = 3 #seconds
user = environ['USER_ID']
pwd = environ['USER_PASS']
nusync_url = "https://vafs.nus.edu.sg/adfs/ls/?SAMLRequest=fZFLT8MwEIT%2FSuR74jwKba0mUmgPVCoQkcCBC3LcTWMpsYPXKfTfkzY8ioR68MWenZn9vEDeNh1Le1urR3jrAa3z0TYK2ekhJr1RTHOUyBRvAZkVLE%2FvNiz0fNYZbbXQDXFSRDBWarXUCvsWTA5mLwU8PW5iUlvbIaNUmx0elPCEbmley7LUDdjaQ9T0aBnS7CEviLMaOkjFj26%2Fs3teoad69GDbe7ijfFshbZASZ72KyasAUVUzH8rpNczLSEyjSQDzyWwyHD%2BY%2B4MMsYe1QsuVjUk4XLp%2B4IZREcxYFLGr4IU42dc%2BN1JtpdpdXr4cRchuiyJzx%2BrPYPBUexCQZHFEyE7B5gzqZVv%2BTZIk%2F3HDH24udgt6ljDGdex%2BsFyvMt1IcXDSptHvSwPcQkwCQpNx5O%2BHJ58%3D&RelayState=https%3A%2F%2Forgsync.com%2Fshib%2Fnational-university-of-singapore"
#nusync_cal_url = "https://orgsync.com/134631/forms/208857" --can skip this and go straight to calander frame
nusync_cal_frame = "https://calendar.google.com/calendar/embed?showPrint=0&shbs=0&showTz=0&height=600&wkst=1&bgcolor=%23FFFFFF&src=eusoffcalendar%40gmail.com&co%231B887A&ctz=Asia%2FSingapore"

driver = webdriver.Chrome()
driver.get(nusync_url)

#Login to NUSync
elem = driver.find_element_by_id('userNameInput')
elem.send_keys(user)
elem = driver.find_element_by_id('passwordInput')
elem.send_keys(pwd)
elem.send_keys(Keys.RETURN)

#Go to Calendar
driver.get(nusync_cal_frame)
driver.find_element_by_id("tab-controller-container-agenda").click() #Agenda view for easier scraping

#Scraping process using bs4
try:
	check = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.ID, 'eventContainer1'))) #webdriver will wait for a page to load by default but not for loading inside frames or for ajax requests, hence waiting is used explicitly using expected_conditions for the page to load
	data = driver.find_element_by_id("eventContainer1").get_attribute('innerHTML') # -- find the next 45 event summaries
	data_soup = soup(data, "lxml")
	event_list = data_soup.findAll("div", {"class": "event-summary"})
	if dt.date.today().strftime("%d %B") in event_list[0].span["alt"]: # check that the first event in the list takes place today, if not, return no activities today.
		for event in event_list:
			event_time = event.span["alt"] #get datetime + duration
			event_info = event.div.text #get venue + activity
			print(event_time, event_info)
	else:
		print("There are no activities today!")

except TimeoutException:
	print('Loading is taking too much time.')

