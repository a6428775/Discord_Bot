import os
import discord
import asyncio
from discord.ext import commands
import json
import os
from datetime import datetime, timezone, timedelta
from selenium import webdriver
from bs4 import BeautifulSoup as Soup
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time


async def shopee_coin2(self):
  # 新增時間GMT+8
  dt1 = datetime.utcnow().replace(tzinfo=timezone.utc)
  dt2 = dt1.astimezone(timezone(timedelta(hours=8)))  # 轉換時區 -> 東八區

  #Discord 傳送現在時間
  await self.channel.send('現在時間 : ' + dt2.strftime("%Y-%m-%d %H:%M:%S"))

  #今天講個特別的，我們可以不讓瀏覽器執行在前景，而是在背景執行（不讓我們肉眼看得見）
  #如以下宣告 options
  options = webdriver.ChromeOptions()
  #options.add_argument('--headless')
  options.add_argument('--disable-dev-shm-usage')
  options.add_argument('--no-sandbox')
  #反反爬蟲 去除 webdriver 特征
  options.add_argument("--disable-blink-features")
  options.add_argument("--disable-blink-features=AutomationControlled")

  #不顯示瀏覽器視窗
  browser = webdriver.Chrome(options=options)
  #讀取設定json檔
  with open(os.path.join(os.path.dirname((os.path.dirname(__file__))),'setting.json'),'r',encoding='utf8') as settingFile:
    settingdata = json.load(settingFile)
  #根據設定檔選擇讀取cookies方式
  if (settingdata["cookies_savetype"] == '1'):
    #讀取存放cookies的json檔
    with open(
        os.path.join(os.path.dirname((os.path.dirname(__file__))),
                     'cookies_shopee.json')) as f:
      cookies = json.load(f)
  elif (settingdata["cookies_savetype"] == '2'):
    channel = self.bot.get_channel(int(settingdata["shopee_cookies-channel"]))
    cookiesstr = ''
    async for message in channel.history(limit=10, oldest_first=True):
      cookiesstr = cookiesstr + message.content

    cookies = cookiesstr.replace('*', '')
    cookies = json.loads(cookies)
      

  #開啟蝦皮簽到網站網址
  browser.get('https://shopee.tw/shopee-coins')
  print("開啟蝦皮簽到網站網址")
  #載入cookie
  try:
    for cookie in cookies:
      #刪除cookies中sameSite部分 不然會報錯
      try:
        cookie.pop('sameSite')
      except:
        None
      browser.add_cookie(cookie)
    print("載入cookie")
    #重新整理網頁
    browser.refresh()
    print("重新整理網頁完成")
    await asyncio.sleep(8)
  except:
    print('cookies失效 改用帳密登入')
    await self.channel.send('cookies失效 改用帳密登入')

  #判斷是否有登入成功 如cookies 登入失敗改用帳密登入並儲存新的cookies
  login = browser.find_element(
    By.CLASS_NAME,
    'pcmall-dailycheckin_3u8jig.pcmall-dailycheckin_3uUmyu.pcmall-dailycheckin_1EAaO5'
  )
  if login.text == '登入以獲得蝦幣':

    browser.get(
      'https://shopee.tw/buyer/login?next=https%3A%2F%2Fshopee.tw%2Fshopee-coins'
    )
    await asyncio.sleep(10)
    #輸入帳號欄位
    browser.find_element(By.NAME,
                         'loginKey').send_keys(str(os.getenv("shopee_act")))
    await asyncio.sleep(3)
    #輸入密碼欄位
    browser.find_element(By.NAME,
                         'password').send_keys(str(os.getenv("shopee_pwd")))
    await asyncio.sleep(3)
    #點擊登入按鈕
    browser.find_element(
      By.CLASS_NAME, 'wyhvVD._1EApiB.hq6WM5.L-VL8Q.cepDQ1._7w24N1').click()
    await asyncio.sleep(8)

    #獲取當前cookies資訊並儲存
    my_cookies = browser.get_cookies()

    #根據設定檔選擇儲存cookies方式
    #儲存在cookies_shopee.json檔 (私人儲存空間/伺服器)
    if(settingdata["cookies_savetype"]=='1'):
        
      with open(
          os.path.join(os.path.dirname((os.path.dirname(__file__))),
                      'cookies_shopee.json'), 'w') as f:
        f.write(json.dumps(my_cookies))
    #儲存在 DC 私人頻道內 因有限制字數2000內 將cookies 分段儲存
    elif (settingdata["cookies_savetype"] == '2'):
      channel = self.bot.get_channel(int(settingdata["shopee_cookies-channel"]))

      #先清空舊的cookies資訊
      await channel.purge(limit=15)

      my_cookies = json.dumps(my_cookies)
      my_cookies_length = len(str(my_cookies))
      #每1750字為一段
      i = 1750
      j = 0
      for num in range(0, int(my_cookies_length / 1750 + 1)):
        await channel.send('**' + str(my_cookies)[j:i] + '**')
        j = i
        i = i + 1750


    #跳轉回蝦皮簽到頁面
    await asyncio.sleep(8)
    browser.get('https://shopee.tw/shopee-coins')
    await asyncio.sleep(8)


    

  #解析網頁原始碼
  soup = Soup(browser.page_source, "lxml")

  await asyncio.sleep(6)
  print("解析網頁原始碼完成")

  #獲取網頁所有的按鈕原始碼
  findBtn = soup.find_all('button')

  print("開始找尋簽到的按鈕")
  for btn in findBtn:
    #       找尋簽到的按鈕
    if '完成簽到' in btn.getText():
      #取得簽到按鈕的CLASS_NAME
      BTN_CLASS_NAME = btn.get("class")[0]
      #蝦皮簽到
      browser.find_element(By.CLASS_NAME, BTN_CLASS_NAME).click()

      await self.channel.send('簽到成功 : ' + btn.getText()[btn.getText().find('獲得'):])

      print("簽到成功")
      break
    elif '明天再回來' in btn.getText():
      #今天已簽到
      await self.channel.send('今天已簽到過,明天再來')
      print("今天已簽到過,明天再來")
      break
    elif '快來登入領蝦幣' in btn.getText():
      await self.channel.send('找不到簽到按鈕,可能是cookies過期')
      print("找不到簽到按鈕,可能是cookies過期")
      break

  #獲得目前蝦幣數量
  findCoinCount = browser.find_element(By.CLASS_NAME,'pcmall-dailycheckin_2ixaiI').text
  await asyncio.sleep(3)
  await self.channel.send('目前擁有蝦幣數量 : ' + findCoinCount)
  browser.quit()
