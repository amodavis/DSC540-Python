# --------------------------------------------------------------------------------------
# File: Exercise_8.2.py
# Name: Amie Davis
# Date: 10/17/2019
# Course: DSC540 - Data Preparation
# Assignment Number: 8.2
#
# Purpose:  Ch 11 & 12 Review: Web Scraping
#           Open and get response from a web page.
#           Use Beautiful Soup to scrape info from Take Action articles.
#           Interact with web page using Selenium.
#
# Websites Utilized: http://google.com
#                    http://www.enoughproject.org/take_action
#
# Usage: Uses Python 3.7.
#        Developed using PyCharm 2019.1.3.
#
# --------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------
# Function open_website()
#
# Description:  Connects to website
#
# Parameters:   url: website URL
#
# Returns:      No return value
#
def open_website(url):

    import urllib.request

    url_open = urllib.request.urlopen(url)
    url_read = url_open.read()
    #print(url_read[:200])

# --------------------------------------------------------------------------------------
# Function get_web_response()
#
# Description:  Calls HTTP get and returns response
#
# Parameters:   url: website URL
#
# Returns:      website response
#
def get_web_response(url):

    import requests

    url_req = requests.get(url)

    # Make sure we have a 200 response
    #print(url_req.status_code)
    #print(url_req.content[:200])

    # Check the response’s headers attribute
    #print(url_req.headers)

    # Reads cookies and returns key-value pairs
    #print(url_req.cookies.items())

    return(url_req)

# --------------------------------------------------------------------------------------
# Function bea_soup()
#
# Description:  Gets website info using Beautiful Soup.
#               Specifically, outputs each Take Action entry into dictionary with matching keys.
#
# Parameters:   url: website URL
#
# Returns:      No return value.  Outputs to screen.
#
def bea_soup(url):

    from bs4 import BeautifulSoup
    import requests

    # Grab the content of the page
    page = requests.get(url)
    bs = BeautifulSoup(page.content, features="html.parser")

    # Show page title
    print(bs.title)

    # Show all anchor and paragraph tags
    #print(bs.find_all('a'))
    #print(bs.find_all('p'))

    # Creates a list of children from the header
    header_children = [c for c in bs.head.children]
    #print(header_children)

    # Finds a selected element using CSS Selector ID
    # Note that ID in text is no longer valid - globalNavigation
    # Used mega-menu-wrap for Menu bar instead
    sel_element = bs.find(id="mega-menu-wrap")

    # Iterates over children of selected element
    #for d in sel_element.descendants:
    #    print(d)

    #for s in sel_element.previous_siblings:
    #    print(s)

    # Find info on Action Articles
    # Note that class name in our text is no longer valid (views-row)
    # Used wpb_wrapper as the class used by article links
    # Note there is no header (h2), so it has been excluded
    ta_divs = bs.find_all("div", class_="wpb_wrapper")
#    print(len(ta_divs))

    # Iterates through all of the article links
    all_data = []
    for ta in ta_divs:
        data_dict = {}
        link = ta.a

        # Ignore the first few records that don't have article links
        if link is not None:
            data_dict['title'] = ta.h6
            data_dict['link'] = ta.a.get('href')
            data_dict['about'] = [p.get_text() for p in ta.find_all('p')]
            all_data.append(data_dict)

    # Outputs each Take Action entry into dictionary with matching keys
    print(all_data)
# --------------------------------------------------------------------------------------
# Function open_browser()
#
# Description:  Opens browser with Selenium driver
#
# Parameters:   None.
#
# Returns:      browser
#
def get_browser():
    browser = webdriver.Chrome()
    return browser

# --------------------------------------------------------------------------------------
# Function find_text_element()
#
# Description:  Retrieves text element using Selenium
#
# Parameters:   html_element
#               element_css
#
# Returns:      Text element
#
def find_text_element(html_element, element_css):
    try:
        text_element = html_element.find_element_by_css_selector(element_css).text
        return text_element
    except NoSuchElementException:
        pass
    return None

