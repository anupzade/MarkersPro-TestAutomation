import time
import pytest
import softest

from pages.yatra_launch_page import LaunchPage
from utilities.utils import Utils
from ddt import ddt, data, file_data, unpack

@pytest.mark.usefixtures("setup")
@ddt
class TestSearchAndVerifyFilter(softest.TestCase):
    log = Utils.custom_logger()

    @pytest.fixture(autouse=True)
    def class_setup(self):
        self.lp = LaunchPage(self.driver)
        self.ut = Utils()

    # @data(("New Delhi", "JFK", "30/10/2021", "1 Stop"), ("BOM", "JFK", "11/11/2021", "2 Stop"))
    # @unpack
    # @file_data("../testdata/testdata.json")
    # @file_data("../testdata/testyaml.yaml")
    # @data(*Utils.read_data_from_excel("C:\\MarkersPro_TestAutomation\\testdata\\testdataexcel.xlsx", "Sheet1"))
    # @unpack
    @data(*Utils.read_data_from_csv("C:\\MarkersPro_TestAutomation\\testdata\\testdatacsv.csv"))
    @unpack
    def test_search_flights_By_One_Stop(self, goingfrom, goingto, date, stops):
        time.sleep(2)
        search_flight_result = self.lp.search_flights(goingfrom, goingto, date)
        time.sleep(2)
        search_flight_result.click_filter_flights_by_stop(stops)
        self.lp.page_scroll()
        allFlights = search_flight_result.get_search_flights_result()
        self.log.info(len(allFlights))
        self.ut.asserListItemText(allFlights, stops)