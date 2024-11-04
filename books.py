import requests
from bs4 import BeautifulSoup


# get all books with requests to books.toscrape.com
def getAllBooks():
    encode = "utf-8"
    parser = "html.parser"
    url_catalogue ="https://books.toscrape.com/catalogue/"
    books  = []
    print("Extract books ....")
    for n in range(1,51):
        print("\tPage " + str(n))
        url = "https://books.toscrape.com/catalogue/page-" + str(n) + ".html"

        response= requests.get(url)

        soup = BeautifulSoup(response.content.decode("utf-8"), "html.parser")

        articles = soup.find_all('article')


        for article in articles:
            link = getArticleLink(url_catalogue,article)
            book = getBook(link, article)
            books.append(book)

    return books


def getBook(link, article):
    res = requests.get(link)
    soup = BeautifulSoup(res.content.decode('utf-8'), 'html.parser')
    # title
    title = getArticleTitle(soup)
    # description
    description = getArticleDescription(soup)
    # price
    price = getArticlePrice(soup)
    # img
    img = getArticleImage(soup)
    # availability
    availability = getArticleAvailibility(soup)
    # upc
    upc = getArticleUpc(soup)
    #product type
    productType = getArticleType(soup)
    # tax
    tax = getArticleTax(soup)
    # reviews
    reviews = getArticleReviews(soup)
    # rating
    rating = getArticleRating(soup)

    book = {
        "title":title,
        "description":description,
        "price":price,
        "img":img,
        "availability":availability,
        "upc":upc,
        "productType":productType,
        "tax":tax,
        "reviews":reviews,
        "rating":rating
    }

    return book



def getArticleLink(url_catalogue,article):
    return url_catalogue + article.find('h3').find('a').get('href')
def getArticleUpc(article):
    trs = article.find_all('tr')

    for e in trs:
        if e.find('th').text == 'UPC' :
            return e.find('td').text
def getArticleType(article):
    trs = article.find_all('tr')
    for e in trs:
        if e.find('th').text == 'Product Type':
            return e.find('td').text

def getArticleReviews(article):
    trs = article.find_all('tr')
    for e in trs:
        if e.find('th').text == 'Number of reviews':
            return e.find('td').text
def getArticleTax(article):
    trs = article.find_all('tr')
    for e in trs:
        if e.find('th').text == 'Tax':
            return e.find('td').text
def getArticleImage(article):
    return "https://books.toscrape/" + (article.find('img').get('src')).replace('../../', '');
def getArticleRating(article):
    return article.find('p', class_='star-rating').get('class')[-1];
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
