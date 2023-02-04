#導入 Discord.py
import discord
from discord.ext import commands
from core.classes import Cog_Extension
from datetime import datetime,timezone,timedelta
import openai
import asyncio
import requests
import pandas
dt1 = datetime.utcnow().replace(tzinfo=timezone.utc)
dt2 = dt1.astimezone(timezone(timedelta(hours=8))) # 轉換時區 -> 東八區
import taskfile.shopee_coin as sc
 
class Main(Cog_Extension):
    #目前機器人延遲時間
    @commands.command()
    async def ping(self,ctx):
        await ctx.send(f'{round(self.bot.latency*1000)} (ms)')

    
    #embed 嵌入訊息
    @commands.command()
    async def em(self,ctx):
        embed=discord.Embed(title="下一屆岡山區信義里里長候選人", url="https://www.facebook.com/trolltrollriven", description="about the 義守空幹王", color=0x1fc3f9,timestamp=dt2)
        embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/892510884746891334/974926111425323038/ezgif-7-4bb934133a.gif")
        embed.add_field(name="身高", value="161cm", inline=True)
        embed.add_field(name="體重", value="80kg", inline=True)
        embed.add_field(name="下面", value="30mm", inline=True)
        embed.add_field(name="地址", value="大義二路 元寶XXX", inline=True)
        await ctx.send(embed=embed)

    # 機器人複誦訊息
    @commands.command()
    async def sayd(self,ctx,*,msg):
        await ctx.message.delete()
        await ctx.send(msg)
    # 機器人刪除幾條訊息
    @commands.command()
    async def clean(self,ctx,num:int):
        await ctx.channel.purge(limit=num+1)

    #套用openai
    @commands.command()
    async def aibot(self,ctx,msg):
        await openaibot(ctx,msg)
    
    #台彩世足賠率
    @commands.command(name='賠率')
    async def Lottery(self,ctx):
        await point(ctx)


#取得台彩世足賠率
async def point(ctx):
    res = requests.get('https://blob.sportslottery.com.tw/apidata/Live/Register.json')

    jd = res.json()

    ary = []
    for rec in jd:
        game_type = rec.get('cn')[0]
        if game_type == '國際賽(國家)':
            atn = rec.get('atn')[0]
            htn = rec.get('htn')[0]
            try:
                for ms in rec.get('ms'):
                    for cs in ms.get('cs'):
                        win = cs[0].get('o')
                        tie = cs[1].get('o')
                        loss = cs[2].get('o')
                ary.append({'game_type': game_type, '主':atn, '客':htn, '主勝':win, '和局':tie, '客勝':loss})
            except :
                print()

        df = pandas.DataFrame(ary)

    await ctx.send(df)





#openai chat api
async def openaibot(ctx,msg):

    try :

        openai.api_key = ('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')

        response = openai.Completion.create(
        model="text-davinci-003",
        prompt=msg,
        temperature=0.9,
        max_tokens=2048,
        top_p=1,
        frequency_penalty=0.0,
        presence_penalty=0.6,
        stop=[" Human:", " AI:"]
        )
        await asyncio.sleep(0.5)

        await ctx.send(response["choices"][0]["text"])

    except:
        await ctx.send('別問這什麼雞巴洨,老子不知道')




#註冊cog       
async def setup(bot):
    await bot.add_cog(Main(bot))