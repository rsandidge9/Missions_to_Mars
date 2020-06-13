# Dependencies
from bs4 import BeautifulSoup
import requests
import pymongo
import urllib
import urllib.request
from splinter import Browser
import pandas as pd
import re
import time


def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {"executable_path": "chromedriver.exe"}
    return Browser("chrome", **executable_path, headless=False)


def scrape():
    browser = init_browser()

    mars_data = {}

    title, thread = mars_news(browser)
    mars_data["title"] = title
    mars_data["thread"] = thread
    mars_data["featured_image_url"] = mars_feature_image(browser)

    mars_data['mars_weather'] = mars_weather(browser)
    mars_data['mars_facts'] = mars_facts(browser)

    mars_data["mars_hemispheres"] = mars_hemispheres(browser)
    browser.quit()
    return mars_data


def mars_news(browser):
    # URL of page to be scraped
    nasa_url = 'https://mars.nasa.gov/news/'
    #nasa_page = urllib.request.urlopen (nasa_url)
    browser.visit(nasa_url)
    browser.is_element_present_by_css('ul.item_list li.slide', wait_time=5)
    # nasa_soup
    # Examine the results, then determine element that contains sought info
    # results are returned as an iterable list
    html = browser.html
    nasa_soup = BeautifulSoup(html, 'html.parser')
    # pull news data
    nasa_results = nasa_soup.select_one("ul.item_list li.slide")
    # pull news data
    title = nasa_results.find('div', class_='content_title').get_text()
    thread = nasa_results.find('div', class_='article_teaser_body').get_text()

    return title, thread


def mars_feature_image(browser):
    # URL of page to be scraped
    space_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    # Space page
    space_page = urllib.request.urlopen(space_url)
    # space_soup
    space_soup = BeautifulSoup(space_page, 'html.parser')
    space_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    # visit browser
    browser.visit(space_url)
    # loacte image
    image = browser.find_by_id('full_image')
    # click on image
    image.click()
    # wait time
    browser.is_element_present_by_text("more info", wait_time=1)
    # locate more info linl
    more_info_link = browser.links.find_by_partial_text("more info")
    # click on link
    more_info_link.click()
    space_html = browser.html
    space_soup = BeautifulSoup(space_html, 'html.parser')
    # get image
    feature_image = space_soup.select_one("figure.lede a img").get("src")
    # create URL
    featured_image_url = 'https://www.jpl.nasa.gov' + feature_image

    return featured_image_url


def mars_weather(browser):
    executable_path = {'executable_path': 'chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=False)
    weather_url = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(weather_url)
    # https://docs.python.org/3.0/library/time.html

    # weather_page = urllib.request.urlopen (weather_url)
    weather_page = browser.html
    weather_soup = BeautifulSoup(weather_page, 'html.parser')
    # weather_soup
    # weather_results = weather_soup.find(
    # 'div', attrs={"class": "tweet", "data-name": "Mars Weather"})
    pattern = re.compile(r"sol")
    time.sleep(2)
    # pattern
    weather = weather_soup.find('span', text=pattern).text
    # mars_weather

    return weather


def mars_facts(browser):
    # page to scrape
    facts_url = 'https://space-facts.com/mars/'
    #facts_page = urllib.request.urlopen(facts_url)
    # time.sleep(5)
    # beautiful soup
    #facts_soup = BeautifulSoup(facts_page, 'html.parser')
    # facts_soup
    # get results
    #facts_results = facts_soup.find_all('tr', class_='row')
    # facts_results
    # create dataframe
    mars_df = pd.read_html(facts_url)[0]
    # print(mars_df)
    mars_df.columns = ["Desc.", "Value"]
    mars_df.set_index("Desc.", inplace=True)
    # mars_df

    return mars_df.to_html()


def mars_hemispheres(browser):

    hemisphere_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(hemisphere_url)
    time.sleep(5)

    html = browser.html
    astro_soup = BeautifulSoup(html, 'html.parser')

    hemisphere_names = []

    # Search for the names of all four hemispheres
    results = astro_soup.find_all('div', class_="collapsible results")
    hemispheres = results[0].find_all('h3')

    # # Get text and store in list
    for i, name in enumerate(hemispheres):
        mars_dict = {}
        mars_dict["title"] = name.text
        browser.find_by_css('a.product-item h3')[i].click()
        sample = browser.links.find_by_text("Sample").first
        mars_dict["url"] = sample['href']
        hemisphere_names.append(mars_dict)
        browser.back()

    return hemispheres


# print(scrape())
