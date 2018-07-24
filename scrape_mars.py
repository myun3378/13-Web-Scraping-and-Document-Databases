# Dependencies
from bs4 import BeautifulSoup
import requests
from splinter import Browser
import pandas as pd
from selenium import webdriver     

def scrape():
    # NASA Mars News

    # URL of page to be scraped. 
    url = 'https://mars.nasa.gov/news/'

    # Retrieve page with the requests module. Make a request to the url.
    response = requests.get(url)

    # Create a Beautiful Soup object
    soup = BeautifulSoup(response.text, 'html.parser')

    # Latest News Title
    news_title = soup.find('div', class_='content_title').text

    # Get paragraph text
    news_p = soup.find('div', class_='rollover_description_inner').text


    # JPL Mars Space Images - Featured Image

    #chromedriver
    executable_path = {'executable_path': 'chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=False)

    # URL of page to be scraped. 
    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)

    #Feed browser.html into BeautifulSoup
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    browser.click_link_by_partial_text('FULL IMAGE')
    browser.click_link_by_partial_text('more info')

    jpl_html = browser.html
    jpl_soup = BeautifulSoup(jpl_html, 'html.parser')
    temp_url = jpl_soup.find('img', class_='main_image')
    img_url = temp_url.get('src')

    feature_image_url = "https://www.jpl.nasa.gov" + img_url

    #Close the chrome browser 
    browser.quit()             


    #Mars Weather

    # URL of page to be scraped. 
    url = 'https://twitter.com/marswxreport?lang=en'

    # Retrieve page with the requests module. Make a request to the url.
    response = requests.get(url)

    # Create a Beautiful Soup object
    soup = BeautifulSoup(response.text, 'html.parser')

    tweets = []
    tweets = soup.find_all('div', class_="js-tweet-text-container")

    for i in range(20):
        t = tweets[i].text
        if "Sol " in t:
            mars_weather = t
            break


    # Mars Facts

    # URL of page to be scraped. 
    url = 'https://space-facts.com/mars/'

    #List of dataframes of any tables it found
    tables = pd.read_html(url)  

    df = tables[0]
    df.columns = ['Profile','Data']

    #DataFrame to HTML
    html_table = df.to_html()
    mission_to_mars['mars_facts_table'] = html_table
    html_table.replace('\n', '')
    df.to_html('mars_table.html')

    # Mars Hemispheres

    #chromedriver
    executable_path = {'executable_path': 'chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=False)

    # URL of page to be scraped. 
    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')    

    hemisphere_image_urls = []                    

    products = soup.find('div', class_='result-list')                   
    hemispheres = products.find_all('div', class_='item')

    for hemisphere in hemispheres: 
        title = hemisphere.find('div', class_='description')
        
        title_text = title.a.text  
        title_text = title_text.replace(' Enhanced', '')
        browser.click_link_by_partial_text(title_text)
        
        html = browser.html
        soup = BeautifulSoup(html, 'html.parser')   
        image = soup.find('div', class_='downloads').find('ul').find('li') 
        img_url = image.a['href']
        
        hemisphere_image_urls.append({'title': title_text, 'img_url': img_url})
        
        browser.click_link_by_partial_text('Back')

    mars_data = {
     "News_Title": news_title,
     "Paragraph_Text": news_p,
     "Most_Recent_Mars_Image": feature_image_url,
     "Mars_Weather": mars_weather,
     "mars_h": hemisphere_image_urls
     }
    #Close the chrome browser 
    browser.quit()  

