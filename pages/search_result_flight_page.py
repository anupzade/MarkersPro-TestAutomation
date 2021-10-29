import time

from selenium.webdriver.common.by import By
from base.base_driver import BaseDriver
from utilities.utils import Utils

class SearchFilghtResults(BaseDriver):
    log = Utils.custom_logger()

    FILTER_BY_1_STOP_Button = "//p[@class='font-lightgrey bold'][normalize-space()='1']"
    FILTER_BY_2_STOP_Button = "//p[@class='font-lightgrey bold'][normalize-space()='2']"
    FILTER_BY_0_STOP_Button =  "//p[@class='font-lightgrey bold'][normalize-space()='0']"
    SEARCH_FILGHT_RESULTS = "//span[contains(text(), '1 Stop') or contains(text(), '2 Stop') or contains(text(), 'Non Stop')]"

    def __init__(self, driver):
        super().__init__(driver)
        self.driver = driver

    def get_one_stop_button(self):
        return self.driver.find_element(By.XPATH, self.FILTER_BY_1_STOP_Button)

    def get_two_stop_button(self):
        return self.driver.find_element(By.XPATH, self.FILTER_BY_2_STOP_Button)

    def get_non_stop_button(self):
        return self.driver.find_element(By.XPATH, self.FILTER_BY_0_STOP_Button)

    def get_search_flights_result(self):
        return self.wait_for_presence_of_all_elements(By.XPATH, self.SEARCH_FILGHT_RESULTS)

    def click_filter_flights_by_stop(self, by_stop):
        if by_stop == '1 Stop':
            self.get_one_stop_button().click()
            self.log.info("Selected Flights With 1 Stop")
            time.sleep(4)
        elif by_stop == '2 Stop':
            self.get_two_stop_button().click()
            self.log.info("Selected Flights With 2 Stop")
            time.sleep(4)
        elif by_stop == 'Non Stop':
            self.get_non_stop_button().click()
            self.log.info("Selected Flights With Non Stop")
            time.sleep(4)
        else:
            self.log.warning("Please Provide Valid Stop Filter Option")


