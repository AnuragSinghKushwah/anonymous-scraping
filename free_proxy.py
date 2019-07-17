import requests,re,socket
from common import get_public_ip
from selenium import webdriver
from selenium.webdriver.common.proxy import Proxy, ProxyType
import urllib.request
import urllib.error


def is_bad_proxy(pip):
    "Function to Check if the proxy is working or not"
    try:
        proxy_handler = urllib.request.ProxyHandler({'http': pip})
        opener = urllib.request.build_opener(proxy_handler)
        opener.addheaders = [('User-agent', 'Mozilla/5.0')]
        urllib.request.install_opener(opener)
        req=urllib.request.Request('https://www.google.com')  # change the URL to test here
        print("req : ",req)
        sock=urllib.request.urlopen(req)
    except urllib.error.HTTPError as e:
        print('Error code: ', e.code)
        return e.code
    except Exception as detail:
        print("ERROR:", detail)
        return True
    return False

def get_anonymous_ip():
    "Function to get annonymous ip from Free Proxy "
    url = "https://free-proxy-list.net/"
    # url = "http://spys.one/en/anonymous-proxy-list/"
    resp = requests.get(url).text
    regex = '\d+\.\d+\.\d+\.\d+'
    regex2 = re.compile(r'>(\d+?)\<')
    urls = re.findall(regex, resp)
    ports = re.findall(regex2, resp)
    proxyList = [i + ":" + j for i, j in zip(urls, ports)]
    print("total proxies : ", len(proxyList))

    socket.setdefaulttimeout(120)
    for currentProxy in proxyList:
        if is_bad_proxy(currentProxy):
            print("Bad Proxy %s" % (currentProxy))
        else:
            print("%s is working" % (currentProxy))
            return currentProxy
    return proxyList[0]

def get_proxy_capabilities():
    "Function to add proxy to Browser Capabilities"

    from selenium import webdriver
    from selenium.webdriver.common.proxy import Proxy, ProxyType
    try:
        proxy_url = get_anonymous_ip()
        print("proxy_url : ",proxy_url)
        prox = Proxy()
        prox.proxy_type = ProxyType.MANUAL
        prox.http_proxy = proxy_url
        prox.socks_proxy = proxy_url
        prox.ssl_proxy = proxy_url
        capabilities = webdriver.DesiredCapabilities.CHROME
        prox.add_to_capabilities(capabilities)
        return capabilities
    except Exception as e:
        print("Exception in setting proxy capabilities : ",e)
        pass


# proxy_url = "{}:{}".format(host, str(port))
print("***** ip address before *****",get_public_ip())

# Getting Anonymous Proxy IP Address
proxy_url = get_anonymous_ip()
print("Anonymous Proxy URL : ",proxy_url)

# Adding Proxy to Chrome Capabilities
capabilities = get_proxy_capabilities()

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--headless")
chrome_options.add_argument("no-sandbox")

driver = webdriver.Chrome(
                        executable_path="Your ChromeDriver Executable Path",
                        chrome_options=chrome_options,
                        desired_capabilities=capabilities)

# Checking Driver with Proxy Enabled
driver.get("https://whatismyip.org")
print("new_ip : ",driver.find_element_by_xpath('//*[@id="collapse-menu"]/h3/a').text)
