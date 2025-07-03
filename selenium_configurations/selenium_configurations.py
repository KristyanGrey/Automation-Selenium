from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
# from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.firefox.service import Service as FirefoxService
from element_of_pages.login_element import LoginElements
from element_of_pages.cloud_element import CloudElement
from element_of_pages.studio_element import StudioElement
# from .pages.checkout import Checkout
# from .pages.guest_checkout import GuestClass
# from .pages.login_n_order import LoginAndOrder
import logging
import traceback
import threading
import time
import os


MOBILE_X = 640
MOBILE_Y = 719


class SeleniumTest():
    def __init__(self, name, url, settings, user_data, poll=None):
        self.name = name
        self.url = url
        self.settings = settings
        self.poll = poll
        self.user_data = user_data
        self.results = []

    def __config(self, settings):

        # SETUP LOGGING
        self.log = logging.getLogger(f"{self.name}")
        self.log.setLevel(level=logging.INFO)
        log_handler = logging.StreamHandler()
        log_handler.setLevel(level=logging.INFO)
        self.log.addHandler(log_handler)

        # VALIDATE INPUTS
        ###################

        # RETRIEVE CONFIG VALUES AND SET UP WEBDRIVER CONFIG
        headless = settings['headless']
        detatched = settings['detatched']
        incognito = settings['incognito']

        for browser in settings['browser']:
            if browser == "chrome":
                for resolution in settings['resolution']:
                    options = ChromeOptions()
                    options.add_argument('--no-sandbox')
                    options.browser_version = "stable"
                    if headless:
                        options.add_argument('--headless')
                    if detatched:
                        options.add_experimental_option("detach", True)
                    if incognito:
                        options.add_argument('--incognito')
                    if resolution[0] < MOBILE_X:
                        print("Session is mobile.\n")
                        mobile_emulation = {
                            "deviceMetrics": { "width": resolution[0], "height": resolution[1], "pixelRatio": 3.0},
                            "userAgent": "Mozilla/5.0 (iPhone; CPU iPhone OS 10_3 like Mac OS X) AppleWebKit/602.1.50 (KHTML, like Gecko) CriOS/56.0.2924.75 Mobile Safari/535.19"}
                        options.add_experimental_option("mobileEmulation", mobile_emulation)
                    else:
                        print("Session is laptop/pc.\n")
                        options.add_argument(f'window-size={resolution[0]},{resolution[1]}')
                    self.driver = webdriver.Chrome(options=options)
                    self.driver.set_page_load_timeout(60)
                    self.__execute_sequence(browser, resolution, detatched)
            if browser == "firefox":
                for resolution in settings['resolution']:
                    options = FirefoxOptions()
                    service = FirefoxService()
                    if headless:
                        options.add_argument('--headless')
                    if detatched:
                        options.set_preference('detach', True)
                    if resolution[0] < MOBILE_X:
                        options.add_argument('--user-agent=Mozilla/5.0 (iPhone; CPU iPhone OS 10_3 like Mac OS X) AppleWebKit/602.1.50 (KHTML, like Gecko) CriOS/56.0.2924.75 Mobile/14E5239e Safari/602.1')
                    options.add_argument('--disable-dev-shm-usage')
                    self.driver = webdriver.Firefox(options=options, service=service)
                    self.driver.set_window_position(0, 0)
                    self.driver.set_window_size(resolution[0], resolution[1])
                    self.__execute_sequence(browser, resolution, detatched)

            if browser == "safari":
                for resolution in settings['resolution']:
                    pass

            if browser == "edge":
                for resolution in settings['resolution']:
                    pass

    def __execute_sequence(self, browser, resolution, detatched):
        resolution = str(resolution).replace(',', '')
        get_time = time.strftime("%Y%m%d-%H%M%S")
        logname = f"{self.name}-{browser}-{resolution}-{get_time}"
        testname = f"{self.name} -- {browser}, {resolution}"
        log_directory = "logs"  # Define the log directory

        # Set up logging
        self.test_log = logging.getLogger(f"{self.name}-{browser}-{resolution}")
        self.test_log.setLevel(level=logging.DEBUG)

        log_path = os.path.join(log_directory, f"{logname}.txt")

        try:
            file_handler = logging.FileHandler(log_path, mode='w')
            file_handler.setLevel(level=logging.DEBUG)
            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            file_handler.setFormatter(formatter)
            self.test_log.addHandler(file_handler)
        except Exception as e:
            self.log.error(f"Error setting up test log file: {e}")
            return  # Exit the method if logging setup fails

        test_sequence = {
            'event': testname,
            'pass': False,
            'error': None
        }

        try:
            self.log.info(f"Running Test: {testname}")
            self.sequence()
            test_sequence['pass'] = True
        except Exception as e:
            print("Test failed!")
            self.log.error("Test failed!")
            try:
                # Use the correct path to access the log file
                with open(log_path, "r") as file:
                    test_log_data = file.read()
                    self.log.error(f"Retrieving test log... \n{test_log_data}")
            except Exception:
                self.log.error("Unable to access test level logging.")
            self.log.error(f"{traceback.format_exc()}\n")
            test_sequence['error'] = e

        if not detatched:
            print(detatched)
            try:
                self.driver.quit()
            except Exception:
                self.log.debug("Unable to quit driver window.")

        self.results.append(test_sequence)  # Fixed typo: self.result to self.results

    def start(self):
        self.test_thread = threading.Thread(target=self.__config, args=(self.settings,))
        self.test_thread.start()

    def load_website(self):
        self.driver.get(self.url)
        return self.driver
    
    def get_login_page_element(self):
        page = LoginElements(self.driver, self.poll, self.test_log)
        return page

    def get_cloud_element(self):
        page = CloudElement(self.driver, self.poll, self.test_log)
        return page 
    
    def get_studio_element(self):
        page = StudioElement(self.driver, self.poll, self.test_log)
        return page 

    def get_result(self):
        return self.results

    def sequence():
        pass
