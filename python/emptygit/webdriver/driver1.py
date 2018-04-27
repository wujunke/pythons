#coding=utf-8


from selenium import webdriver
import time


driver = webdriver.Chrome('/usr/local/bin/chromedriver', )
driver.get("https://www.baidu.com")
print 'Browser will close.1'
driver.find_element_by_id('kw').send_keys(u"18616837957")
print '正在输入密码...'

# driver.find_element_by_xpath('//*[@id="create_account_password"]').click()
#
#
# page = driver.page_source
#
# print page
#
# driver.quit()

