from selenium import webdriver
import random
from selenium.webdriver.common.proxy import Proxy, ProxyType
from common import get_public_ip

# Checking Public IP before using Proxy
print("Ip Address Before : ",get_public_ip())

# Your Luminati User Name
username = 'Your User Name'

# Your Luminati Password
password = 'Your Password'

# Default Luminati Port
port = 22225

# Generating a Random Session Id
session_id = random.random()

# Creating Proxy Url
super_proxy_url = ('http://%s-session-%s:%s@zproxy.luminati.io:%d' %(username, session_id, password, port))
print("super_proxy_url : ",super_proxy_url)

# Creating Selenium Proxy Object
proxy = Proxy({
    'proxyType': ProxyType.MANUAL,
    'httpProxy': super_proxy_url,
    'ftpProxy': super_proxy_url,
    'sslProxy': super_proxy_url,
    'noProxy': ''  # set this value as desired
})

print(proxy)

browser = input("Please Enter your browser name i.e Chrome/Firefox etc")
driver=None

# Checking Browser type
if browser == "Chrome":
    # Creating Chrome Options
    options = webdriver.ChromeOptions()

    # Adding Proxy to Chrome Arguments
    options.add_argument('--proxy-server=%s' % proxy)

    # Initialising Driver
    driver = webdriver.Chrome(
        executable_path='Your Chromedriver Executable Path',
        chrome_options=options)

elif browser=="Firefox":
    driver = webdriver.Firefox(executable_path="Your Geckodriver Executable path",
                               proxy=proxy)

# Checking Browsers IP Address
driver.get('https://www.whatismyip.org/')
print("IP Address After " ,driver.find_element_by_xpath('//*[@id="collapse-menu"]/h3/a').text)
driver.quit()
