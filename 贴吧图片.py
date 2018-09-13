# -*- coding: utf-8 -*-
"""
步骤
    1、获取贴吧主页的URL
        http://tieba.baidu.com/f?kw=河南大学&pn=0
        http://tieba.baidu.com/f?kw=河南大学&pn=50
    2、获取每个帖子的URL,//div[@class='t_con cleafix']/div/div/div/a/@href
        https://tieba.baidu.com/p/5878699216
    3、打开每个帖子，找到图片的URL,//img[@class='BDE_Image']/@src
        http://imgsrc.baidu.com/forum/w%3D580/sign=da37aaca6fd9f2d3201124e799ed8a53/27985266d01609240adb3730d90735fae7cd3480.jpg
    4、保存到本地
    
"""
import requests
from lxml import etree
class TiebaPicture:
    def __init__(self):
        self.baseurl = "http://tieba.baidu.com"
        self.pageurl = "http://tieba.baidu.com/f"
        self.headers = {'User-Agent':"Mozilla5.0/"}
      
    
    def getPageUrl(self,url,params):
        '''获取每个帖子的URL'''
        res = requests.get(url,params=params,headers = self.headers)
        res.encoding = 'utf-8'
        html = res.text

        #从HTML页面获取每个帖子的URL
        parseHtml = etree.HTML(html)
        t_list = parseHtml.xpath("//div[@class='t_con cleafix']/div/div/div/a/@href")
        print(t_list)
        for t in t_list:
            t_url = self.baseurl + t
            self.getImgUrl(t_url)
        
    
    def getImgUrl(self,t_url):
        '''获取帖子中所有图片的URL'''
        res = requests.get(t_url,headers=self.headers)
        res.encoding = "utf-8"
        html = res.text
        parseHtml = etree.HTML(html)
        img_url_list = parseHtml.xpath("//img[@class='BDE_Image']/@src")
        for img_url in img_url_list:
            self.writeImg(img_url)

    
    
    def writeImg(self,img_url):
        '''将图片保存如文件'''
        res = requests.get(img_url,headers=self.headers)
        html = res.content
        #保存到本地,将图片的URL的后10位作为文件名
        filename = img_url[-10:]
        with open(filename,'wb') as f:
            print("%s正在下载"%filename)
            f.write(html)
            print("%s下载完成"%filename)

    def workOn(self):
        '''主函数'''
        kw = input("请输入你要爬取的贴吧名")
        begin = int(input("请输入起始页"))
        end = int(input("请输入终止页"))
        for page in range(begin,end+1):
            pn = (page-1)*50
            #拼接某个贴吧的URl
            params = {"kw":kw,"pn":pn}
            self.getPageUrl(self.pageurl,params=params)
            
if __name__ == "__main__":
    spider = TiebaPicture()
    spider.workOn()
    