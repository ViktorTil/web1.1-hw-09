import json

import requests
from bs4 import BeautifulSoup

from data import url, file_authors, file_quotes

def get_info():
    page_num = 1
    authors_list = []
    quotes_info = []
    authors_info = []
    while True:
        working_url = f"{url}/page/{page_num}/"   
        response = requests.get(working_url)
        soup = BeautifulSoup(response.text, 'html.parser')
        content = soup.select('div[class = quote]')    
        if content:
            for cont in content:
                author_info = {}
                tags = []
                que = cont.find('span', attrs={"class": "text"}).text
                auth = cont.find('small', class_ ="author").text     
                tags_ = cont.find_all("a", attrs={"class": "tag"})
                for tag in tags_:
                    tags.append(tag.text)
                quotes_info.append({"tags": tags, "author":auth, "quote": que})
                if not auth in authors_list:
                    authors_list.append(auth)
                    auth_link = cont.find('a')
                    auth_link = auth_link["href"]
                    author_info = {"fullname":auth}
                    author_info.update(get_author_info(url+auth_link+"/"))
                    authors_info.append(author_info)                          
        else:
            break
        page_num += 1 
    return quotes_info, authors_info

def get_author_info(url):
    author_info = {}
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml')
    content = soup.select_one('div[class = author-details]')
    data = content.find("span", attrs = {"class": "author-born-date"}).text
    author_info["born_date"] = data
    born_location = content.find("span", attrs = {"class": "author-born-location"}).text
    author_info["born_location"] = born_location
    description = content.find("div", class_ = "author-description").text.strip()
    author_info["description"] = description
    return author_info

def run():
    print("\n Wait for scraping...", end="\r")
    quotes_data, authors_data = get_info()
    
    with open(file_quotes, 'w', encoding='utf-8') as fh:
        json.dump(quotes_data, fh, ensure_ascii=False)
        
    with open(file_authors, 'w', encoding='utf-8') as fh1:
        json.dump(authors_data, fh1, ensure_ascii=False)
    
    print("\r", end="Scraping successful!!!\n")
if __name__ == "__main__":
    run()

    

    
