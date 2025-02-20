
import random

import threading
import time
from queue import Queue
from typing import Any

import undetected_chromedriver as uc

from langchain.tools import BaseTool
from pydantic import PrivateAttr
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

import atexit


class UndetectedBrowserTool(BaseTool):
    """
        UndetectedBrowserTool class.
        This class represents a tool for fetching the text content from a webpage URL using Selenium and undetected-chromedriver.
        As this is a chrome instance, it is not recommended to use this tool for high performance tasks as it is slow.
        However, it is useful for fetching content from websites that have bot detection mechanisms or require JavaScript rendering.
        
        Methods:
            __init__(self, headless: bool = True, as_text: bool = True, additional_opts: dict = {}, **kwargs):
                Initializes the UndetectedBrowserTool instance.
    """

    name: str = "undetected_browser_tool"
    description: str = "Fetch the text content from a webpage URL using Selenium"

    _task_queue: Queue = PrivateAttr(default=None)
    _driver: Any = PrivateAttr(default=None)
    _worker_thread: threading.Thread = PrivateAttr(default=None)
    _headless: bool = PrivateAttr()
    _additional_opts: dict = PrivateAttr()
    as_text: bool = True
    
    def __init__(self, headless: bool = True, as_text :bool = True, additional_opts: dict = {}, **kwargs):
        """
        Initializes an instance of the `undetected_browser` class.
        Args:
            headless (bool, optional): Whether to run the browser in headless mode. Defaults to True.
            as_text (bool, optional): Whether to return the response as text. Defaults to True.
            additional_opts (dict, optional): Additional options to be passed to the driver, useful for proxies. Defaults to {}.
            **kwargs: Additional keyword arguments.
        """
        super().__init__(**kwargs)
        self._headless = headless
        self._additional_opts = additional_opts
        self._task_queue = Queue()
        self.as_text = as_text
        
        atexit.register(self.cleanup)
        
        self.initialize_driver(additional_opts=additional_opts)
        
        

    def initialize_driver(self, additional_opts):
        """Initialize the WebDriver."""
        options = uc.ChromeOptions()
        if self._headless:
            options.add_argument("--headless=new")
        
        for key, value in additional_opts.items():
            options.add_argument(f"--{key}={value}")
            
        options.add_argument("--disable-gpu")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-blink-features=AutomationControlled")
        #options.add_argument("--auto-open-devtools-for-tabs")
        #options.add_experimental_option("excludeSwitches", ["enable-automation"])
        #options.add_experimental_option("useAutomationExtension", False)


        # Set up WebDriver using undetected-chromedriver
        self._driver = uc.Chrome(driver_executable_path=ChromeDriverManager().install(), options=options)
        self._driver.set_page_load_timeout(30)  # Increase page load timeout
        self._driver.implicitly_wait(10)  # Increase implicit wait time
        
        # Execute CDP commands to modify navigator properties
        # self._driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
        #     "source": """
        #     Object.defineProperty(navigator, 'webdriver', {
        #         get: () => undefined
        #     });
        #     """
        # })

        # Start a worker thread to process the queue
        self._worker_thread = threading.Thread(target=self.process_queue)
        self._worker_thread.daemon = True  # Daemonize the thread to exit with the program
        self._worker_thread.start()
    
    def set_type(self, as_text: bool = True):
        self.as_text = as_text

    def process_queue(self):
        """Process the queue to fetch web pages."""
        while True:
            url, result_queue = self._task_queue.get()
            try:
                result = self.fetch_page(url)
            except Exception as e:
                result = f"Error fetching the webpage: {str(e)}"
            result_queue.put(result)
            self._task_queue.task_done()

    def fetch_page(self, url: str) -> str:
        """Fetch the content from a webpage URL."""
        print("Fetching URL:", url)

        for attempt in range(3):  # Retry up to 3 times
            try:
                # Open the webpage
                self._driver.get(url)
                time.sleep(random.uniform(1, 5))  # Random sleep to reduce load

                if not self.as_text:
                    return self._driver.page_source
                
                # Fetch the page content using the updated method
                page_text = self._driver.find_element(By.TAG_NAME, "body").text

                return page_text.strip()

            except Exception as e:
                if attempt < 2:  # Retry logic
                    time.sleep(5)  # Wait before retrying
                    continue
                else:
                    return f"Error fetching the webpage: {str(e)}"

    def run(self, url: str) -> str:
        """Fetch the text content from a webpage URL."""
        return self.fetch_page(url)
    
    def _run(self, url: str) -> str:
        """Add a fetch task to the queue and return the result."""
        result_queue = Queue()
        self._task_queue.put((url, result_queue))
        return result_queue.get()  # Block until result is available
    
    
    def cleanup(self):
        """Clean up the WebDriver."""
        if self._driver:
            self._driver.quit()
            
            
            