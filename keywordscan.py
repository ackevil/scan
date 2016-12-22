#encoding:utf-8
import requests
from bs4 import BeautifulSoup
import traceback
import urlparse
import urllib
#pn 第几个开始 显示rn个https://www.baidu.com/s?
def getUrls(word,pn,rn):
    url="https://www.baidu.com/s?wd="+urllib.quote(word)+"&pn="+str(pn)+"&rn="+str(rn)+"&utf-8"
    headers = {'user-agent': "Mozilla/5.0 (X11; Linux x86_64; rv:45.0) Gecko/20100101 Firefox/45.0"}
    print(url)
    r=requests.get(url,headers=headers, timeout=30)
    html=r.text
    soup = BeautifulSoup(html,'html.parser')
    tags=soup.find_all("a",attrs={"class": "c-showurl"})
    for tag in tags:
        attrs =tag.attrs
        for name in attrs:
            try:
                if name == "href":
                    heads=requests.get(attrs[name],allow_redirects=False,timeout=30).headers
                    l=heads['Location']
                    f2.write(l+"\n")
                    print(l)
            except Exception:
                traceback.print_exc()

if __name__=="__main__":
    f=open("keyword.txt","r")
    f2=open("urls.txt","w")
    keywords=f.readlines()
    for keyword in keywords:
        for i in range(15):
            getUrls(keyword,i*50,50)
    
