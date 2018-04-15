## 简介

这是一个爬取lofter文章的小爬虫程序，采用[Scrapy](https://scrapy.org/)框架，更多内容可参考[官方文档](https://docs.scrapy.org/en/latest/)


## 如何使用

1. 修改 `lofter/lofter/spiders/article_spider.py`中的`start_urls`，更改成要爬取的第一个页面，此处默认以榜单首页爬起，共50页，如果tag不多也可以按时间顺序全爬。

如:

```python

class LofterArticleSpider(Spider):
    name = "lofter" # 此处{name}改成lofter的tag名，注意，中文可能会显示转码，不必担心
    start_urls = [
        "http://{name}.lofter.com/total?page=1" 
    ]

```


2. 执行下面命令

```bash
virtualenv -p python3 .env
source .env/bin/activate

pip install -r requirements.txt -i  https://mirrors.aliyun.com/pypi/simple/

cd lofter/ && mkdir articles
scrapy crawl lofter

```

3. 最终文章将保存在lofter/articles目录下


注意： 因为网络问题可能会卡住，将url中的page参数修改为之前爬到的页数并保存，关掉进程重启即可。



