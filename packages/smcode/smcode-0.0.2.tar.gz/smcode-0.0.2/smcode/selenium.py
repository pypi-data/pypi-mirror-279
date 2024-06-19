import os
import sys
import shutil
import time
import pyperclip
import random
import requests
import subprocess
import chromedriver_autoinstaller as AutoChrome
from fake_useragent import UserAgent
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.select import Select
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.remote.command import Command
from selenium.webdriver.remote.webelement import WebElement
from selenium.common.exceptions import *
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
import glob


def get_status(driver: WebDriver):
    """
    If the driver can get the title of the page, it's alive, otherwise it's dead
    
    :param driver: The webdriver object
    :type driver: WebDriver
    :return: The status of the driver.
    """
    try:
        driver.title
    except:
        return "Dead"
    else:
        return "Alive"
    
    
def find_testdriver():

    import zipfile

    chrome_ver = AutoChrome.get_chrome_version().split('.')[0]
    zip_link = get_chromedriver_url(AutoChrome.get_chrome_version())

    if zip_link:
        zip_response = requests.get(zip_link)
        with open("chromedriver.zip", "wb") as zip_file:
            zip_file.write(zip_response.content)

        with zipfile.ZipFile("chromedriver.zip", "r") as zip_ref:
            zip_ref.extractall(f"C:\\chromedriver\\{chrome_ver}\\")

        os.remove("chromedriver.zip")
        for directory in glob.glob(f"C:\\chromedriver\\{chrome_ver}\\*"):
            if 'chromedriver' in directory:
                os.rename(directory, f"C:\\chromedriver\\{chrome_ver}\\chromedriver")

        source_path = f"C:\\chromedriver\\{chrome_ver}\\chromedriver\\chromedriver.exe"
        target_path = f"C:\\chromedriver\\{chrome_ver}\\chromedriver.exe"
        shutil.move(source_path, target_path)


def get_chromedriver_url(chromedriver_version, no_ssl=False):

    try:
        from packaging import version
    except:
        subprocess.run(['python', '-m', 'pip', 'install', '--upgrade', 'packaging'])
        from packaging import version

    platform, architecture = AutoChrome.utils.get_platform_architecture()
    if chromedriver_version >= "115":  
        versions_url = "googlechromelabs.github.io/chrome-for-testing/known-good-versions-with-downloads.json"
        versions_url = "http://" + versions_url if no_ssl else "https://" + versions_url
        response = requests.get(versions_url)
        download_version_list = response.json()

        for good_version in download_version_list["versions"]:
            if version.parse(good_version["version"]) > version.parse(chromedriver_version):
                try: download_urls = last_version["downloads"]["chromedriver"]
                except: download_urls = good_version["downloads"]["chromedriver"]
                for url in download_urls:
                    if url["platform"] == platform + architecture:
                        return url['url']
            last_version = good_version
    else:  
        base_url = "chromedriver.storage.googleapis.com/"
        base_url = "http://" + base_url if no_ssl else "https://" + base_url
        return base_url + chromedriver_version + "/chromedriver_" + platform + architecture + ".zip"


