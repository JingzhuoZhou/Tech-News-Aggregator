# 实验报告

## 爬虫功能（crawler/）

爬取原网页为[新闻中心滚动新闻_新浪网](https://news.sina.com.cn/roll/)，数据量为5000条。

爬取数据信息包括：url（crawler_url.py）、标题、作者、正文、图片、时间（crawler_info.py）以及原文下方评论数&参与人数（crawler_data.py）

![62c5940c-0434-4105-85b4-5537b03b763b](file:///C:/Users/Qingjun/Pictures/Typedown/62c5940c-0434-4105-85b4-5537b03b763b.png)

info示例

![faabf9d5-3c81-40d0-9669-a771f91b318e](file:///C:/Users/Qingjun/Pictures/Typedown/faabf9d5-3c81-40d0-9669-a771f91b318e.png)

data示例

crawler_url.py及crawler_info.py采用requests及bs4库

crawler_data.py采用selenium框架

## 网页设计

### 基本情况

后端采用django框架，数据库通过import_export库批量导入爬虫及创建倒排索引（inverted-index/inverted_index.py）时保存的json文件，前端应用bootstrap进行美化（及fontsawesome的搜索&刷新按钮样式）

### 功能介绍

![ea40f87e-1b6d-4030-af34-f5cefaf4cfe0](file:///C:/Users/Qingjun/Pictures/Typedown/ea40f87e-1b6d-4030-af34-f5cefaf4cfe0.png)

### 

主页包括随机20条新闻展示（支持按钮刷新）和搜索（支持分类多选及排序单选）功能。

搜索功能使用jieba库中文分词，及手写倒排索引（数据存至数据库）。

主页可随时点击左上方名称跳转。

![4f2f8773-325a-432f-8c16-60c7b406a009](file:///C:/Users/Qingjun/Pictures/Typedown/4f2f8773-325a-432f-8c16-60c7b406a009.png)

新闻正文页包括所有原文信息（静态图片，且文字图片排列顺序与原网站顺序一致）。

左侧悬浮导航栏包括原网址和分类信息，二者均可直接跳转。

![3e45f7e7-1d9c-4ae4-ace4-62743a696f26](file:///C:/Users/Qingjun/Pictures/Typedown/3e45f7e7-1d9c-4ae4-ace4-62743a696f26.png)

正文页支持评论及删除功能，按时间倒序排列显示（评论条数会更新在每个列表页）。

![be749987-58ec-440d-9537-68bb9d7351e2](file:///C:/Users/Qingjun/Pictures/Typedown/be749987-58ec-440d-9537-68bb9d7351e2.png) 

新闻分类页可随时通过点击头部导航栏跳转，包括按时间的五个分类。每个分类可直接点击跳转对应分类列表页。

![59a8f436-abb7-4f20-b5d0-cd98e48faefe](file:///C:/Users/Qingjun/Pictures/Typedown/59a8f436-abb7-4f20-b5d0-cd98e48faefe.png)

上图为July分类列表页，下方有分页控件支持前一页、后一页、首页、尾页及输入跳转。

全部新闻列表类似分类列表页，可随时由上方导航栏跳转。

![293d7329-64d1-46d5-b787-34f6e9d4fc45](file:///C:/Users/Qingjun/Pictures/Typedown/293d7329-64d1-46d5-b787-34f6e9d4fc45.png)

搜索结果页类似分类列表页，加入搜索用时提示。

## 数据分析

见data-analyze/data-analyzing-report.md
