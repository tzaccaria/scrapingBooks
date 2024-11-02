import requests
from bs4 import BeautifulSoup


# get all articles with requests to books.toscrap.com
def getAllArticles():
    encode = "utf-8"
    parser = "html.parser"
    url_catalogue ="https://books.toscrape.com/catalogue/"
    books  = []
    print("Extract books ....")
    for n in range(1,51):
        print("\tPage " + str(n))
        url = "https://books.toscrape.com/catalogue/page-" + str(n) + ".html"

        response= requests.get(url)

        soup = BeautifulSoup(response.content.decode(encode), parser)

        articles = soup.find_all('article')


        for article in articles:
            link = getArticleLink(url_catalogue,article)
            print(link)
            book = getArticle(link, article)
            books.append(book)

    return books


def getArticle(link, article):
    res = requests.get(link)
    soup = BeautifulSoup(res.content.decode('utf-8'), 'html.parser')
    # title
    title = getArticleTitle(soup)
    print(title)
    # description
    description = getArticleDescription(soup)
    print(description)
    # price
    price = getArticlePrice(soup)
    print(price)
    # img
    img = getArticleImage(soup)
    print(img)
    # availability
    availability = getArticleAvailibility(soup)
    print(availability)
    # img

    # tax

    # reviews

    # product type

    # upc
    #title = getArticleTitle(article)
    #price = getArticlePrice(article)
    #link = getArticleLink(link,article)
    #print(link)
    #bookObj = {
    #    "title": title,
    #    "price": price,
    #    "link": link,
    #}
    #return bookObj


def getArticleLink(url_catalogue,article):
    return url_catalogue + article.find('h3').find('a').get('href')
    #return url_catalogue + article.find('h3').find('a').get('href')
def getArticleImage(article):
    return "https://books.toscrape/" + (article.find('img').get('src')).replace('../../', '');
def getArticleDescription(article):
    try:
        description = article.find('article', class_='product_page').find('p', attrs={"class": None}).text
        return description
    except:
        return "no description"
def getArticleAvailibility(article):
    return article.find('p', class_='instock availability').text.strip()

def getArticleTitle(article):
    return article.find('h1').text

def getArticlePrice(article):
    return article.find('p', class_= 'price_color').text
    #return article.find('div', class_= 'product_price').find('p').text
