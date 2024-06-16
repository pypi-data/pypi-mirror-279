from kdb import report
from kdb.webdriver import kdb_driver


def verify_title_test():
    report.add_comment("Test verify title")
    # start browser
    kdb_driver.start_browser()
    # loads page
    kdb_driver.open_url('http://automationpractice.com/index.php')
    # Verify title is Account Suspended
    kdb_driver.verify_title('Account Suspended')
    # Verify title is not Women - My Store
    kdb_driver.verify_title('Women - My Store', reverse=True, timeout=2)
    kdb_driver.screen_shot()

    #
    kdb_driver.open_url("https://demoqa.com/books?book=9781449325862")
    # Verify title is DEMOQA
    kdb_driver.verify_title('DEMOQA')
    # Verify title is not My Store
    kdb_driver.verify_title('Account Suspended', reverse=True, timeout=2)
    kdb_driver.screen_shot()
    kdb_driver.close_browser()
