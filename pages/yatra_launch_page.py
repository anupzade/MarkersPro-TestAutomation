import time

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from base.base_driver import BaseDriver
from pages.search_result_flight_page import SearchFilghtResults
from utilities.utils import Utils

class LaunchPage(BaseDriver):
    log = Utils.custom_logger()

    def __init__(self, driver):
        super().__init__(driver)
        self.driver = driver

    # LOCATORS
    DEPART_FROM_FIELD = "//input[@id='BE_flight_origin_city']"
    GOING_TO_FIELD = "//input[@id='BE_flight_arrival_city']"
    GOING_TO_SEARCH_RESULT_LIST = "//div[@class='viewport']//div[1]//li"
    DEPART_DATE_FIELD = "//input[@id='BE_flight_origin_date']"
    ALL_DEPART_DATES = "//div[@id='monthWrapper']//tbody//td[@class!='inActiveTD']"
    SEARCH_BUTTON = "BE_flight_flsearch_btn"

    def getDepartFromField(self):
        return self.wait_until_element_is_clickable(By.XPATH, self.DEPART_FROM_FIELD)

    def getGoingToField(self):
        return self.wait_until_element_is_clickable(By.XPATH, self.GOING_TO_FIELD)

    def getGoingToResults(self):
        try:
            return self.wait_for_presence_of_all_elements(By.XPATH, self.GOING_TO_SEARCH_RESULT_LIST)
        except None as e:
            print (e)

    def getDepartureDateField(self):
        return self.wait_until_element_is_clickable(By.XPATH, self.DEPART_DATE_FIELD)

    def getAllDateFields(self):
        return self.wait_until_element_is_clickable(By.XPATH, self.ALL_DEPART_DATES)

    def getSearchButton(self):
        return self.driver.find_element_by_id(self.SEARCH_BUTTON)

    def enterDepartFromLocation(self, deaprtlocation):
        self.getDepartFromField().click()
        time.sleep(2)
        self.getDepartFromField().send_keys(deaprtlocation)
        self.getDepartFromField().send_keys(Keys.ENTER)
        time.sleep(2)

    def enterGoingToLocation (self, goingtolocation):
        time.sleep(1)
        self.getGoingToField().click()
        time.sleep(2)
        self.getGoingToField().send_keys(goingtolocation)
        time.sleep(2)
        search_results = self.getGoingToResults()
        self.log.info(len(search_results))
        time.sleep(2)
        for results in search_results:
            if goingtolocation in results.text:
                results.click()
                time.sleep(1)
                break

    def enterDepartDate(self, departdate):
        time.sleep(4)
        self.getDepartureDateField().click()
        # time.sleep(1)
        # self.getAllDateFields()
        time.sleep(4)
        all_dates = self.getAllDateFields().find_elements(By.XPATH, self.ALL_DEPART_DATES )
        for date in all_dates:
            if date.get_attribute("data-date") == departdate:
                date.click()
                time.sleep(2)
                break

    def clickSearchButton(self):
        self.getSearchButton().click()
        time.sleep(2)

    def search_flights(self, deaprtlocation, goingtolocation, departdate):
        self.enterDepartFromLocation(deaprtlocation)
        self.enterGoingToLocation(goingtolocation)
        self.enterDepartDate(departdate)
        self.clickSearchButton()
        search_flights_results_page = SearchFilghtResults(self.driver)
        return search_flights_results_page