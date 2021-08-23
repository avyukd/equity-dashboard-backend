import requests
from bs4 import BeautifulSoup
import html2text
import jsonlines
import openai
import json 
import os
from requests.api import get 
from unidecode import unidecode
import textract
import nltk
from requests.structures import CaseInsensitiveDict
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

def get_text_for_answers(filepath):
    text = textract.process(filepath).decode("utf-8")
    #tokenize the text into sentences
    text = unidecode(text)
    text = " ".join(text.split())
    sentences = nltk.sent_tokenize(text)
    return sentences

def create_openai_file(filepath):
    sentences = get_text_for_answers(filepath)
    with jsonlines.open('answers.jsonl', mode='w') as writer:
        cnt = 0
        for sentence in sentences:
            writer.write({"text":sentence, "metadata":str(cnt)})  
            cnt += 1
    keys = json.load(open("../keys.json"))
    openai.api_key = keys["openai_key"]
    response = openai.File.create(file=open("answers.jsonl"), purpose="answers")
    print(response)

def get_answers_from_open_api(query, fileid="file-nfohV7tdAeMPEmJzha1xLjwm",num_results=5):
    keys = json.load(open("../keys.json"))
    openai.api_key = keys["openai_key"]
    response = openai.Engine("davinci").search(
        search_model="davinci", 
        query=query, 
        max_rerank=num_results,
        file=fileid,
        return_metadata=True
    )
    return response

def delete_file(fileid):
    keys = json.load(open("../keys.json"))
    openai.api_key = keys["openai_key"]
    #delete request using requests library
    url = "https://api.openai.com/v1/files/"+fileid
    headers = CaseInsensitiveDict()
    headers["Authorization"] = "Bearer "+keys["openai_key"]
    response = requests.delete(url, headers=headers)
    print(response.content)

#delete_file("file-FkMSygR4oB9BcIGs3ycktu8u")

#create_openai_file("./test_files/baba10k.pdf")

sentences = get_text_for_answers("test_files/baba10k.pdf")
while True:
    q = input("Enter a question: ")
    all_data = get_answers_from_open_api(query=q,fileid="file-Vkurt3RrZ7Qz8MOfgYzYgAf5",num_results=1)["data"]
    for data in all_data:
        index = int(data["metadata"])
        print(sentences[index-3:index+3])

 
#uranium answers id: file-nfohV7tdAeMPEmJzha1xLjwm
#dcma rfp id: file-BTozQfpsqzuJYWSP9eyEG9Me
#coal answers id: file-rlWEPIXGvq3H0UViLrRVf5ue
#machine learning book: file-XdYldjkRt2DbPMVSHbHA2e8W
#baba 10k: file-Vkurt3RrZ7Qz8MOfgYzYgAf5


#create_initial_jsonl_file()
#send_to_open_api("bookmarks_8-8.jsonl")
#while True:
#    q = input("Query: ")
#    print(search_open_api(q)["data"][0].metadata.split("\n"))