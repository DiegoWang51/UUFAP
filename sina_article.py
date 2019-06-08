import re
import requests
from bs4 import BeautifulSoup
import json

class SinaArticle:

    def __init__(self, url):
        self.url = url
    
    def getnewsid(self):
        self.newsid = re.search("doc-i(.+)\.shtml",self.url).group(1)# group(1) returns contents in ()
    
    def getarticleinfo(self):
        newsid = self.newsid
        newsurl = "http://news.sina.com.cn/o/2017-05-10/doc-i"+newsid+".shtml"
        res = requests.get(newsurl)
        res.encoding = "utf-8"
        soup = BeautifulSoup(res.text,"html5lib")

        commentsurl = "http://comment5.news.sina.com.cn/page/info?version=1\
        &format=js&channel=gn&newsid=comos-"+newsid+"&group=&compress=0&ie=utf-8\
        &oe=utf-8&page=1&page_size=20"
        res_comments = requests.get(commentsurl)
        res_comments.encoding = "utf-8"
        jd = json.loads(res_comments.text.strip("var data="))# creates a dictionary

        title = soup.select("title")[0].text# or soup.title
        time = soup.select(".time-source")[0].contents[0].strip()
        #.contents returns a list with objects, .strip() returns a String and removes /t
        source = soup.select(".time-source span a")[0].text
        articlelist = []
        for p in soup.select("#artibody p")[:-1]:# id="artibody", paragraphs
            articlelist.append(p.text.strip())
        article = '\n'.join(articlelist)
        editor = soup.select(".article-editor")[0].text.lstrip("责任编辑：")
        comments_num = jd["result"]["count"]["total"]
        
        self.articleinfo = {"title":title, "source":source, "time":time, "article":article,\
                     "editor":editor,"comments_num":comments_num, "newsid":newsid}
    
    def printarticle(self):
        self.getnewsid()# use info in self to call the function, instead of giving parameter
        self.getarticleinfo()
        articleinfo = self.articleinfo
        print(articleinfo["title"])
        print(articleinfo["source"])
        print(articleinfo["time"])
        print(articleinfo["article"])
        print(articleinfo["editor"])
        print(articleinfo["comments_num"])
        print('\n'+articleinfo["newsid"])


if __name__ == "__main__":
    sampleurl = "http://news.sina.com.cn/o/2017-05-10/doc-ifyfecvz0805318.shtml"
    article = SinaArticle(sampleurl)
    article.printarticle()
