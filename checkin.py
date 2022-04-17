#!/usr/bin/env python3
"""
File: checkin.py
Project: nju-health-checkin
Author: Maxwell Lyu https://github.com/Maxwell-Lyu
-----
Last Modified: Tuesday, 28th December 2021 3:53:25 pm
Modified By: Antares (antares0982@gmail.com)
-----
Copyright (C) 2021 Maxwell Lyu
"""

import base64
import json
import os
import random

import requests
from bs4 import BeautifulSoup
from Crypto.Cipher import AES
from Crypto.Util import Padding


def encryptAES(_p0: str, _p1: str) -> str:
  _chars = list("ABCDEFGHJKMNPQRSTWXYZabcdefhijkmnprstwxyz2345678")

  def _rds(len: int) -> str:
    return "".join(random.choices(_chars, k=len))

  def _gas(data: str, key0: str, iv0: str) -> bytes:
    encrypt = AES.new(
      key0.strip().encode("utf-8"), AES.MODE_CBC, iv0.encode("utf-8")
    )
    return base64.b64encode(encrypt.encrypt(Padding.pad(data.encode("utf-8"), 16)))

  return _gas(_rds(64) + _p0, _p1, _rds(16)).decode("utf-8")


def to_shell_urltext(s: str) -> str:
  s = "%20".join(s.split())
  s = s.replace("{", r"\{")
  s = s.replace("}", r"\}")
  return s


def main():
  username = os.environ['NJU_USER']
  password = os.environ['NJU_PASS']

  # login
  url_login = r"https://authserver.nju.edu.cn/authserver/login"
  url_list = r"http://ehallapp.nju.edu.cn/xgfw/sys/yqfxmrjkdkappnju/apply/getApplyInfoList.do"
  session = requests.Session()
  response = session.get(url_login, proxies={})

  soup = BeautifulSoup(response.text, "html.parser")
  soup.select_one("#pwdDefaultEncryptSalt").attrs["value"]
  data_login = {
    "username": username,
    "password": encryptAES(
      password, soup.select_one("#pwdDefaultEncryptSalt").attrs["value"]
    ),
    "lt": soup.select_one('[name="lt"]').attrs["value"],
    "dllt": "userNamePasswordLogin",
    "execution": soup.select_one('[name="execution"]').attrs["value"],
    "_eventId": soup.select_one('[name="_eventId"]').attrs["value"],
    "rmShown": soup.select_one('[name="rmShown"]').attrs["value"],
  }

  # Solve CAPTCHA
  r = session.get("https://authserver.nju.edu.cn/authserver/needCaptcha.html?username=" + username)
  if r.text == "true":
    # CAPTCHA REQUIRED
    import muggle_ocr
    os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
    res = session.get("https://authserver.nju.edu.cn/authserver/captcha.html")
    sdk = muggle_ocr.SDK(model_type = muggle_ocr.ModelType.Captcha)
    captcha_text = sdk.predict(image_bytes = res.content)
    data_login["captchaResponse"] = captcha_text
  
  session.post(url_login, data_login)

  from pytz import timezone    
  from datetime import datetime
  
  time_str = datetime.now(timezone("Asia/Hong_Kong")).strftime("%Y-%m-%d %H:%M:%S")

  # get info
  raw = session.get(url_list)
  content = raw.json()

  # apply
  data = next(x for x in content["data"] if x.get("TJSJ") != "")

  data["WID"] = content["data"][0]["WID"]
  data["ZJHSJCSJ"] = "2022"
  fields = [
    "WID",
    "CURR_LOCATION",
    "IS_TWZC",  # 体温正常
    "IS_HAS_JKQK",  # 健康情况
    "JRSKMYS",  # 今日苏康码颜色
    "JZRJRSKMYS",  # 居住人今日苏康码颜色
    "SFZJLN",  # 是否最近离宁
    "ZJHSJCSJ"  # 最近核酸检测时间
  ]

  result = session.get(
    "http://ehallapp.nju.edu.cn/xgfw/sys/yqfxmrjkdkappnju/apply/saveApplyInfos.do?"
    + "&".join([key + "=" + data[key] for key in fields])
  )

  answer = json.loads(result.text)

  if result.status_code != 200:
    answer = f"Checkin failed with status code {result.status_code}"

  response = """
<b>✅ Health Check-in Success</b>
Location: {location}
Checkin time: {time} CST
Response: {answer}
  """.format(
    location = data["CURR_LOCATION"],
    answer = str(answer),
    time = time_str
  )

  import urllib.parse
  response = urllib.parse.quote(response)

  print(response)


if __name__ == "__main__":
  main()
