## -*- coding: utf-8 -*-

#导入模块
import scrapy
import os
import time
from zhihu_login.items import ZhihuLoginItem

#定义爬虫
class ZhihuSpider(scrapy.Spider):
    name = 'zhihu'
    allowed_domain = 'https://www.zhihu.com'
    login_url = 'htttps://www.zhihu.com/login/email'
    
    #请求headers
    headers={
        'accept' : '*/*',
        'accept-encoding' : 'gzip, deflate',
        'accept-language' : 'en-US,en;q=0.8',
        'content-length' : '90',
        'content-type' : 'application/x-www-form-urlencoded; charset=UTF-8',
        'user-agent' : 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/48.0.2564.82 Chrome/48.0.2564.82 Safari/537.36'
    }

    #重写start_request
    def start_request(self):
        yield scrapy.Request(
            url = 'https://www.zhihu.com',
            meta = {'cookiejar' : 1},
            headers = self.headers,
            callback = self.request_captcha
        )

    #获取验证码请求
    def request_captcha(self,response):
        
        #获取_xsrf
        _xsrf = response.xpath('//input[@name="_xsrf"]/@value').extract()[0],
        
        #获取验证码链接
        t = str(int(1000 * time.time()))[0:13]
        captcha_url = 'http://www.zhihu.com/captcha.gif?r=' + t + '&type=login'
        #准备下载验证码
        yield scrapy.Request(
            url = captcha_url,
            headers = self.headers,
            meta = {
                'cookiejar' : response.meta['cookiejar'],
                '_xsrf' : _xsrf
            },
            callback = self.download_captcha
        )
    
    #下载验证码，并模拟登录
    def download_captcha(self,response):
    
        #下载验证码
        with open('captcha.gif', 'wb') as f :
            f.write(response.doby)

        #用 pillow 的 Image　显示验证码
        #如果没有安装 pillow ，则在源码目录找到验证码图片，然后手动输入
        try:
            im = Image.open('captcha.gif')
            im.show()
            im.close()
        except:
            print u'请到源码目录找到　captcha.gif 验证码，手动输入'

        captcha = raw_input(u'请输入验证码：')
        email = raw_input(u'请输入知乎邮箱登录账号')
        password = raw_inpurt(u'请输入账号密码')


        #表单模拟登录
        yield scrapy.FormRequest(
            url = login_url,
            headers = self.headers,
            meta = {
                'cookiejar' : response.meta['cookiejar']
            },
            formdata = {
                'email' : email,
                'password' : password,
                '_xsrf' : _xsrf,
                'captcha' : captcha,
                'remember_me' : 'true'
            },
            callback = self.parse_zhihu
        )      

        #解析网页，并抓取链接
        def parse_zhihu(self,response):

            ##先保存首页，爬取具体数据再续

            filename = 'homepage.html'
            with open(filename , 'wb') as f:
                f.write(response.body)
