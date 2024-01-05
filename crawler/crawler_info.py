import requests
from bs4 import BeautifulSoup
import re
import json
import random
import os
import time
from requests.adapters import HTTPAdapter

r = open("urls.txt", "r", encoding="utf-8")
urls = r.read().splitlines()
r.close()

data_list = []
headers = {
    "Referer": "https://news.sina.com.cn/roll/",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36",
}


s = requests.Session()
s.mount("http://", HTTPAdapter(max_retries=10))  # 访问http协议时，设置重传请求最多三次
s.mount("https://", HTTPAdapter(max_retries=10))

if not os.path.exists("images"):
    os.mkdir("images")
if not os.path.exists("info"):
    os.mkdir("info")
if not os.path.exists("html"):
    os.mkdir("html")
for i in range(5000):
    time.sleep(random.uniform(1, 2))

    w = open("info/" + str(i + 1) + ".txt", "w", encoding="utf-8")
    w.write("URL: " + urls[i] + "\n")
    # print(urls[i])
    response = requests.get(urls[i], params={}, headers=headers)
    response.encoding = "utf-8"
    soup = BeautifulSoup(response.text, "html.parser")

    title = re.findall('<meta property="og:title" content="(.*?)" />', response.text)
    if not title:
        print("title:\n")
        print(urls[i])
    data_list.append({"title": title[0]})
    w.write("标题：" + title[0] + "\n正文：\n")

    article = soup.select("#artibody")[0].select("p")
    article = re.findall("<p.*?>(.*?)</p>", str(article))

    num = 0
    flag = True
    body = ""
    for j in article:
        p = str(j)
        # print(p+'\n')
        num += 1
        data_list[-1]["brief"] = ""
        while re.search("<", p):
            info = re.findall("(<font.*?>)(.*?)(</font>)", p)
            for k in info:
                p = p.replace(k[0] + k[1] + k[2], k[1])
            info = re.findall("(<strong>)(.*?)(</strong>)", p)
            for k in info:
                p = p.replace(k[0] + k[1] + k[2], k[1])
            info = re.findall("(<em>)(.*?)(</em>)", p)
            for k in info:
                p = p.replace(k[0] + k[1] + k[2], k[1])
            info = re.findall("(<u>)(.*?)(</u>)", p)
            for k in info:
                p = p.replace(k[0] + k[1] + k[2], k[1])
            info = re.findall("(<span.*?>)(.*?)(</span>)", p)
            for k in info:
                p = p.replace(k[0] + k[1] + k[2], k[1])
            info = re.findall("(<a.*?>)(.*?)(</a>)", p)
            for k in info:
                p = p.replace(k[0] + k[1] + k[2], k[1])
            info = re.findall("<!--.*?-->", p)
            for k in info:
                p = p.replace(k, "")
            info = re.findall("<div.*?/div>", p)
            for k in info:
                p = p.replace(k, "")
            info = re.findall("<br.*?>", p)
            for k in info:
                p = p.replace(k, "")
        body = body + p + "\n"
    w.write(body)
    data_list[-1]["brief"] = body[:90]

    tm = soup.select("#top_bar > div > div.date-source > span.date")
    if not tm:
        tm = soup.select("#pub_date")
    if not tm:
        print("time:\n")
        print(urls[i])
    t = str(tm)
    t = t.replace(" ", "")
    t = t.replace("\n", "")
    t = t.replace("\r", "")
    t = re.findall("<span.*?>(.*?)</span>", t)
    for k in t:
        tm = str(k)
        tm = tm.replace("-", "年", 1)
        tm = tm.replace("-", "月", 1)
        if re.match("\d", tm[10]):
            tm = list(tm)
            tm.insert(10, "日")
            del tm[-3:]
            tm = "".join(tm)
    w.write("发布时间：" + tm + "\n")
    data_list[-1]["date"] = tm

    author = soup.select("#top_bar > div > div.date-source > a")
    if not author:
        author = soup.select(
            "#top_bar > div > div.date-source > span.source.ent-source"
        )
    if not author:
        author = soup.select("#author_ename > a")
    if not author:
        author = soup.select("#media_name")
    if not author:
        author = soup.select("#top_bar > div > div.date-source > span.source > a")
    if not author:
        author = soup.select("#top_bar > div > div.date-source > span.source")
    if not author:
        print("author:\n")
        print(urls[i])

    p = str(author[0])
    info = re.findall("(<span.*?>)(.*?)(</span>)", p)
    for k in info:
        p = p.replace(k[0] + k[1] + k[2], k[1])
    info = re.findall("(<a.*?>)(.*?)(</a>)", p)
    for k in info:
        p = p.replace(k[0] + k[1] + k[2], k[1])
    w.write("作者:" + p + "\n")
    data_list[-1]["author"] = p

    h = open("html/" + str(i + 1) + ".html", "w", encoding="utf-8")
    ad = soup.find("div", class_="clearfix appendQr_wrap")
    if ad:
        ad.decompose()
    html = "{% load static %}\n" + str(soup.select("#artibody")[0])

    imgs = soup.findAll("div", class_="img_wrapper")
    for img in imgs:
        img_url = re.findall('<img.*?src="(.*?)"', str(img))
        if img_url:
            img_url = img_url[0]
        else:
            continue
        # print(img_url)
        if img_url[0] == "/":
            url = "https:" + img_url
        else:
            url = img_url
        img_data = requests.get(url).content
        img_name = img_url.split("/")[-1]
        with open(os.path.join("images", img_name), "wb") as f:
            f.write(img_data)
            f.close()
        html = html.replace(img_url, '{% static "images/' + img_name + '" %}')
    h.write(html)
    h.close()

    data_list[-1]["url"] = urls[i]
    data_list[-1]["like"] = random.randint(100, 30000)
    if tm[6] == "8":
        data_list[-1]["category"] = "August"
    elif tm[6] == "7":
        data_list[-1]["category"] = "July"
    elif tm[6] == "6":
        data_list[-1]["category"] = "June"
    elif tm[6] == "5":
        data_list[-1]["category"] = "May"
    else:
        data_list[-1]["category"] = "April"
    w.close()
j = open("data.json", "w", encoding="utf-8")
j.write(json.dumps(data_list, indent=2, ensure_ascii=False))
j.close()
