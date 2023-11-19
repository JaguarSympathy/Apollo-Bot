import discord
from discord.ext import commands
from discord import app_commands
import roblox
import random
import json
import string

TOKEN = "MTE0NjU3MzMzMTI5MDY3MzIyMg.Gygi9K.x30DzogeiihJ_7VQpuLtGltTagjpAPzwugN90c"
ROTOKEN = "CEA35A71C8D3278A0FFABEE140A79947287582FB5AFEB5233643BAA45761338F69FE4DE7DD6F306E6244EB6574A26C9A93D0013F2073A14112618652837DC0CEDB9D04B794F12B4EF6ED5C41BD5B3C652BBA9D33D7577284A0EA9B6E77E981ABBBD6F2C655C8DD1CB6427B40F9D9A6DCFC5FD98D4222926C5E73F83FAF7B3368B59F14BE4EB8B08EFA40486BAD5F8235A1FA32F89B33658C54FC38AE7B32F05D0E7D53313460AFCB7DF58EF7462F643EE70626BF2013FC974287BFFE47CB2DACAA33995C952522EF06BCAE537AE57BB44543EAA76B346C4957DDC50E6FCE83A686105AEDB0A4D4DD615B08E7FDA16FD87A5AF37F64CA933A4893FEAE0D16AB7055691150904DB7DDC75B4F373A828FFADA4AF465865C3B66649501BFB51AF4CDBA362EDB429219222FD3E7CE80F76F48646553B90A87F1F7CFA252B697BBFEB19E81F3CB116662CB7FC14A21480E3D694E34E78624F08DB12AF9C4F40081D541FFEA53495C8A68E7779152E37036E2A2893ABC8F8F97198B7C998A1970D2C6A95E752CEA20595F9C9DFFD869E9148ADD6B84DA027C85E172EE3A8907030FEB914101FD688209E850D801E2D9DD4812AF70CDBC21CDF837E835AD713D94B56BC95E94388A1609637762F05C6BB451BB41D3E37A78"

client = discord.Client(intents=discord.Intents.all())
roClient = roblox.Client(token=ROTOKEN)
tree = discord.app_commands.CommandTree(client)
codes = {}

with open("C:/Users/MatthewWade/OneDrive - St Edmunds School/Desktop/Apollo/Apollo/database.json") as f:
    database = json.load(f)

async def log(msg):
    logs = await client.fetch_channel(1146565921037627453)
    await logs.send(msg)

@client.event
async def on_ready():
    print("Apollo Online")
    await client.change_presence(status=discord.Status.online,activity=discord.CustomActivity(name="Management @ Apollo Systems"))
    await tree.sync()

@tree.command(name="verify",description="Verify your account")
@app_commands.describe(account="Account to verify")
async def verify(cmd: discord.Interaction,account: str):
    try: 
        user = await roClient.get_user_by_username(account)
    except: 
        cmd.response.send_message("Invalid account name.")

    try: 
        if codes[user.name] in user.description:
            database[user.name] = "Verified"
            await cmd.user.edit(nick=user.name)
            await cmd.response.send_message(f"Successfully verified as `{account}`. You can now delete your code from your profile.")
            await log(f"`{cmd.user.display_name} ({cmd.user.name})` has verified as `{account}`.")
        else:
            await cmd.response.send_message(f"Please put {codes[user.name]} in your roblox profile description!")
    except:
        letters = string.ascii_lowercase
        result = ""
        for i in range(0,10):
            result = list(result)
            result = result.append(random.choice(letters))
            result = str(result)
            
        codes[user.name] = result
        await cmd.response.send_message(f"Please put {codes[user.name]} in your roblox profile description and run </verify:1172956138489254041> again.")

    with open("C:/Users/MatthewWade/OneDrive - St Edmunds School/Desktop/Apollo/Apollo/database.json","w") as f:
        json.dump(database,f)

@tree.command(name="estimate",description="For Staff use")
async def estimate(cmd: discord.Interaction):
    embed = discord.Embed()
    embed.set_author(name="Staff Team @ Apollo")
    embed.add_field(name="",value="The estimate provided above is a reflection of average price ranges. All prices are subject to negotiation and Apollo Systems' own discretion. Estimates should not be taken as final prices.")
    embed.set_footer(text="Apollo Systems",icon_url="https://images-ext-1.discordapp.net/external/Np5C1pTnH-TzpjkymlStLb11uB_JqKsCgX56Tqn8ykc/https/tr.rbxcdn.com/0d0c68b68e1073c8c91b9cf29e98af4b/150/150/Image/Png")
    await cmd.channel.send(embed=embed)
    await cmd.response.send_message(content="Sent embed",ephemeral=True)

client.run(TOKEN)