# --------------------------------------------------------------------------------------
# Function find_attr_element()
#
# Description:  Retrieves text for element's attribute using Selenium
#
# Parameters:   html_element
#               element_css
#               attr
#
# Returns:      No return value
#
def find_attr_element(html_element, element_css, attr):
    try:
        return html_element.find_element_by_css_selector(element_css).get_attribute(attr)
    except NoSuchElementException:
        pass
    return None

# --------------------------------------------------------------------------------------
# Function selenium_scrape()
#
# Description:  Retrieves web page content using Selenium
#
# Parameters:   url: website URL
#
# Returns:      List of dictionary values of content
#
def selenium_scrape(url):

    # Get Web Page
    browser = get_browser()
    browser.get(url)
    browser.implicitly_wait(10)

    # Find content bubbles
    # Note that class name in text is no longer valid - content
    # Found content bubbles under li.feed-item instead
    try:
        all_bubbles = browser.find_elements_by_css_selector('li.feed-item')
    except WebDriverException:
        browser.implicitly_wait(5)
        all_bubbles = browser.find_elements_by_css_selector('li.feed-item')

    # Iterate over content bubbles to pull out elements
    # Note that class names in text are no longer valid
    # There are no longer names or timestamps on the posts
    # Found text under div.j-message
    # Found original link under a.j-image
    # Found picture under img
    all_data = []
    for elem in all_bubbles:
        elem_dict = {}
        elem_dict['text_content'] = find_text_element(elem, 'div.j-message')
        elem_dict['original_link'] = find_attr_element(elem, 'a.j-image', 'href')
        elem_dict['picture'] = find_attr_element(elem, 'img', 'src')
        all_data.append(elem_dict)
    browser.quit()
    return(all_data)

# --------------------------------------------------------------------------------------
# Function selenium_interact()
#
# Description:  Interacts with web page using Selenium
#
# Parameters:   url: website URL
#
# Returns:      No return value
#
def selenium_interact(url):
    from time import sleep

    # Open browser
    browser = get_browser()
    browser.get(url)

    # Finds the form
    # Note that selector name in text is no longer valid
    # Used Copy CSS Selector feature to retrieve updated name
    inputs = browser.find_elements_by_css_selector('.gLFyf')
    for i in inputs:
        if i.is_displayed():
            search_bar = i
        break

    # Fills out form
    search_bar.send_keys('web scraping with python')

    # Submits form
    # Note that selector name in text is no longer valid
    # Used Copy CSS Selector feature to retrieve updated name
    search_button = browser.find_element_by_css_selector('div.VlcLAe:nth-child(7) > center:nth-child(2) > input:nth-child(1)')
    search_button.click()

    browser.implicitly_wait(10)

    # Scrolls down to each result
    results = browser.find_elements_by_css_selector('div h3')
    for r in results:
        action = webdriver.ActionChains(browser)
        action.move_to_element(r)
        action.perform()
        sleep(2)

    browser.quit()

# --------------------------------------------------------------------------------------
# Main function
#
def main():

    ###############################################
    # Part I - Connect to the Internet using urllib
    ###############################################
    import urllib.parse

    # Identify web pages
    google_url = 'http://google.com'
    google_query_url = 'http://google.com?q='
    url_with_query = google_query_url + urllib.parse.quote_plus('python web scraping')
    # Open the google website
    open_website(google_url)

    # Open google search
    open_website(url_with_query)

    # Set response from google search page
    url_resp = get_web_response(url_with_query)

    ###############################################
    # Part II - Read a Web Page with Beautiful Soup
    ###############################################
    # Identify web page
    enough_url = 'http://www.enoughproject.org/take_action'

    # Use Beautiful Soup to scrape info from Take Action articles
    bea_soup(enough_url)

    ###############################################
    # Part III - Web Scraping with Selenium
    ###############################################
    # Retrieve dara from a web page using Selenium
    fairphone_url = 'http://www.fairphone.com/we-are-fairphone/'
    content_data = selenium_scrape(fairphone_url)
    # print(content_data)

    # Interact with web page using Selenium
    selenium_interact(google_url)

#----------------------------------------------------------------
# Run program

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException

main()
