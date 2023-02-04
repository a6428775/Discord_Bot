import discord
import asyncio
from discord.ext import commands
import json
import os
from datetime import datetime,timezone,timedelta
from selenium import webdriver
from bs4 import BeautifulSoup as Soup
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time

async def shopee_coin2(self):
    # 新增時間GMT+8    
    dt1 = datetime.utcnow().replace(tzinfo=timezone.utc)
    dt2 = dt1.astimezone(timezone(timedelta(hours=8))) # 轉換時區 -> 東八區

    #Discord 傳送現在時間
    await self.channel.send('現在時間 : ' + dt2.strftime("%Y-%m-%d %H:%M:%S"))

    #今天講個特別的，我們可以不讓瀏覽器執行在前景，而是在背景執行（不讓我們肉眼看得見）
    #如以下宣告 options
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--no-sandbox')
    #不顯示瀏覽器視窗
    browser = webdriver.Chrome(options= options)


    #讀取存放cookies的json檔
    with open(os.path.join(os.path.dirname((os.path.dirname(__file__))),'cookies_shopee.json')) as f:
        cookies = json.load(f)

    #開啟蝦皮簽到網站網址
    browser.get('https://shopee.tw/shopee-coins')

    #載入cookie
    for cookie in cookies:
        browser.add_cookie(cookie)
    #重新整理網頁
    browser.refresh()

    await asyncio.sleep(2)

    #解析網頁原始碼
    soup = Soup(browser.page_source,"lxml")

    await asyncio.sleep(2)

    #獲取網頁所有的按鈕原始碼
    findBtn = soup.find_all('button')

    for btn in findBtn:
#       找尋簽到的按鈕
        try:       
            if '今日簽到獲得' in btn.getText():            
                #取得簽到按鈕的CLASS_NAME
                BTN_CLASS_NAME = btn.get("class")[0]
                #蝦皮簽到
                browser.find_element(By.CLASS_NAME,BTN_CLASS_NAME).click()
                await self.channel.send('簽到成功')
                break
            elif '明天再回來領取' in btn.getText():
                #今天已簽到
                await self.channel.send('今天已簽到過,明天再來')
                break
        except:
            await self.channel.send('找不到簽到按鈕,可能是cookies過期')
