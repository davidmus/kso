import unittest

import twill
from twill import commands as tc
from twill.shell import TwillCommandLoop
from django.test import TestCase
from django.core.servers.basehttp import AdminMediaHandler
from django.core.handlers.wsgi import WSGIHandler
from StringIO import StringIO
import os

os.environ['DJANGO_SETTINGS_MODULE'] = 'ksodjango.settings'

def twill_setup():
    app = AdminMediaHandler(WSGIHandler())
    twill.add_wsgi_intercept("127.0.0.1", 8080, lambda: app)

def twill_teardown():
    twill.remove_wsgi_intercept('127.0.0.1', 8080)

def make_twill_url(url):
    # modify this
    return url.replace("http://www.kso.org.uk/",
                       "http://127.0.0.1:8080/")

def twill_quiet():
    # suppress normal output of twill.. You don't want to
    # call this if you want an interactive session
    twill.set_output(StringIO())

class testHomePage(TestCase):

    def setUp(self):
        twill_setup()

    def tearDown(self):
        twill_teardown()

    def test_openSite(self):
        url = "http://www.kso.org.uk/"
        twill_quiet()
        tc.go(make_twill_url(url))
        assert "KSO ::" in tc.title()

#    def test_homePageHasNextConcertLink(self):
#        browser = webdriver.Firefox()
#        browser.get("http://localhost:8000")
#        title = browser.find_element_by_xpath("//h2[2]")
#        assert "Next concert" in title.text
#        browser.close()
#
#    def test_homePageShowsQuotes(self):
#        browser = webdriver.Firefox()
#        browser.get("http://localhost:8000")
#        quotes = browser.find_element_by_xpath("//div[@id='quotes']")
#        assert "One of the very best" in quotes.text
#        browser.close()
#
#    # This won't work on OS X at the moment - no native events support
#    def xtest_switchMenu(self):
#        browser = webdriver.Firefox()
#        browser.get("http://localhost:8000")
#        print browser.title
#        home = browser.find_element_by_xpath("//div[@id='submenu']//a[text()='Home']")
#        assert home.is_displayed()
#        nextConcert = browser.find_element_by_xpath("//div[@id='submenu']//a[text()='Next concert']")
#        assert not nextConcert.is_displayed()
#        concerts = browser.find_element_by_xpath("//div[@id='tabsmenu']//a[text()='Concerts']")
#        actions = ActionChains(browser)
#        actions.move_to_element(concerts)
#        actions.perform()
#        assert not home.is_displayed()
#        assert nextConcert.is_displayed()
#        browser.close()

if __name__ == '__main__':
    unittest.main()