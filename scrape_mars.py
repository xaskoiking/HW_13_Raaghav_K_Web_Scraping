#Importing Dependencies
from splinter import Browser
from bs4 import BeautifulSoup
import pandas as pd

######----------Declaring variables----------######

#1.0) URL to fetch the Latest News Title and Paragraph Text
mars_news = "https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest"

#2.0) URL to fetch the MARS image
mars_image = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"

#3.0) URL to get twitter details
twitter_details = "https://twitter.com/marswxreport?lang=en"

#4.0) URL to get MARS facts
mars_facts = "https://space-facts.com/mars/"

#5.0) URL to get MARS Hemisphere
mars_hemisphere = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"

######----------Declaring Functions----------######

# Function to call the chrome driver
def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {"executable_path": "C:/chromedriver_win32/chromedriver.exe"}
    return Browser("chrome", **executable_path, headless=False)

#Initializing the browswer
browser = init_browser()
def scrape_marsDetails():
    #1.0) URL to fetch the Latest News Title and Paragraph Text
    #----------------------------------------------------------
    browser.visit(mars_news)
    html = browser.html
    soup = BeautifulSoup(html, "html.parser")
    newsDetails = soup.findAll('ul', attrs={'class': 'item_list'})
    counter = 0;

    for articlesList in newsDetails:
        for indArticle in articlesList:
            if counter == 0:
                news_date = indArticle.find('div', attrs={'class': 'list_date'}).text
                news_title = indArticle.find('div', attrs={'class': 'content_title'}).text
                news_p = indArticle.find('div', attrs={'class': 'article_teaser_body'}).text
                counter = counter + 1
    #----------------------------------------------------------

    #2.0) URL to fetch the MARS image
    #----------------------------------------------------------
    browser.visit(mars_image)
    html = browser.html
    soup = BeautifulSoup(html, "html.parser")

    #Finding the latest News Title Header
    featureImage = soup.find('article', attrs={'class':'carousel_item'})

    featuredImageBuffer = featureImage.attrs['style']
    featured_image_url  = "https://www.jpl.nasa.gov" + featuredImageBuffer[featuredImageBuffer.find('url') + 5: len(featuredImageBuffer) - 3] 
    #----------------------------------------------------------
    
    #3.0) URL to get twitter details
    #----------------------------------------------------------
    #This is to get the latest tweet
    counter = 0

    #Scraping the URL
    browser.visit(twitter_details)
    html = browser.html
    soup = BeautifulSoup(html, "html.parser")

    #Finding all the tweets content
    allTweetsContainter = soup.findAll('div', attrs={'class': 'js-tweet-text-container'})

    #Iterating the tweets to get the temperature details
    for a in allTweetsContainter:
        if("Sol" in a.find('p').text and "pressure" in a.find('p').text and "daylight" in a.find('p').text and counter == 0):
            mars_weather = a.find('p').text
            counter = counter + 1
    #4.0) URL to get Mars Facts
    #----------------------------------------------------------
    #This is to get the Mars Facts

    #Scraping the URL
    browser.visit(mars_facts)
    html = browser.html
    soup = BeautifulSoup(html, "html.parser")

    #Finding all the facts
    tables = pd.read_html(mars_facts)
    df = tables[0]
    df.columns = ['desc', 'facts']

    desc = df["desc"].values.tolist()
    facts = df["facts"].values.tolist()
    
    #5.0) URL to get Mars Facts
    #----------------------------------------------------------
    #To get the MARS image details
    #Scraping the URL
    browser.visit(mars_hemisphere)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    #marsHemisphere
    marsHemisphere = soup.findAll('div', attrs={'class': 'item'})

    #Adding the text to the lit, so that you can use the linktext
    imageTextList = []

    #Iterating the class -- item and storing the tex
    for a in marsHemisphere:
        for b in a.findAll('a'):
            if(len(b.text) > 0):
                imageTextList.append(b.text)
    
    #Creating a list to store the dictionaries
    hemisphere_image_urls = []

    #Iteraing the text and adding the text and URL for the last module of the web page
    for text in imageTextList:
    #Parent Page
    browser.visit(mars_hemisphere)
    html = browser.html
    
    #Click Action
    browser.click_link_by_partial_text(text)
    
    #Child Page
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    image = soup.findAll('img')
    for a in image:
        if('full' in a.get('src')):
            dictDetails = {'title':text, 'img_url' : 'https://astrogeology.usgs.gov' + a.get('src') }
            hemisphere_image_urls.append(dictDetails)
        
    #----------------------------------------------------------
    
    marsDetails = {
            "news_p": news_p,
            "news_title": news_title,
            "featured_image_url": featured_image_url,
            "mars_weather": mars_weather,
            "desc":desc,
            "facts":facts,
            "hemisphere_image_urls":hemisphere_image_urls
        }

    return marsDetails;