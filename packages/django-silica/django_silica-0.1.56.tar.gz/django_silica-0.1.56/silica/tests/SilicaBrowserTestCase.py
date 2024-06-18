from urllib.parse import urlparse, parse_qs

from selenium import webdriver
from selenium.webdriver.common.by import By

from django.test import override_settings
from django.contrib.staticfiles.testing import StaticLiveServerTestCase

from silica.tests.urls import urlpatterns as silica_test_url_patterns
from silica.urls import urlpatterns as silica_urlpatterns

urlpatterns = silica_urlpatterns + silica_test_url_patterns


@override_settings(ROOT_URLCONF=__name__)
class SilicaBrowserTestCase(StaticLiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        options = webdriver.ChromeOptions()
        options.add_argument('--log-level=DEBUG')
        options.add_argument("--headless")
        options.add_argument("--remote-debugging-pipe")
        options.add_argument("--disable-gpu")
        options.add_argument("--disable-extensions")
        options.add_argument("--no-sandbox")
        options.add_argument("--incognito")
        options.add_argument("--disable-dev-shm-usage")
        options.binary_location = '/usr/bin/chromium'
        options.set_capability('goog:loggingPrefs', {'browser': 'ALL'})

        # service = webdriver.ChromeService(log_output=subprocess.STDOUT, service_args=['--verbose'])
        cls.selenium = webdriver.Chrome(options)

    def get_query_param(self, param):
        url = self.selenium.current_url
        parsed_url = urlparse(url)
        query_params = parse_qs(parsed_url.query)
        return query_params.get(param, [None])[0]

    def get_url(self):
        return self.selenium.current_url

    def get_page_source(self):
        return self.selenium.page_source

    def get_console_log(self):
        return self.selenium.get_log('browser')

    def assertConsoleLogContains(self, text):
        logs = self.get_console_log()
        self.assertTrue(any(text in log['message'] for log in logs))

    def assertHtmlContains(self, text):
        assert text in self.selenium.page_source, f'"{text}" is not seen in the page source'
        return self

    def assertHtmlNotContains(self, text):
        assert text not in self.selenium.page_source, f'"{text}" is seen in the page source'
        return self

    def findElementById(self, element_id):
        return self.selenium.find_element(By.ID, element_id)

    def assertElementIsVisible(self, element):
        self.assertTrue(element.is_displayed())
        return self

    def assertIdIsVisible(self, element_id):
        element = self.findElementById(element_id)
        self.assertTrue(element.is_displayed())
        return self

    def assertIdIsNotVisible(self, element_id):
        element = self.findElementById(element_id)
        self.assertFalse(element.is_displayed())
        return self

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super().tearDownClass()
        pass
