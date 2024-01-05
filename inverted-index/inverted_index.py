import jieba
import re
import json
dic={}
for i in range(1,5001):
    r=open("info/"+str(i)+".txt",'r',encoding='utf-8')
    text=r.read()
    r.close()
    text=text.replace('\n','')
    
    s=open('stopwords.txt','r',encoding='utf-8')
    sw=s.readlines()
    stop_words=[]
    for wd in sw:
        wd=wd.replace('\n','')
        stop_words.append(wd)
    s.close()

    if(len(re.findall('发布时间：',text))>1):
        print('Warning:',i)
    title=re.findall("标题：(.*?)正",text)[0]
    words=jieba.lcut_for_search(title)
    for word in words:
        if(word in stop_words):
            continue
        if(word not in dic):
            dic[word]=[i]
        elif(i not in dic[word]):
            dic[word].append(i)
    body=re.findall("正文：(.*?)发布时间：",text)[0]
    words=jieba.lcut_for_search(body)
    for word in words:
        if(word in stop_words):
            continue
        if(word not in dic):
            dic[word]=[i]
        elif(i not in dic[word]):
            dic[word].append(i)
print(len(dic))
w=open('dic.json','w',encoding='utf-8')
w.write(json.dumps(dic,indent=2,ensure_ascii=False))
w.close()