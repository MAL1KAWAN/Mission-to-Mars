from splinter import Browser
from bs4 import BeautifulSoup as bs
import requests
import pandas as pd
import io
import time
from selenium import webdriver

def init_browser():
    executable_path = {'executable_path': 'C:/Users/Bashira/Documents/Python Scripts/Resources/chromedriver'}
    return Browser('chrome', **executable_path, headless=False)

def scrape():
    browser = init_browser()
    mars_facts_data = {}

    #scrapping latest news about mars from nasa
    url = 'https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest/'
    browser.visit(url)
    time.sleep(2)

    html = browser.html
    soup = bs(html, 'html.parser')
    title = soup.find('div', class_="content_title").text
    para = soup.find('div', class_="article_teaser_body").text
    #date = soup.find('div', class_="list_date").text 
    mars_facts_data['news_title'] = title
    mars_facts_data['news_paragraph'] = para

    #Mars Featured Image
    mars_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(mars_url)
    time.sleep(2)
    # create a xpath
    xpath = "//*[@id='full_image']"
    image = browser.find_by_xpath(xpath)
    results = image[0]
    results.click()
    time.sleep(2)
    # 2nd xpath
    second_path = "//*[@id='fancybox-lock']/div/div[2]/div/div[1]/a[2]"
    info_image = browser.find_by_xpath(second_path)
    info_image.click()
    time.sleep(2)
    # getting large size image
    mars_html = browser.html
    image_soup = bs(mars_html, "html.parser")
    img_url = image_soup.find('img', class_ = 'main_image')['src']
    featured_image_url = "https://www.jpl.nasa.gov"+img_url
    mars_facts_data["featured_image"] = featured_image_url

    # scrape the latest Mars weather tweet from the page.
    twitter_url = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(twitter_url)
    time.sleep(2)
    twitter_html = browser.html
    tweet_soup = bs(twitter_html, 'html.parser')
    tweet = tweet_soup.find_all('p', class_='TweetTextSize TweetTextSize--normal js-tweet-text tweet-text')
    for weather in tweet:
        if weather.text.strip().startswith("InSight sol"):
                mars_weather = weather.text.strip()
    mars_facts_data["mars_weather"] = mars_weather    
    
    # Mars table
    space_url = 'https://space-facts.com/mars/'
    browser.visit(space_url)
    time.sleep(2)
    df = pd.read_html(space_url)
    mars_info = df[0]
    mars_info.columns = ["description", "value"]
    mars_info.set_index('description', inplace=True)
    mars_table = mars_info.to_html()
    mars_table = mars_table.replace("\n", "")
    mars_facts_data["mars_facts_table"] = mars_table

    # Cerberus-Hemisphere-image-url
    astro_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(astro_url)
    hemisphere_img_urls = []

    # create 2 xpaths

    cer_first_xpath = "//*[@id='product-section']/div[2]/div[1]/a/img"
    small_image = browser.find_by_xpath(cer_first_xpath)
    small_image.click()
    time.sleep(2)
    cer_second_xpath = "//*[@id='wide-image-toggle']"
    open_image = browser.find_by_xpath(cer_second_xpath)
    open_image.click()
    time.sleep(2)
    cer_html = browser.html
    image_soup = bs(cer_html, "html.parser")
    img_url = image_soup.find('img', class_ = 'wide-image')['src']
    cerberus_img_url = "https://astrogeology.usgs.gov"+img_url
    cerberus_title = image_soup.find('h2',class_='title').text
    cerberus_dict = {'title':cerberus_title, 'img_url': cerberus_img_url}
    hemisphere_img_urls.append(cerberus_dict)

    # Schiaparelli-Hemisphere-image-url
    sch_astro_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(sch_astro_url)
    sch_first_xpath = "//*[@id='product-section']/div[2]/div[2]/a/img"
    small_image = browser.find_by_xpath(sch_first_xpath)
    small_image.click()
    time.sleep(2)
    sch_second_xpath = "//*[@id='wide-image-toggle']"
    open_image = browser.find_by_xpath(sch_second_xpath)
    open_image.click()
    time.sleep(2)
    sch_html = browser.html
    image_soup = bs(sch_html, "html.parser")
    img_url = image_soup.find('img', class_ = 'wide-image')['src']
    schiaparelli_img_url = "https://astrogeology.usgs.gov"+img_url
    schiaparelli_title = image_soup.find('h2',class_='title').text
    schiaparelli_dict = {'title': schiaparelli_title, 'img_url': schiaparelli_img_url}
    hemisphere_img_urls.append(schiaparelli_dict)

    # Syrtis Major Hemisphere 
    syr_astro_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(syr_astro_url)
    syr_first_xpath = "//*[@id='product-section']/div[2]/div[3]/a/img"
    small_image = browser.find_by_xpath(syr_first_xpath)
    small_image.click()
    syr_second_xpath = "//*[@id='wide-image-toggle']"
    open_image = browser.find_by_xpath(syr_second_xpath)
    open_image.click()
    syr_html = browser.html
    image_soup = bs(syr_html, "html.parser")
    img_url = image_soup.find('img', class_ = 'wide-image')['src']
    syrtis_img_url = "https://astrogeology.usgs.gov"+img_url
    syrtis_title = image_soup.find('h2',class_='title').text
    syrtis_dict = {'title': syrtis_title, 'img_url': syrtis_img_url}
    hemisphere_img_urls.append(syrtis_dict) 

    # Valles Marineris Hemisphere 
    val_astro_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(val_astro_url)
    val_first_xpath = "//*[@id='product-section']/div[2]/div[4]/a/img"
    small_image = browser.find_by_xpath(val_first_xpath)
    small_image.click()
    time.sleep(2) 
    val_second_xpath = "//*[@id='wide-image-toggle']"
    open_image = browser.find_by_xpath(val_second_xpath)
    open_image.click()
    time.sleep(2)
    val_html = browser.html
    image_soup = bs(val_html, "html.parser")
    img_url = image_soup.find('img', class_ = 'wide-image')['src']
    valles_img_url = "https://astrogeology.usgs.gov"+img_url
    valles_title = image_soup.find('h2',class_='title').text
    valles_dict = {'title': valles_title, 'img_url': valles_img_url}
    hemisphere_img_urls.append(valles_dict)

    mars_facts_data["hemisphere_img_url"] = hemisphere_img_urls

    
    
    return mars_facts_data
    