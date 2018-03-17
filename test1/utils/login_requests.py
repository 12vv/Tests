# -*- coding: utf-8 -*-

import requests
import PyV8
import re
from lxml import etree
from lxml import html

try:
    import cookielib
except:
    # python3
    import http.cookiejar as cookielib

import re

session = requests.session()

# r = session.get("https://segmentfault.com/user/login")
# token = r.cookies.items()[0][1]
# cookies = r.cookies
# 以下为测试，所获取的token及cookie的格式
# print(type(token))
# print(token)
# print(cookies)
# print(r.headers)
# print(r.url)


# cookies = {
#     "PHPSESSID": "web2~232788b24c557d5ed8511e79da7b03b1"
# }

# def get_xsrf():
#     response = requests.get("http://segmentfault.com")
#     print requests.text
#     return ""


def get_token(st):
    h = re.match('[\s\S]*\(function \(w\) \{[\s\S]+? \}\)\(window\);', st).group()
    print h

    with PyV8.JSContext() as ctxt:
        # ctxt.locals.window = {}
        ctxt.eval("""window={};\n""" + h)
        vars = ctxt.locals
        token_var = vars.window.SF.token
        print token_var

    return token_var


def login_test(account, password):
    response = requests.get('https://segmentfault.com/user/login')

    sel = html.fromstring(response.text)
    # print sel
    # print response.text
    s = sel.xpath('/html/body/script[8]/text()')[0]
    st = str(s.encode('utf-8'))
    # print st
    token = get_token(st)
    # response = requests.get("https://segmentfault.com", headers=header)
    url = "https://segmentfault.com/api/user/login"
    post_data = {
        "remember": 1,
        "username": account,
        "password": password
    }
    agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.162 Safari/537.36"
    header = {
        "HOST": "segmentfault.com",
        "Referer": "https://segmentfault.com/user/login",
        "User-Agent": agent,
        "token": token,
        "X-Requested-With": "XMLHttpRequest"
    }
    # cookies = {}
    cookies = response.cookies
    # for i in line:
    #     name, value = line.strip().split('=', 1)
    #     cookies[name] = value
    # print cookies
    post_url = url + "?_=" + token
    print post_url
    response = session.post(post_url, data=post_data, cookies=cookies, headers=header)
    print response.text

    response = session.get('https://segmentfault.com/user/draft', data=post_data, cookies=cookies, headers=header)
    # response = session.get("https://segmentfault.com/user/draft")
    print response.text




login_test("765864667@qq.com", "Akashi12")

