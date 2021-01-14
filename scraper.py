import requests
from bs4 import BeautifulSoup

def details(soup):
    title = soup.find('h1', class_='title-name h1_bold_none').getText()
    print("\nName of the Anime : ", title,"\n") 
    description = soup.find('p', {'itemprop': 'description'}).getText()
    print('Description :  \n' + description)
    imageUrl = soup.find('img', alt=title)['data-src']
    print('Image link :  ' + imageUrl)
    score = soup.find('div', class_='score-label').getText()
    print('MyAnimeList Score :  ' + score)
    rank = soup.find('span', class_='numbers ranked').getText()
    print(rank)
    popularity = soup.find('span', class_='numbers popularity').getText()
    print(popularity)


def search():
    anime_name = input("--> Enter the name of the Anime : ")
    search_url = ("https://myanimelist.net/search/all?q=" + anime_name +"&cat=anime")
    source_code = requests.get(search_url)
    content = source_code.content
    global soup
    soup = BeautifulSoup(content,features="html.parser")
    link = soup.find('a', class_='hoverinfo_trigger fw-b fl-l')['href']

    actualPage = requests.get(link)
    actualContent = actualPage.content
    goodSoup = BeautifulSoup(actualContent,features="html.parser")
    # print (goodSoup)

    print('Closest Matching Anime :  ' + link)
    details(goodSoup)

if __name__ == "__main__":
    search()
