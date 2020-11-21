from time import sleep
import requests
from bs4 import BeautifulSoup
import requests
import unicodedata
import csv
import pandas as pd

class Investing:
    headers = {
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36",
                    "X-Requested-With": "XMLHttpRequest",
                    "Accept": "text/html",
                    "Accept-Encoding": "gzip, deflate, br",
                    "Connection": "keep-alive",
                }

    def __init__(self,comp_name):
        self.comp_name = comp_name

    def headline(self,filename):
        id = 1
        currpg = 1
        while True:
            try:
                sleep(1)
                url2 = 'https://www.investing.com/equities/'+self.comp_name+'-news/'+str(id)
                
                req2 = requests.get(url2,headers=self.headers)
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
            except Exception as e:
                print(e)
                break

        
    def get_meta_data(self):
        print(self.comp_name)

    def content(self,file_name):
        data = pd.read_csv(file_name,names = ['title','url','date'],encoding='latin1')
        data['content'] = ""
        for i in range(len(data['url'])):
            news_url = data['url'][i]
            # print(data['url'][i])
            news_content = requests.get(news_url,headers=self.headers)
            page = BeautifulSoup(news_content.content,'html.parser')
            try:
                article = page.find('div',class_='WYSIWYG articlePage')
                cont = article.find_all('p')
                content = []
                for para in cont:
                    # print(para.text, sep="\n\n\n")
                    content.append(para.text)
                content = "".join(content)
                data['content'][i]=content
                # print(content)
                print("Extracting...",news_url)
            except Exception as e:
                print("Error",e)
                pass
        data.to_csv(self.comp_name+'-Investing-data.csv',index=True,header=True)
