import os

import pytest
from selenium import webdriver
from webdriver_manager import driver
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.microsoft import IEDriverManager, EdgeChromiumDriverManager



@pytest.fixture(autouse=True)
def setup(request, browser, url):
    browser = "chrome"
    url = "https://www.yatra.com/"

    if browser == "chrome":
        driver = webdriver.Chrome(executable_path=ChromeDriverManager().install())
    elif browser == "firefox":
        driver = webdriver.Firefox(executable_path=GeckoDriverManager().install())
    elif browser == "ie":
        driver = webdriver.Ie(IEDriverManager().install())
    elif browser == "edge":
        driver = webdriver.Edge(EdgeChromiumDriverManager().install())
    else:
        print("No Browser Value is provided")

    driver.get(url)
    driver.maximize_window()
    request.cls.driver = driver
    yield
    driver.close()

def pytest_addoption(parser):
    parser.addoption("--browser")
    parser.addoption("--url")

@pytest.fixture(scope="class", autouse=True)
def browser(request):
    return request.config.getoption("--browser")

@pytest.fixture(scope="class", autouse=True)
def url(request):
    return request.config.getoption("--url")

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item):
    pytest_html = item.config.pluginmanager.getplugin("html")
    outcome = yield
    report = outcome.get_result()
    extra = getattr(report, "extra", [])
    if report.when == "call":
        # always add url to report
        extra.append(pytest_html.extras.url("http://www.google.com/"))
        xfail = hasattr(report, "wasxfail")
        if (report.skipped and xfail) or (report.failed and not xfail):
            # only add additional html on failure
            report_directory = os.path.dirname(item.comfig.option.htmlpath)
            file_name = report.nodeid.replace("::", "_") + ".png"
            destinationFile = os.path.join(report_directory, file_name)
            driver.save_screenshot(destinationFile)
            if file_name:
                html= '<div><img src="%s" alt="screenshot" style="width:300px;height:200px" '\
                    'onclick="window.open(this.src)" align="right"></div>'%file_name
            extra.append(pytest_html.extras.html(html))
        report.extra = extra

def pytest_html_report_title(report):
    report.title = "Python Automation Report"





