import unittest
from queue import Queue
from unittest.mock import MagicMock
from undetected_browser_tool import UndetectedBrowserTool
from tabulate import tabulate


class TestUndetectedBrowserTool(unittest.TestCase):
    def setUp(self):
        #self.tool = UndetectedBrowserTool(headless=False)
        # opts = {"proxy-server": "http://134.122.26.11:80"}
        # self.tool = UndetectedBrowserTool(headless=True, additional_opts=opts)
        self.tool = UndetectedBrowserTool(headless=True)


    def test_fetch_page(self):
        url = "https://example.com"
        page_text = self.tool.fetch_page(url)
        print(page_text)
        self.assertIsInstance(page_text, str)
        

    def test_run(self):
        url = "https://example.com"
        result = self.tool._run(url)
        self.assertIsInstance(result, str)

    def test_bot_detection(self):
        url = "https://www.browserscan.net/bot-detection"
        
        self.tool.set_type(as_text=False)
        result = self.tool._run(url)
        self.assertIsInstance(result, str)
        headers = ['Browser Check', 'Result']
        print(tabulate(parse_html_to_tabulate(result),  headers=headers, tablefmt="pretty"))


from bs4 import BeautifulSoup, Tag

search_texts = [
    'WebDriver', 'WebDriver Advance', 'Selenium', 'NightmareJS', 'PhantomJS',
    'Awesomium', 'Cef', 'CefSharp', 'Coaches', 'FMiner', 'Born', 'Phantomas',
    'Rhino', 'Webdriverio', 'Headless Chrome', 'CDP', 'vendorSub', 'productSub',
    'vendor', 'maxTouchPoints', 'scheduling', 'userActivation', 'doNotTrack',
    'geolocation', 'connection', 'plugins', 'mimeTypes', 'pdfViewerEnabled',
    'webkitTemporaryStorage', 'webkitPersistentStorage', 'windowControlsOverlay',
    'hardwareConcurrency', 'cookieEnabled', 'appCodeName', 'appName', 'appVersion',
    'platform', 'product', 'userAgent', 'language', 'languages', 'onLine',
    'webdriver', 'getGamepads', 'javaEnabled', 'sendBeacon', 'vibrate',
    'constructor', 'deprecatedRunAdAuctionEnforcesKAnonymity', 'protectedAudience',
    'bluetooth', 'storageBuckets', 'clipboard', 'credentials', 'keyboard', 'managed',
    'mediaDevices', 'storage', 'serviceWorker', 'virtualKeyboard', 'wakeLock',
    'deviceMemory', 'userAgentData', 'login', 'ink', 'mediaCapabilities', 'hid',
    'locks', 'gpu', 'mediaSession', 'permissions', 'presentation', 'usb', 'xr',
    'serial', 'adAuctionComponents', 'runAdAuction', 'canLoadAdAuctionFencedFrame',
    'clearAppBadge', 'getBattery', 'getUserMedia', 'requestMIDIAccess',
    'requestMediaKeySystemAccess', 'setAppBadge', 'webkitGetUserMedia',
    'clearOriginJoinedAdInterestGroups', 'createAuctionNonce',
    'deprecatedReplaceInURN', 'deprecatedURNToURL', 'getInstalledRelatedApps',
    'joinAdInterestGroup', 'leaveAdInterestGroup', 'updateAdInterestGroups',
    'registerProtocolHandler', 'unregisterProtocolHandler', '__defineGetter__',
    '__defineSetter__', '__lookupGetter__', '__lookupSetter__', 'isPrototypeOf',
    'propertyIsEnumerable', 'toString', 'valueOf', 'toLocaleString'
]

def parse_html_to_tabulate(html_content):
    
    soup = BeautifulSoup(html_content, 'html.parser')
    
    results = []

    t_results : Tag = soup.find_all(string='Test Results:')[0]
    test_results = t_results.find_next('strong').get_text(strip=True)
    
    results.append(['Test Results:', test_results])
    
    # Iterate over each text in search_texts
    for text in search_texts:
        # Find all elements containing the text
        elements = soup.find_all(string=text)

        for element in elements:
            # Navigate to the great-great-grandparent node (two levels up)
            grandparent = element.find_parent().find_parent().find_parent().find_parent()

            if grandparent:
                # Find the first span within the grandparent
                first_span : Tag = grandparent.find('span')
                value = "" 
                if first_span is not None:
                    #print(text)
                    #print(first_span)
                    #print(type(first_span))
                    value = first_span.get_text(strip=True)
                        
                # Store the result
                # result = {
                #     'search_text': text,
                #     'grandparent': str(grandparent) if grandparent else None,
                #     'first_span': str(first_span) if first_span else None
                # }
                
                result = [text, value]
                results.append(result)

    return results



if __name__ == "__main__":
    unittest.main()