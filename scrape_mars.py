#Importing Dependencies
from splinter import Browser
from bs4 import BeautifulSoup

######----------Declaring variables----------######

#1.0) URL to fetch the Latest News Title and Paragraph Text
mars_news = "https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest"

#2.o) URL to fetch the MARS image
mars_image = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"

######----------Declaring Functions----------######

# Function to call the chrome driver
def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {"executable_path": "C:/chromedriver_win32/chromedriver.exe"}
    return Browser("chrome", **executable_path, headless=False)

#Initializing the browswer
browser = init_browser()
def scrape_marsDetails():
    #Scraping the URL
    browser.visit(mars_news)
    html = browser.html
    soup = BeautifulSoup(html, "html.parser")

    #Finding the latest News Title Header
    newsTitleHeader = soup.find('div', attrs={'class':'content_title'})
    newsParaText = soup.find('div', attrs={'class':'article_teaser_body'})

    #Grabbing the news title
    for a in newsTitleHeader.find_all('a'):
        newsTitle = a.text #for getting text between the link

    #Storing the news Para Text
    newsParaText = newsParaText.text

    #Scraping the URL
    browser.visit(mars_image)
    html = browser.html
    soup = BeautifulSoup(html, "html.parser")

    #Finding the latest News Title Header
    featureImage = soup.find('article', attrs={'class':'carousel_item'})

    featuredImageBuffer = featureImage.attrs['style']
    featured_image_url  = "https://www.jpl.nasa.gov" + featuredImageBuffer[featuredImageBuffer.find('url') + 5: len(featuredImageBuffer) - 3]
    marsDetails = {
        "newsParaText": newsParaText,
        "newsTitle": newsTitle,
        "featured_image_url": featured_image_url,
    }

    return marsDetails;