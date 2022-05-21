
from crypt import methods
from flask import request
from flask import Flask,json
from libgen_api import LibgenSearch
from pprint import pprint

app = Flask(__name__)




def searchBook(title):
    s = LibgenSearch()
    print(title)
    results = s.search_title(title)
    pprint(results)
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
     
  
# main driver function
if __name__ == '__main__':
  
    # run() method of Flask class runs the application 
    # on the local development server.
    app.run()
