from time import sleep
import requests
from bs4 import BeautifulSoup
import requests
import unicodedata
import csv
import pandas as pd

class Investing:
    def __init__(self,comp_name):
        self.comp_name = comp_name

    def headline(self,filename):
        id = 1
        currpg = 1
        while True:
            sleep(1)
            url2 = 'https://www.investing.com/equities/'+self.comp_name+'-news/'+str(id)
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36",
                "X-Requested-With": "XMLHttpRequest",
                "Accept": "text/html",
                "Accept-Encoding": "gzip, deflate, br",
                "Connection": "keep-alive",
            }
            req2 = requests.get(url2,headers=headers)
            soup2 = BeautifulSoup(req2.content, 'html.parser')
            curr = soup2.find('a',class_="pagination selected")
            currpg = int(curr.text)
            if((currpg==1) and (id != 1)):
                break
            print("extracting page..",id)
            articles = soup2.find_all('div', class_="mediumTitle1")
            news = articles[1].find_all('div',class_="textDiv")
            with open(filename,'a',newline='') as f:
                writer = csv.writer(f)
                for ele in news:
                    title = ele.find('a',class_="title")
                    datetag = ele.find('span',class_="date")
                    text_string = datetag.text
                    clean_text = unicodedata.normalize("NFKD",text_string)
                    date = clean_text.split('-')
                    date = date[1].strip()
                    news_url = 'https://www.investing.com'+title['href']
                    writer.writerow([title.string,news_url,date])
                f.close()
            id+=1