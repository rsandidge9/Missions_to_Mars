{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": 1,
   "metadata": {},
   "outputs": [],
   "source": [
    "from splinter import Browser\n",
    "from bs4 import BeautifulSoup as bs\n",
    "import time\n",
    "import pandas as pd"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 2,
   "metadata": {},
   "outputs": [],
   "source": [
    "def init_browser():\n",
    "    # @NOTE: Replace the path with your actual path to the chromedriver\n",
    "    executable_path = {\"executable_path\": \"/usr/local/bin/chromedriver\"}\n",
    "    return Browser(\"chrome\", **executable_path, headless=False)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 3,
   "metadata": {},
   "outputs": [],
   "source": [
    "def scrape():\n",
    "    browser = init_browser()\n",
    "    \n",
    "# Visit Mars site for news\n",
    "    browser.visit('https://mars.nasa.gov/news/')\n",
    "    time.sleep(1)\n",
    "\n",
    "# Scrape page into Soup\n",
    "    html = browser.html\n",
    "    soup = bs(html, \"html.parser\")\n",
    "    \n",
    "    #pull news data\n",
    "    title = result.find('div', class_='content_title').get_text()\n",
    "    thread = result.find('div', class_='rollover_description_inner').get_text()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 4,
   "metadata": {},
   "outputs": [],
   "source": [
    "#Visit JPL site for Mars image\n",
    "def scrape():\n",
    "    browser = init_browser()\n",
    "#visit web page    \n",
    "    browser.visit('https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars')\n",
    "# wait time\n",
    "    time.sleep(1)\n",
    "# click to get image\n",
    "    image=browser.find_by_id('full_image')\n",
    "    image.click()\n",
    "    \n",
    "    browser.is_element_present_by_text(\"more info\", wait_time=1)\n",
    "    more_info_link= browser.find_link_by_partial_text(\"more info\")\n",
    "    more_info_link.click()\n",
    "# soup to read page    \n",
    "    space_html = browser.html\n",
    "    space_soup = BeautifulSoup(space_html, 'html.parser')\n",
    "    \n",
    "    feature_image=space_soup.select_one(\"figure.lede a img\").get(\"src\")\n",
    "\n",
    "#connect URL with featured image   \n",
    "    featured_image_url = 'https://www.jpl.nasa.gov' + feature_image \n",
    "    "
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 5,
   "metadata": {},
   "outputs": [],
   "source": [
    "#Visit twitter site for Mars weather\n",
    "def scrape():\n",
    "    browser = init_browser()\n",
    "#visit web page  \n",
    "    browser.visit('https://twitter.com/marswxreport?lang=en')\n",
    "    \n",
    "    time.sleep(1)\n",
    "    \n",
    "# Scrape page\n",
    "    weather_page = browser.html\n",
    "    weather_soup=bs.BeautifulSoup(weather_page, 'html.parser')\n",
    "   \n",
    "    weather_results = weather_soup.find('div', attrs={\"class\": \"tweet\", \"data-name\": \"Mars Weather\"})\n",
    "    \n",
    "    \n",
    "    pattern = re.compile(r\"sol\")\n",
    "    mars_weather = weather_soup.find('span', text=pattern).text"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 6,
   "metadata": {},
   "outputs": [],
   "source": [
    "#Visit site for Mars facts\n",
    "def scrape():\n",
    "    browser = init_browser()\n",
    "#visit web page  \n",
    "    browser.visit('https://space-facts.com/mars/')\n",
    "    \n",
    "    time.sleep(1)\n",
    "    \n",
    "    facts_page = urllib.request.urlopen (facts_url)\n",
    "    facts_soup=bs.BeautifulSoup(facts_page, 'html.parser')\n",
    "    \n",
    "    facts_results = facts_soup.find_all('tr', class_='row')\n",
    "\n",
    "    mars_df = pd.read_html(\"https://space-facts.com/mars/\")[0]\n",
    "    #print(mars_df)\n",
    "    mars_df.columns=[\"Desc.\", \"Value\"]\n",
    "    mars_df.set_index(\"Desc.\", inplace=True)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 7,
   "metadata": {},
   "outputs": [],
   "source": [
    "#Visit site for hemisphere info\n",
    "def scrape():\n",
    "    browser = init_browser()\n",
    "#visit web page  \n",
    "    browser.visit('https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars')\n",
    "    \n",
    "    time.sleep(1)\n",
    "    \n",
    "    html = browser.html\n",
    "    astro_soup = BeautifulSoup(html, 'html.parser')\n",
    "\n",
    "    hemisphere_names = []\n",
    "\n",
    "# Search for the names of all four hemispheres\n",
    "    results = astro_soup.find_all('div', class_=\"collapsible results\")\n",
    "    hemispheres = results[0].find_all('h3')\n",
    "\n",
    "# # Get text and store in list\n",
    "    for i,name in enumerate(hemispheres):\n",
    "        mars_dict={}\n",
    "        mars_dict[\"title\"]= name.text\n",
    "        browser.find_by_css('a.product-item h3')[i].click()\n",
    "        sample = browser.find_link_by_text(\"Sample\").first\n",
    "        mars_dict[\"url\"]= sample['href']\n",
    "        hemisphere_names.append(mars_dict)\n",
    "        browser.back()\n",
    "    "
   ]
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.7.4"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 2
}
