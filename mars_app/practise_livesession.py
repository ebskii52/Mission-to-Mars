#%%
# Import Splinter and BeautifulSoup
from splinter import Browser
from bs4 import BeautifulSoup as soup
import pandas as pd
import datetime as dt

# Set the executable path and initialize the chrome browser in splinter
executable_path = {'executable_path': './chromedriver'}
# Initiate headless driver for deployment
browser = Browser("chrome", executable_path="chromedriver", headless=True)
# Convert the browser html to a soup object and then quit the browser
html = browser.html
news_soup = soup(html, 'html.parser')

#%%
def scrape_all():
    news_title, news_paragraph = mars_news(browser)
    # Run all scraping functions and store results in dictionary
    data = {
    "news_title": news_title,
    "news_paragraph": news_paragraph,
    "featured_image": featured_image(browser),
    "facts": mars_facts(),
    "last_modified": dt.datetime.now()
    }
    return(data)

# %%
def mars_news(browser):
    try:
        # Visit the mars nasa news site
        url = 'https://mars.nasa.gov/news/'
        browser.visit(url)
        # Optional delay for loading the page
        browser.is_element_present_by_css("ul.item_list li.slide", wait_time=1)
        slide_elem = news_soup.select_one('ul.item_list li.slide')
        # Use the parent element to find the first <a> tag and save it as `news_title`
        news_title = slide_elem.find("div", class_='content_title').get_text()
        # Use the parent element to find the paragraph text
        news_p = slide_elem.find('div', class_="article_teaser_body").get_text()

        return news_title, news_p
    
    except AttributeError:
        return None, None

#%%
news_title, news_paragraph = mars_news(browser)
news_paragraph

# %%
# Visit URL
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
img_url_rel
    
#%%
img_url_rel
#%%
def mars_facts():
    # Add try/except for error handling
    try:
        # Use 'read_html' to scrape the facts table into a dataframe
        df = pd.read_html('http://space-facts.com/mars/')[0]
         # Assign columns and set index of dataframe
        df.columns=['Description', 'Mars', 'Earth']
        df.set_index('Description', inplace=True)
        # Convert dataframe into HTML format, add bootstrap
        return df.to_html()

    except BaseException:
        return None

   

#%%
if __name__ == "__main__":
    # If running as script, print scraped data
    print(scrape_all())

#%%
# Visit the mars nasa news site
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
news_p

# %%
# Import Splinter and BeautifulSoup
from splinter import Browser
from bs4 import BeautifulSoup
# Set the executable path and initialize the chrome browser in splinter
executable_path = {'executable_path': './chromedriver'}
# Initiate headless driver for deployment
browser = Browser("chrome", executable_path="chromedriver", headless=True)
# Visit the mars nasa news site
url = 'https://mars.nasa.gov/news/'
browser.visit(url)
# Optional delay for loading the page
browser.is_element_present_by_css("ul.item_list li.slide", wait_time=1)
html = browser.html
news_soup = BeautifulSoup(html, 'html.parser')
slide_elem = news_soup.select_one('ul.item_list li.slide')
slide_elem.find("div", class_='content_title')# Use the parent element to find the paragraph text
news_p = slide_elem.find('div', class_="article_teaser_body").get_text()
news_p

# %%
# Use 'read_html' to scrape the facts table into a dataframe
df = pd.read_html('http://space-facts.com/mars/')[0]
    # Assign columns and set index of dataframe
df.columns=['Description', 'Mars']
df.set_index('Description', inplace=True)
# Convert dataframe into HTML format, add bootstrap
df.to_html()

# %%
df.head()

# %%
