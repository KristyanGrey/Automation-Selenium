from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time

VAR_CLOUD_LOGIN_FIELD = "(//input[@id='loginform-username'])[1]"
VAR_CLOUD_PASSWORD_FIELD = "(//input[@id='loginform-password'])[1]"
VAR_CLOUD_LOGING_BUTTON = "(//button[normalize-space()='Login'])[1]"
SIDEBAR_OO_ADMIN = "/html/body/section/aside/div[1]/div/div/select"
SKIP_BUTTON_XPATH = '//*[@id="skip-studio"]'
DROPDOWN_SEARCH_BUTTON_XPATH = "/html/body/section/section/div/div[1]/div[1]/div/div[1]/div/span/span[1]/span"
DROPDOWN_SEARCH_INPUT_XPATH = "//input[@type='search']"
SIDEBAR_MENU_ITEM = "/html/body/section/aside/ul/li[4]/a/span[2]"
ADD_ITEM_BUTTON_XPATH = "/html/body/section/section/div/div[1]/div[2]/div[2]/div/div/div[1]/div[2]/button"

CHECKBOX_XPATH = "/html/body/section/section/div/div[1]/div[2]/div[2]/div/div/div[1]/div[2]/button"
PLU_INPUT_XPATH = "(//input[@id='menuitemform-plu'])[1]"


class CloudElement:
    def __init__(self, driver, polling, logger):
        self.driver = driver
        self.log = logger
        self.poll = polling
        time.sleep(2.0)
        
    def enter_cloud_email(self, enter_username):
        self.log.debug("CLOUD - Enter Email")
        element = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, VAR_CLOUD_LOGIN_FIELD)))
        element.send_keys(enter_username)
        
    def enter_cloud_pass(self, enter_password):
        self.log.debug("CLOUD - Enter Password")
        element = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, VAR_CLOUD_PASSWORD_FIELD)))
        element.send_keys(enter_password)
        
    def click_login_button(self):
        self.log.debug("CLOUD - Click Login Button")
        button = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, VAR_CLOUD_LOGING_BUTTON))
        )
        button.click()
        
    def select_sidebar_oo_admin(self, visible_text):
        self.log.debug("CLOUD - Select Sidebar OO Admin Dropdown")
        dropdown = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, SIDEBAR_OO_ADMIN))
        )
        select = Select(dropdown)
        select.select_by_visible_text(visible_text)


# This will create a new PLU

    def click_skip_button(self):
        self.log.debug("Clicking Skip button on modal")
        try:
            skip_btn = WebDriverWait(self.driver, 5).until(
                EC.element_to_be_clickable((By.XPATH, SKIP_BUTTON_XPATH))
            )
            skip_btn.click()
        except Exception:
            self.log.debug("Skip button not found; continuing.")
        
    def search_and_select_store(self, store_name):
        self.log.debug(f"Searching and selecting store: {store_name}")
        # Click the dropdown search button
        dropdown_btn = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, DROPDOWN_SEARCH_BUTTON_XPATH))
        )
        dropdown_btn.click()
        # Wait for the search input to appear
        search_input = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, DROPDOWN_SEARCH_INPUT_XPATH))
        )
        search_input.clear()
        search_input.send_keys(store_name)
        search_input.send_keys(Keys.ENTER)
        
    def click_sidebar_menu_item(self):
        self.log.debug("Clicking sidebar menu item")
        menu_item = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, SIDEBAR_MENU_ITEM))
        )
        menu_item.click()
        
    def click_add_item_button(self):
        self.log.debug("Clicking Add Item button")
        add_item_button = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, ADD_ITEM_BUTTON_XPATH))
        )
        add_item_button.click()
        
    #this is the checkbox on the modal that appears after clicking Add Item 
    def click_checkbox(self): 
        self.log.debug("Clicking the specified checkbox in modal")
        try:
            checkbox = WebDriverWait(self.driver, 5).until(
                EC.element_to_be_clickable((By.XPATH, CHECKBOX_XPATH))
            )
            checkbox.click()
        except Exception:
            self.log.debug("Checkbox in modal not found; continuing.")
            
    def enter_test_in_modal_plu(self):
        self.log.debug("Entering 'test' in PLU field inside modal")
        # Wait for the PLU input to be visible in the modal
        plu_input = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, PLU_INPUT_XPATH))
        )
        self.driver.execute_script("arguments[0].scrollIntoView(true);", plu_input)
        plu_input.clear()
        plu_input.send_keys("test")
        
        
        