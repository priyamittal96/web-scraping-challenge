from bs4 import BeautifulSoup as bs
from splinter import Browser
from pprint import pprint
from webdriver_manager.chrome import ChromeDriverManager
import pymongo
import pandas as pd
import os
import requests


def scrape_all():
    # excutable_path 
    executable_path = { "executable_path": ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)
    news_title, news_paragraph = mars_news(browser) 

    data = {
     "new_title": news_title,
     "news_paragraph": news_paragraph,
     "featured_image": featured_image(browser),
     "facts": mars_facts(),
     "hemispheres": hemispheres(browser)
        
    }
    browser.quit()
    return data


# NASA Mars News
def mars_news(browser):
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)
    html = browser.html
    soup = bs(html, 'html.parser')
    
    try:
        slides = soup.find_all('li', class_='slide')
        title = slides[0].find('div', class_ = 'content_title')
        news_title = title.text.strip()
        print(news_title)
        body = slides[0].find('div', class_= 'article_teaser_body')
        news_paragraph = body.text.strip()
        print(news_paragraph)
    except: 
        return None, None
    
    return news_title, news_paragraph


# JPL Mars Space Images - Featured Image
def featured_image(browser):
    url = 'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/index.html'
    browser.visit(url)
    html = browser.html
    soup = bs(html, 'html.parser')

    try:
        images = soup.find_all('img', class_='headerimage fade-in')
        print(images)
        for image in images:
            pic = image['src']
    except: 
        return None

    featured_image_url = f'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/{pic}'
    return featured_image_url

              
# Mars Facts
def mars_facts():
    mars_facts_url = 'https://space-facts.com/mars/'
    table = pd.read_html(mars_facts_url)
    df = table[0]
    df.columns = ["Facts","Values"]
    df.set_index(["Facts"], inplace= True)

    return df.to_html(classes="table table-striped")


# Mars Hemispheres
headings = []
images = []
hemisphere_image_urls = []

def hemispheres(browser):
    url = ('https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars')
    response = requests.get(url)
    soup = bs(response.text, 'html.parser')
              
    links = soup.find_all('a',class_='itemLink product-item')
    
    try:
        hemispheres = [link['href'] for link in links]
        hemisphere_links = [f'https://astrogeology.usgs.gov{hemisphere}' for hemisphere in hemispheres]
        executable_path = {'executable_path': ChromeDriverManager().install()}
        browser = Browser('chrome', **executable_path, headless=False)
        for link in hemisphere_links:
            url = link
            browser.visit(url)
            html = browser.html
            soup = bs(html, 'html.parser')
            title = soup.find('h2',class_='title').text
            headings.append(title)
            src_links = soup.find_all('img',class_='wide-image')
            for src_link in src_links:
                imgs = src_link['src']
                img_links = f'https://astrogeology.usgs.gov{imgs}'
                images.append(img_links)
            hemisphere_image = {'title': title, 'img_url': img_links}
            hemisphere_image_urls.append(hemisphere_image)              
    except:
        return None
    
    return hemisphere_image_urls


