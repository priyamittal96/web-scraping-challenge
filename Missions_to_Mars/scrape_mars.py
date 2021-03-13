from bs4 import BeautifulSoup as bs
from splinter import Browser
from pprint import pprint
from webdriver_manager.chrome import ChromeDriverManager
import pymongo
import pandas as pd
import os
import requests


# In[147]:


url = 'https://mars.nasa.gov/news/'

executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=False)
browser.visit(url)
html = browser.html
soup = bs(html, 'html.parser')


# In[59]:


print(soup.prettify())


# # NASA Mars News

# In[63]:


slides = soup.find_all('li', class_='slide')


# In[75]:


title = slides[0].find('div', class_ = 'content_title')
news_title = title.text.strip()
body = slides[0].find('div', class_= 'article_teaser_body')
news_p = body.text.strip()

print(news_title)
print(news_p)


# In[148]:


browser.quit()


# # JPL Mars Space Images - Featured Image

# In[78]:


url = 'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/index.html'

executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=False)
browser.visit(url)
html = browser.html
soup = bs(html, 'html.parser')


# In[115]:


images = soup.find_all('img', class_='headerimage fade-in')
print(images)


# In[125]:


for image in images:
    pic = image['src']
    
print(pic)


# In[127]:


featured_image_url = f'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/{pic}'
print(featured_image_url)


# In[128]:


browser.quit()


# # Mars Facts

# In[129]:


mars_facts_url = 'https://space-facts.com/mars/'
table = pd.read_html(mars_facts_url)


# In[130]:


table[0]


# In[135]:


df = table[0]
df.columns = ["Facts","Values"]
df.set_index(["Facts"])
df


# In[139]:


faces_html = df.to_html()
faces_html = faces_html.replace("\n", "")
faces_html


# # Mars Hemispheres

# In[13]:


hemisphere_image_urls = []


# In[16]:


url = ('https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars')

response = requests.get(url)
soup = bs(response.text, 'html.parser')


# In[17]:


print(soup.prettify())


# In[18]:


links = soup.find_all('a',class_='itemLink product-item')
print(links)


# In[29]:


hemispheres = [link['href'] for link in links]
hemispheres


# In[35]:


hemisphere_links = [f'https://astrogeology.usgs.gov{hemisphere}' for hemisphere in hemispheres]
hemisphere_links


# In[36]:


executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=False)


# In[37]:


headings = []
images = []
hemisphere_image_urls = []

for link in hemisphere_links:
    url = link
    browser.visit(url)
    html = browser.html
    soup = bs(html, 'html.parser')
    title = soup.find('h2',class_='title').text
    headings.append(title)
#     print(title)
    src_links = soup.find_all('img',class_='wide-image')
    for src_link in src_links:
        imgs = src_link['src']
        img_links = f'https://astrogeology.usgs.gov{imgs}'
        images.append(img_links)
#         print(img_links)
    hemisphere_image = {'title': title, 'img_url': img_links}
    hemisphere_image_urls.append(hemisphere_image)
browser.quit()


# In[38]:


print(hemisphere_image_urls)

