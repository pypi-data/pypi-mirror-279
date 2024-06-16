from kdb import report
from unit_test.pc import hidden_ads
from kdb.webdriver import kdb_driver


def test_browser_nav():
    # start browser
    report.add_comment("Test browser navigation")
    # start browser
    kdb_driver.start_browser()
    # load page for test.
    kdb_driver.open_url('https://demoqa.com/books')
    hidden_ads()

    kdb_driver.click("xpath=//a[@href='/books?book=9781449325862']")
    kdb_driver.verify_text_on_page("9781449325862")
    kdb_driver.verify_text_on_page("Back To Book Store")
    kdb_driver.verify_url_contains("/books?book=9781449325862")
    kdb_driver.screen_shot()
    kdb_driver.back()
    kdb_driver.verify_url_contains("https://demoqa.com/books")
    kdb_driver.screen_shot()
    kdb_driver.forward()
    kdb_driver.verify_text_on_page("Back To Book Store")
    kdb_driver.screen_shot()

    kdb_driver.close_browser()
