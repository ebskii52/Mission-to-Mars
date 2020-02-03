#%%
# Import Splinter and BeautifulSoup
from splinter import Browser
from bs4 import BeautifulSoup
import pandas as pd
import datetime as dt
# Set the executable path and initialize the chrome browser in splinter
executable_path = {'executable_path': './chromedriver'}
# Initiate headless driver for deployment
browser = Browser("chrome", executable_path="chromedriver", headless=True)

#%%
def scrape_all():
    news_title, news_paragraph = mars_news(browser)
    # Run all scraping functions and store results in dictionary
    SphereImages = []
    SphereTitles = []

    imageData = image_mars(browser)
    for keys in imageData:
        SphereTitles.append(keys)
        SphereImages.append(imageData[keys])


    data = {
    "news_title": news_title,
    "news_paragraph": news_paragraph,
    "featured_image": featured_image(browser),
    "facts": mars_facts(),
    "SphereTitles": SphereTitles,
    "SphereImages": SphereImages,
    "last_modified": dt.datetime.now()
    }
    return(data)

# %%
def mars_news(browser):
    try:
        #Visit the mars nasa news site
        url = 'https://mars.nasa.gov/news/'
        browser.visit(url)
        # Optional delay for loading the page
        browser.is_element_present_by_css("ul.item_list li.slide", wait_time=1)
        html = browser.html
        news_soup = BeautifulSoup(html, 'html.parser')
        slide_elem = news_soup.select_one('ul.item_list li.slide')
        # Use the parent element to find the first <a> tag and save it as `news_title`
        news_title = slide_elem.find("div", class_='content_title').get_text()
        # Use the parent element to find the paragraph text
        news_p = slide_elem.find('div', class_="article_teaser_body").get_text()
        return (news_title, news_p)

    except AttributeError:
        return None, None

# %%
def featured_image(browser):
    try:
        url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
        browser.visit(url)
        # Find and click the full image button
        full_image_elem = browser.find_by_id('full_image')
        full_image_elem.click()
        # Find the more info button and click that
        browser.is_element_present_by_text('more info', wait_time=1)
        more_info_elem = browser.find_link_by_partial_text('more info')
        more_info_elem.click()
        # Parse the resulting html with soup
        html = browser.html
        img_soup = BeautifulSoup(html, 'html.parser')
        # Find the relative image url
        img_url_rel = img_soup.select_one('figure.lede a img').get("src")
        # Use the base URL to create an absolute URL
        img_url = f'https://www.jpl.nasa.gov{img_url_rel}'
        return(img_url)       

    except AttributeError:
        return None
    
#%%
def mars_facts():
    # Add try/except for error handling
    try:
        # Use 'read_html' to scrape the facts table into a dataframe
        df = pd.read_html('http://space-facts.com/mars/')[0]
        # Assign columns and set index of dataframe
        df.columns=['Description', 'Mars']
        df.set_index('Description', inplace=True)
        # Convert dataframe into HTML format, add bootstrap
        return(df.to_html())

    except BaseException:
        return None
   

#%%

def image_mars(browser):
    # Visit URLs
    baseURL = 'https://astrogeology.usgs.gov'
    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)

    # Parse the resulting html with soup
    html = browser.html
    parsedHTML = BeautifulSoup(html, 'html.parser')
    allATags = parsedHTML.find_all('a')

    hrefList = []
    img_urls = {}

    for ls in allATags:
        if '_enhanced' in ls['href']:
            hrefList.append(ls['href'])

    for links in hrefList:
        imgurl =  baseURL + links
        browser.visit(imgurl)
        imghtml = browser.html
        img_zp = BeautifulSoup(imghtml, 'html.parser')
        img_url_rel = img_zp.select_one('div.wide-image-wrapper img.wide-image').get("src")
        mars_img_url = f'https://astrogeology.usgs.gov{img_url_rel}'
        title = img_zp.find('h2', class_="title").get_text()
        img_urls[title] = mars_img_url

    return(img_urls)


# %%
