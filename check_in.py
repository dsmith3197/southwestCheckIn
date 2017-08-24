from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait

from optparse import OptionParser
from datetime import datetime
from datetime import timedelta

import sched, time

# Command line flags to pass.  All are Required
parser = OptionParser()
parser.add_option("-c", "--confirmation_number",
                  action="store",
                  type="string",
                  dest="confirmation_number",
                  help="flight confirmation number")
parser.add_option("-f", "--first_name",
                  action="store",
                  type="string",
                  dest="first_name",
                  help="first name of passenger")
parser.add_option("-l", "--last_name",
                  action="store",
                  type="string",
                  dest="last_name",
                  help="last name of passenger")
parser.add_option("-p", "--phone_number",
                  action="store",
                  type="string",
                  dest="phone_number",
                  help="phone number (1234567890)")
parser.add_option("-t", "--time",
                  action="store",
                  type="string",
                  dest="time",
                  help="flight time")
(options, args) = parser.parse_args()

# scheduler to schedule when we check in
s = sched.scheduler(time.time, time.sleep)

driver = None

# browser is opened 20 seconds before check in time
def open_browser():
    global driver
    driver = webdriver.Chrome()

    wait = WebDriverWait(driver, 10)
    driver.get("https://www.southwest.com/flight/retrieveCheckinDoc.html")

    # find text boxes to input data
    first_name = driver.find_element_by_id("firstName")
    last_name = driver.find_element_by_id("lastName")
    confirmation_number = driver.find_element_by_id("confirmationNumber")

    # input data
    first_name.send_keys(options.first_name)
    last_name.send_keys(options.last_name)
    confirmation_number.send_keys(options.confirmation_number)

def check_in():
    check_in = driver.find_element_by_id("submitButton")
    check_in.click()

    # while it is too early, keep retrying!
    oops = driver.find_element_by_class_name("oopsError_message")
    while oops.is_displayed():
    	check_in = driver.find_element_by_id("submitButton")
    	while not check_in.is_displayed():
    		print "error displayed"
    	check_in.click()
    	oops = driver.find_element_by_class_name("oopsError_message")
        time.sleep(0.5)

    # confirm check in on next page
    printDocumentsButton = driver.find_element_by_id("printDocumentsButton")
    while not printDocumentsButton.is_displayed():
        print
    printDocumentsButton.click()

    # Send Boarding Pass to Phone
    textBoardingPass = driver.find_element_by_id('optionText')
    while not textBoardingPass.is_displayed():
    	print
    time.sleep(1)
    phoneArea = driver.find_element_by_id("phoneArea")
    phonePrefix = driver.find_element_by_id("phonePrefix")
    phoneNumber = driver.find_element_by_id("phoneNumber")

    phone_number = str(options.phone_number)
    textBoardingPass.click()

    phoneArea.send_keys(phone_number[0:3])
    phonePrefix.send_keys(phone_number[3:6])
    phoneNumber.send_keys(phone_number[6:10])

    # submit the request
    driver.find_element_by_id("checkin_button").click()

# calculate time to start checking in
flight_time = datetime.strptime(options.time, '%b %d %Y %I:%M%p')
check_in_time = flight_time - timedelta(days=1)
check_in_time_seconds = time.mktime(check_in_time.timetuple())

s.enterabs(check_in_time_seconds - 20, 1, open_browser, ())
s.enterabs(check_in_time_seconds, 1, check_in, ())
s.run()
