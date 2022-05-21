
from crypt import methods
from flask import request
from flask import Flask,json
from libgen_api import LibgenSearch
from pprint import pprint
from bs4 import BeautifulSoup
import requests

app = Flask(__name__)

def searchBook(title):
    s = LibgenSearch()
    finalSearchResult = []
    results = s.search_title(title)
    result = results
    for i in result:
        mirror1 = i["Mirror_1"]
        imgurl = extractCoverImageOfBook(mirror1)
        i["coverImage"] = imgurl["imageUrl"]
        finalSearchResult.append(i)
    return json.dumps(results)

def searchAuthor(author):
    s = LibgenSearch()
    results = s.search_author(author)
    pprint(results)
    return json.dumps(results)

def downloadBook(itemToDownload):
    s = LibgenSearch()
    download_links = s.resolve_download_links(itemToDownload)
    print(download_links)
    return download_links

def extractCoverImageOfBook(url):
    page = requests.get(url=url)
    soup = BeautifulSoup(page.text, "html.parser")
    links = soup.find("img")
    print(links["src"]) 
    return json.dumps({"imageUrl": "http://library.lol/" + links["src"]})

@app.route('/searchBooks',methods=['GET'])
def get_books():
    searchText = request.args.get('bookTitle')
    return searchBook(searchText)

@app.route('/downloadBook',methods=['POST'])
def download_book():
    content_type = request.headers.get('Content-Type')
    if (content_type == 'application/json'):
        itemToDownload = request.json
        return downloadBook(itemToDownload) 
    else:
        return 'Content-Type not supported!'    


@app.route('/getBookCover',methods=['POST'])
def getBookCover(): 
    content_type = request.headers.get('Content-Type')
    if (content_type == 'application/json'):
        bookUrl = request.json
        return extractCoverImageOfBook(bookUrl["url"]) 
    else:
        return 'Content-Type not supported!'      
  
# main driver function
if __name__ == '__main__':
  
    # run() method of Flask class runs the application 
    # on the local development server.
    app.run()
