import requests
from bs4 import BeautifulSoup
import html2text
import jsonlines
import openai
import json 
import os 
from unidecode import unidecode

#bookmarks_8_8_21.html fileid = file-WRUnw4eMVT1oaiZrgTWXOogH

def get_bookmark_links():
    bookmarks_html = open('bookmarks_8_8_21.html', 'rb').read()
    soup = BeautifulSoup(bookmarks_html, 'html.parser')
    link_els = soup.find_all('a')
    links = []
    for link in link_els:
        href = link.get('href')
        links.append(href)
    return links
def create_initial_jsonl_file(length_limit=1500):
    links = get_bookmark_links()
    data = []
    for link in links:
        if "pdf" not in link:
            print(link)
            try:
                response = requests.get(link)
                soup = BeautifulSoup(response.text, 'html.parser')
                title = soup.find('title').text
                title = unidecode(title)
                title = " ".join(title.split())
                text = html2text.html2text(response.text)
                text = unidecode(text)
                text = " ".join(text.split())
                text = text[:length_limit]
                data.append({"text":text, "metadata":link+"\n"+title})
            except:
                print("Error for " + link)
    with jsonlines.open('bookmarks_8-8.jsonl', mode='w') as writer:
            for doc in data:
                writer.write(doc)    

def send_to_open_api(filename):
    keys = json.load(open("../keys.json"))
    openai.api_key = keys["openai_key"]
    response = openai.File.create(file=open(filename), purpose="search")
    print(response)

def search_open_api(query):
    keys = json.load(open("../keys.json"))
    openai.api_key = keys["openai_key"]
    response = openai.Engine("davinci").search(
        search_model="davinci", 
        query=query, 
        max_rerank=5,
        file="file-WRUnw4eMVT1oaiZrgTWXOogH",
        return_metadata=True
    )
    return response
#create_initial_jsonl_file()
#send_to_open_api("bookmarks_8-8.jsonl")
#while True:
#    q = input("Query: ")
#    print(search_open_api(q)["data"][0].metadata.split("\n"))