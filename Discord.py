import time
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup as Soup
from selenium.webdriver.chrome.options import Options
import os
import json
from datetime import datetime, timezone, timedelta
import keep_alive
#導入 Discord.py
import discord
import random
import asyncio

with open(os.path.join(os.path.dirname(__file__), 'setting.json'),
          'r',
          encoding='utf8') as jfile:
  jdata = json.load(jfile)
#client 是我們與 Discord 連結的橋樑
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

from discord.ext import commands
# client = discord.Client(command_prefix='[',intents=intents)
bot = commands.Bot(command_prefix="$", intents=intents)


#調用 event 函式庫
@bot.event
#當機器人完成啟動時
async def on_ready():
  print('目前登入身份：', bot.user)


#讀取 其他class py
async def load_ext():
  for Filename in os.listdir(os.path.join(os.path.dirname(__file__),
                                          'method')):
    if Filename.endswith('.py'):
      print(f'載入 {Filename} 檔案')
      await bot.load_extension(f'method.{Filename[:-3]}')


@bot.command()
async def load(ctx, extension):
  await bot.load_extension(f'method.{extension}')
  await ctx.send(f'Loaded {extension} done.')


@bot.command()
async def unload(ctx, extension):
  await bot.unload_extension(f'method.{extension}')
  await ctx.send(f'Un - Loaded {extension} done.')


@bot.command()
async def reload(ctx, extension):
  await bot.reload_extension(f'method.{extension}')
  await ctx.send(f'Re - Loaded {extension} done.')


#TOKEN 在 Discord Developer 那邊「BOT」頁面裡面
if __name__ == "__main__":

  async def main():
    async with bot:
      await load_ext()
      await bot.start(jdata["TOKEN"])


keep_alive.keep_alive()
asyncio.run(main())

#原IG登入 已死
# # 等待按鈕出現
# WebDriverWait(browser, 20).until(EC.presence_of_element_located((By.CLASS_NAME, '_acan._acap._acas')))
# # 找到登入按鈕
# button = browser.find_elements(By.CLASS_NAME,'_acan._acap._acas')[0]
# # 找到帳號密碼輸入框 # 輸入帳號密碼
# browser.find_element(By.NAME,'username').send_keys('fktestbot')
# browser.find_element(By.NAME,'password').send_keys('aabb1111')
# print("輸入帳密成功")

# # 點擊登入按鈕
# button.click()
# print("登入成功")

# time.sleep(3)
# # 等待稍後再說出現
# WebDriverWait(browser, 20).until(EC.presence_of_element_located((By.CLASS_NAME, '_acan._acao._acas')))
# # 找到稍後再說按鈕
# button1 = browser.find_elements(By.CLASS_NAME,'_acan._acao._acas')[0]
# # 點擊稍後再說按鈕
# button1.click()
# print("關閉稍後再說成功")

# time.sleep(2)