def load_driver(chrome_options=None, mode=None, userId=None, port=9222, **kwargs) -> WebDriver:
    """
    It opens a Chrome browser with the specified options
    
    :param chrome_options: This is an instance of the ChromeOptions class. You can pass an existing
    instance of ChromeOptions to this parameter, or you can create a new instance of ChromeOptions
    :param mode: This is the mode you want to use. You can use multiple modes at once
    :param userId: This is the user ID that you want to use. This is used to create a cache folder for
    the user
    :param port: The port number that the Chrome browser will be running on, defaults to 9222 (optional)
    :return: A WebDriver object.
    """

    # userAgent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'
    # userAgentMo = 'Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1'
    # userAgent = UserAgent().random

    valid_mode_lst = [
        'fast',
        'cache',
        'debug',
        'secret',
        'android',
        'ios'
    ]

    ios_agent = ['Mozilla/5.0 (iPhone; CPU iPhone OS 14_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Mobile/15E148 Safari/604.1',
        'Mozilla/5.0 (iPhone; CPU iPhone OS 14_0_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1',
        'Mozilla/5.0 (iPhone; CPU iPhone OS 13_3_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.5 Mobile/15E148 Safari/604.1',
        'Mozilla/5.0 (iPhone; CPU iPhone OS 12_4_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.1.2 Mobile/15E148 Safari/604.1',
        'Mozilla/5.0 (iPhone; CPU iPhone OS 11_0_3 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A432 Safari/604.1']
    
    and_agent = ['Mozilla/5.0 (Linux; Android 11; SM-G973W) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.181 Mobile Safari/537.36',
        'Mozilla/5.0 (Linux; Android 10; SM-G980F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Mobile Safari/537.36',
        'Mozilla/5.0 (Linux; Android 11; SM-G991B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.105 Mobile Safari/537.36',
        'Mozilla/5.0 (Linux; Android 9; SM-N960U1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Mobile Safari/537.36',
        'Mozilla/5.0 (Linux; Android 6.0.1; SAMSUNG SM-G930F Build/MMB29K) AppleWebKit/537.36 (KHTML, like Gecko) SamsungBrowser/4.0 Chrome/44.0.2403.133 Mobile Safari/537.36']

    chrome_ver = AutoChrome.get_chrome_version().split('.')[0]
    chrome_driver_path = 'C:\\chromedriver\\'

    if not os.path.isdir('c:\\chromedriver'):
        os.mkdir('c:\\chromedriver')
    
    if chrome_options is None:
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--window-position=850,0')
    
    chrome_options.add_argument('--disable-features=ChromeWhatsNewUI')
    chrome_options.add_experimental_option("excludeSwitches", ["enable-logging", "test-type"])
    
    if not mode:

        pass

    else:

        if isinstance(mode, str):

            md = mode
            
            if md == 'fast':

                prefs = {"profile.managed_default_content_settings.images": 2}
                chrome_options.add_experimental_option("prefs", prefs)
                
            if md == 'cache':
                
                userDataFolder = 'c:/cache/{}'.format(userId)
                chrome_options.add_argument('--user-data-dir=' + userDataFolder)
                chrome_options.add_argument('--disk-cache-dir=' + userDataFolder)
            
            if md == 'debug':
                import subprocess
                try:
                    subprocess.Popen(rf'C:\Program Files\Google\Chrome\Application\chrome.exe --remote-debugging-port={port} --user-data-dir="C:\chrometemp"')
                except:
                    subprocess.Popen(rf'C:\Program Files (x86)\Google\Chrome\Application\chrome.exe --remote-debugging-port={port} --user-data-dir="C:\chrometemp"')

                chrome_options = Options()                                                                    # 옵션객체 생성
                chrome_options.add_experimental_option("debuggerAddress", f"127.0.0.1:{port}")
            
            if md == 'secret':
                chrome_options.add_argument('--incognito')
            
            if md == 'android':
                user_agent = random.choice(and_agent)
                chrome_options.add_argument("user-agent=" + user_agent)
            
            if md == 'ios':
                user_agent = random.choice(ios_agent)
                chrome_options.add_argument("user-agent=" + user_agent)
            
            if md not in valid_mode_lst:
                modes_text = ", ".join(valid_mode_lst)
                raise ValueError(f"Invalid Value : {mode}\nPlease Use below instead of {mode}\n\n{modes_text}\n\nUsage : load_driver(mode=['{random.choice(valid_mode_lst)}'])")
        else:
            for md in mode:
        
                if md == 'fast':

                    prefs = {"profile.managed_default_content_settings.images": 2}
                    chrome_options.add_experimental_option("prefs", prefs)
                    
                if md == 'cache':
                    
                    userDataFolder = 'c:/cache/{}'.format(userId)
                    chrome_options.add_argument('--user-data-dir=' + userDataFolder)
                    chrome_options.add_argument('--disk-cache-dir=' + userDataFolder)
                
                if md == 'debug':
                    import subprocess
                    try:
                        subprocess.Popen(rf'C:\Program Files\Google\Chrome\Application\chrome.exe --remote-debugging-port={port} --user-data-dir="C:\chrometemp"')
                    except:
                        subprocess.Popen(rf'C:\Program Files (x86)\Google\Chrome\Application\chrome.exe --remote-debugging-port={port} --user-data-dir="C:\chrometemp"')

                    chrome_options = Options()                                                                    # 옵션객체 생성
                    chrome_options.add_experimental_option("debuggerAddress", f"127.0.0.1:{port}")
                
                if md == 'secret':
                    chrome_options.add_argument('--incognito')

                if md == 'android':
                    user_agent = random.choice(and_agent)
                    chrome_options.add_argument("user-agent=" + user_agent)
                
                if md == 'ios':
                    user_agent = random.choice(ios_agent)
                    chrome_options.add_argument("user-agent=" + user_agent)
                
                if md not in valid_mode_lst:
                    modes_text = ", ".join(valid_mode_lst)
                    raise ValueError(f"Invalid Value : {mode}\nPlease Use below instead of {mode}\n\n{modes_text}\n\nUsage : load_driver(mode=['{random.choice(valid_mode_lst)}'])")
    
    if os.path.isfile(f'c:\\chromedriver\\{chrome_ver}\\chromedriver.exe'):
        driver = webdriver.Chrome(executable_path=f'c:\\chromedriver\\{chrome_ver}\\chromedriver.exe', options=chrome_options, **kwargs)
    else:
        try:
            driver = webdriver.Chrome(executable_path=AutoChrome.install(path=chrome_driver_path), options=chrome_options, **kwargs)
        except:
            find_testdriver()
            driver = webdriver.Chrome(executable_path=f'c:\\chromedriver\\{chrome_ver}\\chromedriver.exe', options=chrome_options, **kwargs)

    while len(driver.window_handles) > 1:
        driver.close()
        driver.switch_to.window(driver.window_handles[0])

    return driver
