import discord
import asyncio
from discord.ext import commands
from core.classes import Cog_Extension
import json
import os
from datetime import datetime, timezone, timedelta
from selenium import webdriver
from bs4 import BeautifulSoup as Soup
from selenium.webdriver.chrome.options import Options
import random
import time
import taskfile.shopee_coin as sc
import taskfile.exchange_rate as rate
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager

# dt1 = datetime.utcnow().replace(tzinfo=timezone.utc)
# dt2 = dt1.astimezone(timezone(timedelta(hours=8))) # 轉換時區 -> 東八區
#現在時間格式化
#dt2.strftime("%H:%M:%S")


class Task(Cog_Extension):

  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)

    # 間隔時間
    # async def interval():
    #     #等待機器人啟動再執行
    #     await self.bot.wait_until_ready()
    #     self.channel = self.bot.get_channel(1043062121790967849)
    #     while not self.bot.is_closed():
    #         await self.channel.send("HI")
    #         await asyncio.sleep(5) #單位 (秒)

    # self.bg_task = self.bot.loop.create_task(interval())

    #設置條件
    self.counter = 0

    #指定時間
    async def time_task():
      #等待機器人啟動再執行
      await self.bot.wait_until_ready()

      while not self.bot.is_closed():
        dt1 = datetime.utcnow().replace(tzinfo=timezone.utc)
        dt2 = dt1.astimezone(timezone(timedelta(hours=8)))  # 轉換時區 -> 東八區
        now_time = dt2.strftime("%H:%M")
        with open(os.path.join(os.path.dirname((os.path.dirname(__file__))),
                               'setting.json'),
                  'r',
                  encoding='utf8') as jfile:
          jdata = json.load(jfile)
        #每日匯率
        if now_time in jdata['rate_time'] and self.counter == 0:
          self.channel = self.bot.get_channel(1070285248585281566)
          self.counter = 1
          await self.channel.send('今日匯率如下')
          try:
            await rate.exchange_rate(self)
          except:
            await self.channel.send('無法取得今日匯率,請維修')
          await asyncio.sleep(60)
          self.counter = 0
        #蝦皮簽到

        if now_time in jdata['time'] and self.counter == 0:
          self.channel = self.bot.get_channel(1070285440445333573)
          self.counter = 1
          await self.channel.send('開始執行蝦皮自動簽到')
          # await sendpic(self,5)
          try:
            await sc.shopee_coin2(self)
          except:
            await self.channel.send('蝦皮簽到功能出錯,請維修')
          await asyncio.sleep(60)
          self.counter = 0
        else:
          await asyncio.sleep(1)
          pass

    self.bg_task = self.bot.loop.create_task(time_task())

  @commands.command()
  async def set_channel(self, ctx, ch: int):
    self.channel = self.bot.get_channel(ch)
    await ctx.send(f'set_channel : {self.channel.mention} ')

  @commands.command()
  async def set_time(self, ctx, *time):
    # self.counter = 0
    with open(os.path.join(os.path.dirname((os.path.dirname(__file__))),
                           'setting.json'),
              'r',
              encoding='utf8') as jfile:
      jdata = json.load(jfile)

    jdata['time'] = time
    with open(os.path.join(os.path.dirname((os.path.dirname(__file__))),
                           'setting.json'),
              'w',
              encoding='utf8') as jfile:
      json.dump(jdata, jfile, indent=4)


############
async def sendpic(self, count: int):

  # 新增時間
  dt1 = datetime.utcnow().replace(tzinfo=timezone.utc)
  dt2 = dt1.astimezone(timezone(timedelta(hours=8)))  # 轉換時區 -> 東八區
  await self.channel.send('阿臣臣報時 現在時間 : ' + dt2.strftime("%Y-%m-%d %H:%M:%S")
                          )  # 將時間轉換為 string

  #今天講個特別的，我們可以不讓瀏覽器執行在前景，而是在背景執行（不讓我們肉眼看得見）
  #如以下宣告 options
  options = webdriver.ChromeOptions()
  options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
  options.add_argument('--headless')
  options.add_argument('--disable-dev-shm-usage')
  options.add_argument('--no-sandbox')
  # 不顯示瀏覽器
  # browser = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), chrome_options=options)
  # 顯示瀏覽器
  browser = webdriver.Chrome(
    service=ChromeService(ChromeDriverManager().install()))
  # browser = webdriver.Chrome("D:\程式語言\Discord\chromedriver.exe")
  # driver.get(url)

  with open(
      os.path.join(os.path.dirname((os.path.dirname(__file__))),
                   'cookies_jar.json')) as f:
    cookies = json.load(f)

  browser.get('https://www.instagram.com/')

  for cookie in cookies:
    browser.add_cookie(cookie)
  browser.refresh()

  await asyncio.sleep(2)

  #jing 調整 start
  urlPrefix = 'https://instagram.com/'

  #更新這個清單就好
  insAccList = [
    '__mii04', 'janie.lin', 'pyoapple', 'cathrynli', 'kiki_hsieh',
    'asukakiraran', 'miyami176', 'umy510266', 'ms_puiyi', 'alinitydivine',
    'nana.un', 'vernalu49', 'kizunasakura', 'angelakuo0504', 'yolo_ioo',
    'yua_mikami', 'woowoowu.qq', 'thisisshl', 'imfaithxo', 'yuchinjou',
    'inkyung97', 'czz_mz', 'iamlove0410', 'demi59487', '920924jasmine',
    'jessie_199711', 'eyes198877', 'catherine0113', 'niny1212_', 'liz___85',
    'kuanting1003', 'u.710', 'qun_04', 'miss_any', 'yi_______07', 'sallymee',
    'changyachuu', 'sunnyrayyxo', 'diorwynn', 'irenelin0413', 'lillywhite',
    'boygirl.god', 'm.a.m.a.s.i.t.a', 'tehhan', 'kannachan__', '155cm_____',
    'xiaojie._.1218', '36d_yy', 'kitty770126', 'tokbaes'
  ]
  i = 0
  while (i < count):
    #亂數取帳號
    accIndex = random.randrange(len(insAccList))
    url = urlPrefix + insAccList[accIndex]

    #連到特定帳號
    browser.get(url)
    await asyncio.sleep(2)

    soup = Soup(browser.page_source, "lxml")
    await asyncio.sleep(2)

    #確保程式能執行完畢
    try:
      #檢查帳號是否存在
      if insAccList[accIndex] in soup.title.text.lower():
        #檢查是否為公開帳號
        privateMsg = soup.find_all('h2', class_='_aa_u')
        await asyncio.sleep(2)
        if len(privateMsg) == 0:
          #取文章
          allPost = soup.find_all('div', class_='_aagv')
          await asyncio.sleep(2)
          #亂數取文章編號
          postIndex = random.randrange(0, len(allPost))
          await asyncio.sleep(1)
          #取圖片src
          img_frame = allPost[postIndex].img.get('src')
          await self.channel.send(img_frame)
    except:
      print('取圖失敗')
      await self.channel.send('獲取圖片失敗 請稍後再試')
    #jing 調整 end

    i += 1  #避免程式卡死 抓到不存在or私人帳號還是會增加計數

  await self.channel.send('讚啦 好想做愛')
  print("機器人已傳送訊息")


#註冊Task cog
async def setup(bot):
  await bot.add_cog(Task(bot))
