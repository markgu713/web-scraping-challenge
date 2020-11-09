# Import dependencies
import pandas as pd
from bs4 import BeautifulSoup as bs
import requests
import splinter
from splinter import Browser
from selenium import webdriver

def scrape():
    scrapedDict = {}
# Mars News
    # load chrome webdriver
    url = "https://mars.nasa.gov/news/"
    driver = webdriver.Chrome()
    driver.get(url)
    # load page using beautiful soup
    soup = bs(driver.page_source, "lxml")
    # Collect the latest News Title
    content_title = soup.find_all('div', class_='content_title')
    news_title = content_title[1].text
    # Collect Paragraph Text
    paragraph = soup.find_all('div', class_='article_teaser_body')
    news_p = paragraph[0].text

    scrapedDict['news_title'] = news_title
    scrapedDict['news_p'] = news_p
# JPL Mars Space Images
    # import image url
    image_url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    # load chrome webdriver
    executable_path = {'executable_path': 'chromedriver'}
    browser = Browser('chrome', **executable_path, headless=False)
    browser.visit(image_url)
    html = browser.html
    # use beautiful soup to parse html
    soup = bs(html, 'html.parser')
    # find the url for the first image
    images = soup.find_all('div', class_='img')
    featured_image_url = "https://www.jpl.nasa.gov" + images[0].img['src']

    scrapedDict['featured_image_url'] = featured_image_url
# Mars Fact
    # import mars fact url
    mar_facts_url = "https://space-facts.com/mars/"
    # use panda to read html
    tables = pd.read_html(mar_facts_url)
    # return html table string
    html_result = tables[0].to_html()

    scrapedDict['html_string'] = html_result
# Mars Hemispheres
    # load Mars Hemispheres URL
    mar_hemi_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    # load chrome driver
    driver = webdriver.Chrome()
    executable_path = {'executable_path': 'chromedriver'}
    browser = Browser('chrome', **executable_path, headless=False)
    driver.get(mar_hemi_url)
    # use beautiful soup to load the page
    soup = bs(driver.page_source, "lxml")
    # create image url array
    images_urls = []
    with Browser('chrome', **executable_path) as browser:
        for image_title in [h3.text for h3 in soup.find_all('h3')]:
            img = {}
            # visit the hemisphere url
            browser.visit(mar_hemi_url)
            # click on each image link
            browser.click_link_by_partial_text(image_title)
            # find the image by "Sample"
            itag = browser.find_by_text('Sample')
            # import in the img dict
            img['title'] = image_title
            img['url'] = itag['href']
            # append in images_urls array
            images_urls.append(img)
    scrapedDict['images_urls'] = images_urls

    print(scrapedDict)
    return scrapedDict

scrape()