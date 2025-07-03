from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time

VAR_SIGN_IN = '//*[@id="signIn"]'
MODAL_ONE = '//*[@id="jqi_state0_buttonOk"]'



class StudioElement:
    def __init__(self, driver, polling, logger):
        self.driver = driver
        self.log = logger
        self.poll = polling
        time.sleep(2.0)
        
    def click_modal_one(self):
        self.log.debug("Clicking Modal One")
        try:
            modal_one = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, MODAL_ONE))
            )
            self.driver.execute_script("arguments[0].scrollIntoView(true);", modal_one)
            self.driver.execute_script("arguments[0].click();", modal_one)
        except Exception as e:
            self.log.error(f"Error clicking Modal One: {e}")
            raise e

