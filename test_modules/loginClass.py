from selenium_configurations.selenium_configurations import SeleniumTest


class LoginModule(SeleniumTest):
    def __init__(self, name, url, settings, user_data, poll=None):
        super().__init__(name, url, settings, user_data, poll)

    def sequence(self):

        self.load_website()
        login_page = self.get_login_page_element()  # get elements from get_login_page
        login_page.click_login_button_t3()
        login_page.enter_username_t3(self.user_data.get('email'))
        login_page.enter_password_t3(self.user_data.get('password'))
        login_page.click_proceed_login_t3()
