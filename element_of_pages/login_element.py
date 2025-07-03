from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
# from .components.ordering_loyalty_popup import LoyaltyPopup
# from .components.ordering_modal import Modal
# from .components.ordering_alert import AlertPopup
# from .components.ordering_login import LoginPopup
# from .components.ordering_signup import HowToSignUpClass
# from .components.ordering_cart import CartPopup
# from .components.ordering_promotional import PromotionalPopup
# from .components.ordering_order_normal_item import OrderNormalItemClassComponents
# from .components.ordering_group_item import Group_Item_Ordering_Components
import time

# login element
VAR_CART_BUTTON_ID = "show_cart"
VAR_LOGIN_BUTTON_CSS = "span#signIn"
VAR_USER_BUTTON_CSS = "ul#navbar-header li.active"
VAR_VLOGIN_T3 = "//ul[@id='navbar-header'][2]/li[2]"
# GET USER DATA TO test_module_controllers
# Template 3 element
VAR_EMAIL = "(//input[@id='login-email'])[1]"
VAR_PASSWORD = "(//input[@id='login-pass'])[1]"
VAR_PROCEED_LOGIN = "(//button[normalize-space()='Login'])[1]"


class LoginElements:
    def __init__(self, driver, polling, logger):
        self.driver = driver
        self.log = logger
        self.poll = polling
        # self.modal = Modal(self.driver, self.log)
        # self.alert = AlertPopup(self.driver, self.log)
        # self.login = LoginPopup(self.driver, self.log)
        # self.cart = CartPopup(self.driver, self.log)
        # self.loyalty = LoyaltyPopup(self.driver, self.log)
        # self.promotional = PromotionalPopup(self.driver, self.log)
        # self.signup = HowToSignUpClass(self.driver, self.log)
        # self.verification_code = None
        time.sleep(2.0)

    # LOGIN PROCESS
    def click_login_button_t3(self):
        self.log.debug("Ordering Page - Clicking login button T3.")
        element = WebDriverWait(self.driver, 55).until(EC.element_to_be_clickable((By.XPATH, VAR_VLOGIN_T3)))
        element.click()
        time.sleep(2)

    def enter_username_t3(self, enter_username):
        self.log.debug("Ordering Page - Click Login Button")
        element = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, VAR_EMAIL)))
        element.send_keys(enter_username)
        time.sleep(1)

    def enter_password_t3(self, enter_password):
        self.log.debug("Ordering Page - Click Login Button")
        element = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, VAR_PASSWORD)))
        element.send_keys(enter_password)
        time.sleep(1)

    def click_proceed_login_t3(self):
        self.log.debug("Ordering Page / Login Popup - Click login.")
        element = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, VAR_PROCEED_LOGIN)))
        element.click()
        time.sleep(6.0)
