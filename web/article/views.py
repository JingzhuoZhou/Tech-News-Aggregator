from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import ArticleInfo,Comment,Dic
import random
from django.core.paginator import Paginator
from .forms import CommentForm
import jieba
jieba.initialize()
# jieba提前初始化，节省搜索时间
import json
import time

def home_page(request):# 首页
    l=[x for x in range(5000)]
    choice=random.sample(l,20)# 随机新闻id
    articles=[]
    for i in range(20):
        articles.append(ArticleInfo.objects.all()[choice[i]])# all取出所有新闻再切片
    context={'articles': articles}
    return render(request, 'article/home_page.html', context)

def article_page(request,id):# 新闻详情
    article=ArticleInfo.objects.get(id=id)# 取出新闻
    comments=Comment.objects.filter(article=id)# 取出对应评论
    context={'article':article,'body':'article/article_body/'+str(id)+".html",'comments':comments}
    # body为静态地址（为保持原图片文字排版位置，主体部分选择插入html）
    return render(request,'article/article_page.html',context)

def news_list(request):# 全部新闻页
    news_list=ArticleInfo.objects.all()
    paginator=Paginator(news_list, 20)# 分页
    page=request.GET.get('page')
    articles=paginator.get_page(page)
    context={'articles': articles, 'category': '全部新闻'}
    return render(request, 'article/news_list.html', context)

def category_list(request):# 分类页
    categories=[{'name':'August','num':'1001'},
                {'name':'July','num':'1152'},
                {'name':'June','num':'1156'},
                {'name':'May','num':'1185'},
                {'name':'April','num':'506'},]# 传递分类名称和数量给模板
    
    context={'categories':categories}
    return render(request,'article/category_list.html',context)

def category(request,id):# 分类列表类
    filtered=ArticleInfo.objects.filter(category=id).all()# filter过滤
    paginator=Paginator(filtered,20)
    page=request.GET.get('page')
    articles=paginator.get_page(page)
    context={'articles': articles, 'category':id}
    return render(request, 'article/news_list.html', context)

def comment_post(request,id):# 发送评论（接收POST请求）
    article=ArticleInfo.objects.get(id=id)# 取出评论的文章
    if(request.method !='POST'):# 请求异常
        return HttpResponse("Error: Comments can only be POSTed! ")
    comment_form=CommentForm(request.POST)
    if(not comment_form.is_valid()):# 表单不合法
        return HttpResponse("Error: Incorrect Comment Form! ")
    
    comment=comment_form.save(commit=False)# 不立即存入数据库（因为要修改信息）
    comment.article=article
    article.comment_num+=1 # 维护对应文章的评论数
    article.save()# 保存数据
    comment.save()
    return redirect("/article/"+str(id))# 返回文章详情

def comment_del(request,id):# 删除评论
    comment=Comment.objects.get(id=id)
    comment.article.comment_num-=1# 维护对应文章的评论数
    comment.article.save()
    id=comment.article.id
    comment.delete()
    return redirect("/article/"+str(id))

def search(request):# 搜索
    time1=time.time()# 计时开始
    wd=request.GET.get('word')
    word_list=jieba.lcut_for_search(wd)# 对搜索文本进行分词
    # 加载停用词
    s=open('dict/stopwords.txt','r',encoding='utf-8')
    sw=s.readlines()
    stop_words=[]
    for word in sw:
        word=word.replace('\n','')
        stop_words.append(word)
    s.close()
    # 加载预处理的倒排索引
    # d=open('dict/dic.json','r',encoding='utf-8')
    # dic=json.load(d)
    # d.close()
    # 对类别选择进行处理
    categories=['August','July','June','May','April']
    checked={}
    flag=True
    for i in categories:
        checked[i]=request.GET.get(i)
        if(checked[i]=='True'):
            checked[i]=True
            flag=False
        else:
            checked[i]=False
    if(flag):
        for i in categories:
            checked[i]=True

    # 去掉文本中的停用词
    word_list=[word for word in word_list if (word not in stop_words)] 
    
    d=Dic.objects.filter(name=word_list[0])
    if(not d):# 特判：第一个分词即无结果
        article_list=[]
    else:
        article_list=d[0].content[1:-1].split(', ')# 取出备选新闻编号列表
    for word_id in range(1,len(word_list)):# 通过后面的分词对新闻编号列表筛选
        d=Dic.objects.filter(name=word_list[word_id])
        if(not d):
            article_list=[]
            break
        article_list=[article_id for article_id in article_list if (article_id in str(d[0].content))]
        # article_list=[article_id for article_id in article_list if (article_id in dic[word_list[word_id]])]
        # if(not article_list):
        #     break
    
    # 通过新闻编号列表取出新闻，再根据分类筛选
    result=[]
    all_articles=list(ArticleInfo.objects.all())
    # 由于数据库大批量get很慢，因此先把新闻全部取出成list再筛选出搜索结果
    for article_id in article_list:
        article=all_articles[int(article_id)-1]
        if(checked[article.category]==True):
            result.append(article)

    # 默认编号即为时间倒序，对热度排序进行处理
    order=request.GET.get('order')
    if(order=='like'):
        result=sorted(result,key=lambda x:-x.like)
    
    paginator = Paginator(result, 20)
    page = request.GET.get('page')
    if(page):# href传递给模板方便分页跳转
        href=request.get_full_path().replace('page='+page,'page=')
    else:
        href=request.get_full_path()+'&page='
    articles = paginator.get_page(page)

    time2=time.time()# 计时结束
    context={'articles':articles, 'category':'搜索结果', 
             'cost':time2-time1,'href':href,'word':wd,'order':order}

    for i in categories:
        context[i]=checked[i]
    return render(request,'article/search_result.html',context)