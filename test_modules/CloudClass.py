from selenium_configurations.selenium_configurations import SeleniumTest


class CloudLogin(SeleniumTest):
    def __init__(self, name, url, settings, user_data, poll=None):
        super().__init__(name, url, settings, user_data, poll)

    def sequence(self):
        
        self.load_website()
        cloud_page = self.get_cloud_element()
        cloud_page.enter_cloud_email("christian.odevilas@deliverit.com.au")
        cloud_page.enter_cloud_pass("EasyPassDEV123456")
        cloud_page.click_login_button()
        cloud_page.select_sidebar_oo_admin("Online Ordering Admin")
        cloud_page.click_skip_button()
        cloud_page.search_and_select_store("xtian test store 01")
        cloud_page.click_skip_button()
        cloud_page.click_sidebar_menu_item()
        cloud_page.click_add_item_button()
        cloud_page.click_checkbox()
        cloud_page.enter_test_in_modal_plu("AUT001")
        