import time

from selenium.webdriver.common.keys import Keys

from .client import RefresherClient


class Twenty23(RefresherClient):
    """
    2023 hack attempt
    """

    # Source https://twitter.com/BronzeGod4/status/1588236864242302977/photo/1
    REGISTRATION_PHRASE = "Please enter your Glastonbury registration details"
    def _refreshcheck(self, url, phrases_to_check):
        def isregistration(content):
            # print('checking if registration page')
            try:
                content.find_element("id", "main-frame-error")
                print('chrome error page')
                return False
            except:
                try:
                    condition = False
                    for p in phrases_to_check:
                        if p.lower() in content.text.lower():
                            condition = True
                    return condition
                except Exception as e:
                    print('Unable to check if registration page', e)

            return False

        try: 
            self.content = self.client.find_element("id", "main-frame-error")
            print('chrome error page')
        except:
            try:
                self.content = self.client.find_element("tag name", "body")
                # This code below has been deprecated in the latest version of selenium
                #  self.content = self.client.find_element_by_tag_name("body")
                # _ = self.client.find_element_by_tag_name('h1')
                # self.content = self.client.find_element_by_class_name(
                #     'entry-content')
            except:
                print(
                    "Incorrect html format found. Is the URL as expected? URL: {}".format(
                        url
                    )
                )

        # here check for phrases expected in registration page
        # i.e. Please enter registration details...
        while not isregistration(self.content):

            # try again
            if self.verbose:
                print("Refreshing...")
            time.sleep(self.refreshrate)

            if self.client.current_url != url:
                self.client.get(url)
            else:
                self.client.refresh()
            

            try:
                self.content = self.client.find_element("tag name", "body")
                # self.content = self.client \
                #     .find_element_by_xpath("//*[contains(text(), '{}')]".format(REGISTRATION_PHRASE))
            except:
                print('Unable to find body')
                continue
        print("Registration url: {}".format(self.client.current_url))


        self.content = self.pagesource
        # self.client.save_screenshot('./screenshots/registrationpage.png')

    def submit_registration(self, details):
        """
        A bit hacky and largely dependent on id and class names (not good!)
        """

        submitted = False
        inputs = self.client.find_elements("tag name", "input")

        # loop to find registration input
        reg_count = 0
        post_code_count = 0
        for i in inputs:
            if reg_count == len(details) and post_code_count == len(details):
                break
            print(i.get_attribute("name").lower())
            # if foundNum and foundPost:
            #     break
            if "registrationid" in i.get_attribute("name").lower():
                i.send_keys(details[reg_count]["number"])
                reg_count += 1
            if "postcode" in i.get_attribute("name").lower():
                i.send_keys(details[post_code_count]["postcode"])
                post_code_count += 1

        if reg_count != len(details) or post_code_count != len(details):
            print("No such input.")
            # how to handle invalid or mismatch??

        # self.client.save_screenshot('./screenshots/registrationpresubmitted.png')
        # print("Pre registration url: {}".format(self.client.current_url))
        # loop again to find submit and go to submit page
        for i in inputs:
            if "submit" in i.get_attribute("type").lower():
                print("submitting...")
                i.send_keys(Keys.ENTER)
                submitted = True

        # self.client.save_screenshot('./screenshots/registrationpostsubmitted.png')
        # print("Post registration url: {}".format(self.client.current_url))
        return submitted
