#導入 Discord.py
import discord
from discord.ext import commands
from core.classes import Cog_Extension 
import json
import os
with open(os.path.join(os.path.dirname((os.path.dirname(__file__))),'setting.json'),'r',encoding='utf8') as jfile:
    jdata = json.load(jfile)
with open(os.path.join(os.path.dirname((os.path.dirname(__file__))),'on_message.json'),'r',encoding='utf8') as msgfile:
    mdata = json.load(msgfile)


class Event(Cog_Extension):
    #成員加入群組
    @commands.Cog.listener()
    async def on_member_join(self,member):
        channel = self.bot.get_channel(int(jdata["Welcome-channel"]))
        await channel.send(f'{member} 加入到死肥宅DC群')
        
        

    #成員離開群組
    @commands.Cog.listener()
    async def on_member_remove(self,member):
        channel = self.bot.get_channel(int(jdata["Remove-channel"]))
        await channel.send(f'{member} 離開了死肥宅DC群')

    #訊息觸發 機器人回復  
    @commands.Cog.listener()
    async def on_message(self,message):
        global timer
        #排除自己的訊息，避免陷入無限循環
        if message.author == self.bot.user:
            return
        #如果包含 !指令，機器人回傳 XXXXXX
        keyword = ['!指令','！指令']
        if message.content in keyword:
            print(list(mdata.keys()))
            await message.channel.send('```\n!GG長度\n!早點睡\n!閉嘴= =\n!尻尻\n!屌照\n!尻到死```')    
        # if message.content.startswith('我只能說'):
        #     await message.channel.send('說說說說 說你愛我<3')
        #     await message.channel.send('https://cdn.discordapp.com/emojis/935463005464956979.webp?size=96&quality=lossless')
        if message.content.startswith('閉嘴') or message.content.endswith('閉嘴'):
            await message.channel.send('不要叫人家閉嘴嘛...我只會張嘴<3')
        if message.content in list(mdata.keys()) :
            await message.channel.send(mdata[f'{message.content}'])           
        # if message.content == '!尻尻' or message.content =='！尻尻':
        #     await sendpic(message, 1)
        # if message.content == '!尻到死' or message.content =='！尻到死':
        #     await sendpic(message, 5)   
        # if message.content == '!定時' or message.content =='！定時':
            
        #     if(timer == 0):
                
        #         timer = 1
        #         await message.channel.send('啟動定時發圖')
        #         await timerf(message) 
        #     elif(timer == 1):
            
        #         timer = 0
        #         await message.channel.send('關閉定時發圖')

        # await bot.process_commands(message)

#註冊cog
async def setup(bot):
    await bot.add_cog(Event(bot))