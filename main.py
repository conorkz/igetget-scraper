from bs4 import BeautifulSoup
import re
import requests
from datetime import datetime
import pytz
import csv
roi = 'no info on the website'
response = requests.get('https://www.igetget.com/list/%E5%BF%83%E7%90%86%E5%AD%A6/n5lF7jt9fkU1', headers={'User-Agent': 'Mozilla/5.0'})
soup = BeautifulSoup(response.content, "html.parser")
with open('igetget.csv', "w", encoding="utf-8", newline="") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['Berlin time', 'URL', 'Title', 'Subtitle', 'Book cover', 'Price in 得到贝', 'Listen in', 'Description', 'ISBN', 'Publication date', 'Publisher', 'Translated by', 'Author', 'Original title', 'Full title'])
    for k in soup.select('.category-list a'):
        url = 'https://www.igetget.com' + k['href']
        while True:
            respons = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
            sou = BeautifulSoup(respons.content, "html.parser")
            print(f'\nPAGE: {url}\n')
            for y in sou.select('.pro-name a'):
                link = 'https://www.igetget.com' + y['href']
                print(link)
                respon = requests.get(link, headers={'User-Agent': 'Mozilla/5.0'})
                sorpa = BeautifulSoup(respon.content, "html.parser")
                if sorpa.select_one('.head-text .pro-common'):
                    time = sorpa.select_one('.head-text .pro-common').text.strip().replace('分',' minutes ').replace('秒',' seconds')
                else:
                    time = roi
                if sorpa.select_one('.head-text .pro-name'):
                    title = sorpa.select_one('.head-text .pro-name').text.strip()
                else:
                    title = roi
                if sorpa.select_one('.head-text .pro-intro'):
                    subtitle = sorpa.select_one('.head-text .pro-intro').text.strip()
                else:
                    subtitle = roi
                if sorpa.select_one('.page-head img'):
                    img = sorpa.select_one('.page-head img')['src']
                else:
                    img = roi
                if sorpa.select_one('span.coin-num'):
                    price = sorpa.select_one('span.coin-num').text
                else:
                    price = roi
                if sorpa.select_one('.intro-sections'):
                    ff = []
                    for j in sorpa.select_one('.intro-sections').find_all(['p','h4']):
                        if j.text.strip() == '推荐阅读':
                            break
                        ff.append(j.text.strip())
                    text = "\n".join(ff)
                    k = sorpa.select_one('.intro-sections').text.replace(':','：')
                    if re.search(r'ISBN：(\d+)', k):
                        isbn = re.search(r'ISBN：(\d+)', k).group(1)
                    elif re.search(r'ISBN：\s(\d+)', k):
                        isbn = re.search(r'ISBN：\s(\d+)', k).group(1)
                    else:
                        isbn = roi
                    if re.search(r'出版年：(.+)', k):
                        date = re.search(r'出版年：(.+)', k).group(1)
                    else:
                        date = roi
                    if re.search(r'出版社：(.+)', k):
                        publisher = re.search(r'出版社：(.+)', k).group(1)
                    else:
                        publisher = roi
                    if re.search(r'译者：(.+)', k):
                        translator = re.search(r'译者：(.+)', k).group(1)
                    else:
                        translator = roi
                    if re.search(r'作者：(.+)', k):
                        author = re.search(r'作者：(.+)', k).group(1)
                    else:
                        author = roi
                    if re.search(r'原作名：(.+)', k):
                        orgtitle = re.search(r'原作名：(.+)', k).group(1)
                    else:
                        orgtitle = roi
                    if re.search(r'书名：(.+)', k):
                        fulltitle = re.search(r'书名：(.+)', k).group(1)
                    else:
                        fulltitle = roi
                else:
                    text = isbn = date = publisher = translator = author = orgtitle = fulltitle = roi
                berlin = datetime.now(pytz.timezone('Europe/Berlin')).strftime('%Y-%m-%d %H:%M:%S %Z')
                writer.writerow([berlin, link, title, subtitle, img, price, time, text, isbn, date, publisher, translator, author, orgtitle, fulltitle]) 
            if sou.select_one('.right-rec.right-active') and sou.find(class_='page-num-div page-active'):
                url = 'https://www.igetget.com' + sou.find(class_='page-num-div page-active').find_next_sibling().find('a')['href']
            else:
                break