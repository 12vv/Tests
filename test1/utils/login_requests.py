# -*- coding: utf-8 -*-

import requests
try:
    import cookielib
except:
    # python3
    import http.cookiejar as cookielib

import re


def get_xsrf():
    response = requests.get("http://www.zhuhu.com")
    print requests.text
    return ""

# def login_test(account, password):
#     if re.match("^1\d{10}", account):
#         print("use phone number")
#         post_url = "http://www.zhuhu.com/login/phone_num"
#         post_data = {
#             "_xsrf":
#         }
