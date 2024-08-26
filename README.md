## Undetected Browser Tool

### Introduction

The Undetected Browser Tool is an AI Agent tool to simplify the process of accessing individual web pages that are protected by bot detection systems.

e.g. Cloudflare and similar services. 

This tool is designed to facilitate access to publicly available data on a single-page basis for AI Agents. 
This is not a hacking tool, or a paywall bypass tool, nor guaranteed in all situations. 

It is not intended for web scraping or crawling purposes

Various configurations in WAF and security services may still block access, and the tool can still be detected through methods like the Chrome Developer Protocol (CDP) in JavaScript.


It works by creating a headless browser instance and navigating to a page, which inherently makes it slower and unsuitable for high-volume or automated data extraction.

The main aim is to make it easier for AI agents to access web pages that might otherwise be challenging due to bot protection. 

It is built as a LangChain tool using Selenium and the [undetected-chromedriver](https://github.com/ultrafunkamsterdam/undetected-chromedriver) project.


- [Undetected Browser Tool](#undetected-browser-tool)
  - [Introduction](#introduction)
  - [Installation](#installation)
  - [Usage](#usage)
  - [Example with CrewAI](#example-with-crewai)
  - [Tips for being undetected](#tips-for-being-undetected)
  - [Ethics](#ethics)


### Installation

```
pip install -U undetected-browser-tool
```

### Usage 
We use this in [langchain agents](https://python.langchain.com/) or in [CrewAI Agents](https://docs.crewai.com/core-concepts/Agents/#what-is-an-agent)


```python
from undetected_browser_tool import UndetectedBrowserTool

# for a headless browser
browser = UndetectedBrowserTool(headless=True) 

# or useful for debugging
browser = UndetectedBrowserTool(headless=False) 


# or using a proxy, change http to https or socks5 to suit your proxy settings
opts = {"proxy-server" : "http://xxx.xxx.xxx:port"}
browser = UndetectedBrowserTool(headless=False, additional_opts=opts) 

# fetch a page
page = browser.run("https://nowsecure.nl/")
```

### Example with CrewAI
Untested code, written as an example for usage with CrewAI
Be aware that langchain and Crew are in constant development, so these interfaces may change.


```python
from crewai import Agent, Task, Crew
from undetected_browser_tool import UndetectedBrowserTool
from langchain_community.tools import DuckDuckGoSearchResults

browser = UndetectedBrowserTool(headless=True)
search_engine = DuckDuckGoSearchResults()

researcher = Agent(
            role="Researcher",
            goal="A document reviewing the top 5 solutions in {topic}",
            backstory="You are a research analyst tasked with reviewing software for an IT firm to help them make buying decisions",
            tools=[search_engine, browser],
)

report_writer = Agent(
            role="Report writer",
            goal="A executive review of the top 5 solutions in {topic}"
            backstory="You are a report writer for an IT firm, you excel at writing summaries and detailed reports for executives in an IT firm", 
            
)

research_task = Task(
            expected_output="A list of pros and cons, features, customer reviews and pricing of the top 5 solutions in {topic}",
            description="By using a search engine and Capterra, G2, Gartner write a review of the top 5 solutions in {topic}, include the source link for each item you find."
            tools=[search_engine, browser],
            agent=researcher,
)

report_task = Task(
            expected_output="An executive style report, with a summary, detailed information and a recommendation for selecting a solution in {topic}"
            description="Based upon the research provided, write an executive summary, detailed report, and a recommendation on the software selection. The report should have a table of features, pros / cons, and pricing options."
            output_file="report.md",
            context={research_task}
)

crew = Crew(agents=[researcher, report_writer], tasks=[research_task, report_task])

crew.kickoff(inputs={"topic" : "BI Reporting Platforms"})

```


### Tips for being undetected
This is not a 100%, it's hard to be 100% but it's a good start.
* Don't go through a data center, those IPs are easy to track and block.
* Use proxies, and I recommend residential proxies. Tor networks are easily blocked. 
* Switch proxies frequently
* Don't crawl the website, use a search service to try and pinpoint the page you need.

Every time a confirm you are a human page pops up, about 50% of the users just drop out, so companies who are dependent on traffic try to avoid that. Meaning as long as you're not doing something silly you're usually going to be ok.



### Ethics
The use of automation tools to interact with websites is a nuanced topic that involves balancing access to information with respect for publishers' rights. Publishers have the right to protect their content and manage how it is accessed. They often allow search engines to index their data so it can be discovered by the general public, while also setting guidelines to regulate how their information is used.

If your intent is to occasionally access content to obtain information and properly reference the source, this tool can help streamline your workflow by automating repetitive tasks, thus saving time and effort.

However, if your goal is to scrape large amounts of data from a website, this project is not intended for that purpose. Engaging in large-scale scraping can violate the terms of service of many websites, infringe on intellectual property rights, and potentially cause harm to the website's infrastructure. 

Always ensure that your use of automation tools is ethical and complies with the website's terms of service. Respect the rights of content owners and use automation responsibly.