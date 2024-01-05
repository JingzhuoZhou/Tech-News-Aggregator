import requests
import re

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/116.0"
}
url_list = []

url1 = "https://feed.mix.sina.com.cn/api/roll/get?pageid=153&lid=2515&etime="
etime = 1693065600
url2 = "&stime="
stime = 1693152000
url3 = "&ctime="
url4 = "&date=2023-07-30&k=&num=50&page=1&r=0.37625512819868745&callback=jQuery111207622619381524913_1693212234041&_=1693212234042"
# 经测试，url中date不修改不影响结果，故只修改起止时间

while len(url_list) < 5000:
    response = requests.get(
        url1 + str(etime) + url2 + str(stime) + url3 + str(stime) + url4,
        params={},
        headers=headers,
    )
    response.encoding = "utf-8"
    url_list.extend(re.findall('"url":"(.*?)",', response.text))
    stime = etime
    etime -= 86400

f = open("urls.txt", "w", encoding="utf-8")
for i in range(len(url_list)):
    url_list[i] = url_list[i].replace("\/", "/")
    f.write(url_list[i] + "\n")
f.close()
