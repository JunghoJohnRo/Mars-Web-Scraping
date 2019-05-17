from splinter import Browser
from bs4 import BeautifulSoup
import requests
import pandas as pd
import time

def init_browser():
    executable_path = {"executable_path": "/usr/local/bin/chromedriver"}
    return Browser("chrome", **executable_path, headless=False)

def scrape_info():
    # Initializing Browser
    browser = init_browser()

    # Dictionary to Store all the Data
    mars_data = {}

    # Latest Mars News
    url = 'https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'
    browser.visit(url)

    time.sleep(3)

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    results = soup.find("div", class_="list_text")
    news_title = results.find("div", class_="content_title").text
    news_p = results.find("div", class_="article_teaser_body").text

    mars_data["news_title"] = news_title
    mars_data["news_p"] = news_p

    # JPL Mars Space Images - Featured Image
    image_url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(image_url)

    time.sleep(5)

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    image_results = soup.find("article", class_="carousel_item")['style']
    s = image_results.split("'")[1]

    featured_image_url = f'https://www.jpl.nasa.gov{s}'

    mars_data["featured_image_url"] = featured_image_url

    # Mars Weather
    weather_url = "https://twitter.com/marswxreport?lang=en"
    browser.visit(weather_url)

    time.sleep(3)

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    mars_weather = soup.find("p", class_="TweetTextSize TweetTextSize--normal js-tweet-text tweet-text").text[8:159]

    mars_data["mars_weather"] = mars_weather

    # Mars Facts
    facts_url = "https://space-facts.com/mars/"

    tables = pd.read_html(facts_url)

    time.sleep(3)

    df = tables[0]
    df.columns = ['Description','Value']
    df = df.set_index('Description')

    marsfacts_html_table = df.to_html()
    marsfacts_html_table = marsfacts_html_table.replace('\n', '')
    
    mars_data["marsfacts_html_table"] = marsfacts_html_table

    # Mars Hemispheres
    mh_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(mh_url)

    time.sleep(3)

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    images = soup.find('div', class_='collapsible results')

    hemisphere_image_urls = []

    for x in range(len(images.find_all("div", class_="item"))):
        img = browser.find_by_tag('h3')
        img[x].click()
        html = browser.html
        soup = BeautifulSoup(html, 'html.parser')
        title = soup.find("h2", class_="title").text
        div = soup.find("div", class_="downloads")
        for li in div:
            link = div.find('a')
            url = link.attrs['href']
            hemisphere_dict = {
                'title' : title,
                'img_url' : url
                }
        hemisphere_image_urls.append(hemisphere_dict)
        browser.back()

    mars_data["hemisphere_image_urls"] = hemisphere_image_urls

    # Close the browser after scraping
    browser.quit()

    return mars_data

    