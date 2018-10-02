from lxml import html
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
import re 
import vk
import requests
from itertools import chain




def page_is_loaded(driver):
	return driver.find_element_by_tag_name('body') != None

vk_login = # your vk login here
vk_pass = # your vk password here
username = # your login here
password = # your password here
pass_to_chromedriver = #pass on your computer to chromedriver tool
access_token = #your access_token
user_id = #reciever vk id



# logging into site 
driver = webdriver.Chrome(pass_to_chromedriver)#pass to chromedriver
driver.get("https://track.mail.ru/pages/index/#")
wait = WebDriverWait(driver,10)
wait.until(page_is_loaded)

driver.find_element_by_xpath("/html/body/div[1]/nav[1]/ul/li[1]/a/span").click()
driver.implicitly_wait(4)
driver.find_element_by_xpath("//*[@id='popup-login-form']/div[2]/p[1]/input").send_keys(username)
driver.find_element_by_xpath("//*[@id='popup-login-form']/div[2]/p[2]/input").send_keys(password)
driver.find_element_by_xpath("//*[@id='popup-login-form-submit']").click()
driver.implicitly_wait(10)

#parsing timetable

review = []
for i in range(1,8):
	timetab = driver.find_element_by_xpath("//*[@id='container']/div[1]/div[1]/div[{}]".format(i))
	tmp_data = timetab.get_attribute('innerHTML')
	data_date =  re.findall('(?s)<div class="schedule-date__value">([^<]*)</div>',tmp_data)[0]
	review.append(data_date)
	data_no = re.findall('(?s)<div class="no-items">([^<]*)</div>',tmp_data)
	if data_no != []:
		review.append(data_no[0])
	else:
		data_time =  re.findall('(?s)<div class="schedule-item__time">([^<]*)</div>',tmp_data)[0]
		data_name =  re.findall('(?s)<div class="schedule-item__name">([^<]*)</div>',tmp_data)[0].split()
		data_name = data_name[0] + ' ' + data_name[1]
		data_place =  re.findall('(?s)<div class="schedule-item__place">([^<]*)</div>',tmp_data)[0].split()
		data_place = data_place[0] + ' ' + data_place[1]
		review.append(data_time)
		review.append(data_name)
		review.append(data_place)
#completed timetable is in review list

#sending message of timetable to a selected user
for i in range(0,len(review)):
	review[i] += '\n'

final_message = "".join(chain.from_iterable(review))
params = "user_id={}&message={}".format(user_id,final_message);
token = "access_token={}".format(access_token);
method = "messages.send";
req = "https://api.vk.com/method/"+ method +"?"+ params +"&"+ token+"&" + "v=5.85";#final url
send = requests.get(req)
