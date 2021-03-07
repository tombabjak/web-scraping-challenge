from bs4 import BeautifulSoup as bs
from splinter import Browser
import pandas as pd

def init_browser():
    executable_path = {"executable_path": "/Users/thomasbabjak/.wdm/drivers/chromedriver/mac64/89.0.4389.23/chromedriver"}
    return Browser("chrome", **executable_path, headless=False)


def scrape():
    browser = init_browser()
    url = "https://mars.nasa.gov/news/"
    browser.visit(url)

    html = browser.html
    soup = bs(html, "html.parser")

    latest = soup.find(class_ = 'slide')

    news_title = latest.find('div', class_="content_title").text
    news_p = latest.find("div", class_ = "rollover_description_inner").text

    JPL_url = "https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/index.html"
    browser.visit(JPL_url)

    html = browser.html
    soup = bs(html, 'html.parser')

    header = soup.find_all('div', class_='header')

    for image in header:
        partial = image.find('img', class_="headerimage fade-in")['src']
        featured_image_url = "https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/" + partial
    
    mars_url = 'https://space-facts.com/mars/'
    tables = pd.read_html(mars_url)

    df = tables[0]
    df.columns = ['Description', 'Mars']
    df.set_index('Description',inplace=True)
    df_html = df.to_html('table.html')

    hemi_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(hemi_url)

    html = browser.html
    soup = bs(html, 'html.parser')

    hemisphere_image_urls = []

    hemispheres = soup.find_all('div', class_='item')

    for hemisphere in hemispheres:
        sub_url = 'https://astrogeology.usgs.gov' + hemisphere.a['href']
        browser.visit(sub_url)
        html = browser.html
        page = bs(html, 'html.parser')
        
        title = page.find('h2', class_='title').text.strip('Enhanced')
        
        partial = page.find("div", class_="wide-image-wrapper")
        img_url = partial.li.a['href']
        
        dictionary = {"title":title,"img_url":img_url}
        
        hemisphere_image_urls.append(dictionary)

    mars_data = {
        "news_title": news_title,
        "news_p": news_p,
        "featured_image_url": featured_image_url,
        "df_html": df_html,
        "hemisphere_image_urls": hemisphere_image_urls
    }

    browser.quit()

    return mars_data
