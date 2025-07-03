from selenium_configurations.selenium_configurations import SeleniumTest


class StudioStg(SeleniumTest):
    def __init__(self, name, url, settings, user_data, poll=None):
        super().__init__(name, url, settings, user_data, poll)

    def sequence(self):
        
        self.load_website()
        studio_page = self.get_studio_element()
        studio_page.click_modal_one()
        # sample edit on Vscode
