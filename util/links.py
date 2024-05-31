import requests
from bs4 import BeautifulSoup
from util.config import retryBackoff, reqSleep, baseURL
import time

def extractLinks(url):
    time.sleep(reqSleep)
    newLinks = []
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
    try:
        page = requests.get(url, headers=headers)
    except:
        try:
            time.sleep(retryBackoff)
            page = requests.get(url, headers=headers)
        except:
            return []

    soup = BeautifulSoup(page.text, 'lxml')
    mylinks = soup.findAll("a", { "class" : "ga_w2gi_lp listitem" })
    for i in range(len(mylinks)):
        link = mylinks[i]
        newLink = link['href']
        newLinks.append(newLink)

    return newLinks

def extractStoreLinks(url):
    time.sleep(reqSleep)
    newLinks = []
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
    try:
        page = requests.get(url, headers=headers)
    except:
        try:
            time.sleep(retryBackoff)
            page = requests.get(url, headers=headers)
        except:
            return []
    soup = BeautifulSoup(page.text, 'lxml')
    mylinks = soup.findAll("a", { "class" : "capital listitem" })
    for i in range(len(mylinks)):
        link = mylinks[i]
        newLink = link['href']
        newLinks.append(newLink)
    
    return newLinks

def extractStoreInfo(url):
    time.sleep(reqSleep)
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
    try:
        page = requests.get(url, headers=headers)
    except:
        try:
            time.sleep(retryBackoff)
            page = requests.get(url, headers=headers)
        except:
            return []
    soup = BeautifulSoup(page.text, 'lxml')
    storeNum = url.split('/')[-2]
    city = url.split('/')[-3]
    state = url.split('/')[-4]
    try:
        name = soup.find("title").text.split(' (')[0]
    except:
        name = ''
    try:
        phoneNumber = soup.find("a", { "class" : "ga_w2gi_lp phoneclr" }).text.strip()
    except:
        phoneNumber = ''
    try:
        address = ''
        addressTemp = soup.find("div", { "class" : "addressline" }).text.replace('\t','').split('\n')
        for line in addressTemp[:8]:
            if line.isspace():
                continue
            address+= " {}".format(line.strip())
    except:
        address = ''
    try:
        latitude = soup.find("meta", { "property" : "place:location:latitude" })['content']
    except:
        latitude = ''

    try:
        longitude = soup.find("meta", { "property" : "place:location:longitude" })['content']
    except:
        longitude = ''
    return [name, storeNum, phoneNumber, address, url, longitude, latitude, city, state]