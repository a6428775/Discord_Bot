import pandas
import asyncio
import json
import os
from datetime import datetime, timezone, timedelta
from selenium import webdriver
from bs4 import BeautifulSoup as Soup
from selenium.webdriver.common.by import By

#參考資料 : https://www.youtube.com/watch?v=-c5rrzjsN34
pandas.set_option('display.unicode.ambiguous_as_wide', True)  # 将模糊字符宽度设置为2
pandas.set_option('display.unicode.east_asian_width', True)  # 检查东亚字符宽度属性


async def exchange_rate(self):
  # 新增時間GMT+8
  dt1 = datetime.utcnow().replace(tzinfo=timezone.utc)
  dt2 = dt1.astimezone(timezone(timedelta(hours=8)))  # 轉換時區 -> 東八區

  #Discord 傳送現在時間
  await self.channel.send('現在時間 : ' + dt2.strftime("%Y-%m-%d %H:%M:%S"))

  dfs = pandas.read_html('https://rate.bot.com.tw/xrt?Lang=zh-TW')
  currency = dfs[0].iloc[:, 0:5]
  currency.columns = [
    u'幣別', u'現金匯率-本行買入', u'現金匯率-本行賣出', u'即期匯率-本行買入', u'即期匯率-本行賣出'
  ]
  currency[u'幣別'] = currency[u'幣別'].str.extract('\((\w+)\)')

  await self.channel.send('`' + str(currency) + '`')
