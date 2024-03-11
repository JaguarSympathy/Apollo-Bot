import discord
from discord import app_commands
from discord.ext import tasks
import datetime
import json
import requests
from dateutil.parser import parse
import random
import string

TOKEN = "MTE0NjU3MzMzMTI5MDY3MzIyMg.Gygi9K.x30DzogeiihJ_7VQpuLtGltTagjpAPzwugN90c"

# initialising clients
client = discord.Client(intents=discord.Intents.all())
tree = discord.app_commands.CommandTree(client)

# functions
def getProfile(user):
    return dict(requests.get(f"https://users.roblox.com/v1/users/{user}").json())

def getUserID(username):
    response = requests.post("https://users.roblox.com/v1/usernames/users",json={"usernames":[username]})
    assert response.status_code == 200

    return response.json()["data"][0]["id"]

async def log(msg):
    logs = await client.fetch_channel(1146565921037627453)
    await logs.send(msg)

def generateVerificationKey():
    letters = string.ascii_lowercase
    return "".join(random.choice(letters) for i in range(20))


# events

@tasks.loop(time=datetime.time(hour=0,minute=0,second=1))
async def qotd():
    embed = discord.Embed(colour=discord.Colour.green(),title="Quote of the Day")
    channel = await client.fetch_channel(1174832919789977675)
    quote = requests.get("https://zenquotes.io/api/random")
    quote = json.loads(quote.text)
    quote = quote[0]['q'] + " - " + quote[0]['a']
    embed.add_field(name="",value=quote)
    await channel.send(embed=embed)

@client.event
async def on_ready():
    print("Apollo Online")
    await client.change_presence(status=discord.Status.online,activity=discord.CustomActivity(name="Bot @ Apollo Systems"))
    await tree.sync()
    await qotd.start()


@tree.command(name="estimate",description="For Staff use")
async def estimate(cmd: discord.Interaction):
    if "Staff" in str(cmd.user.roles):
        embed = discord.Embed()
        embed.set_author(name="Staff Team @ Apollo")
        embed.add_field(name="",value="The estimate provided above is a reflection of average price ranges. All prices are subject to negotiation and Apollo Systems' own discretion. Estimates should not be taken as final prices.")
        embed.set_footer(text="Apollo Systems",icon_url="https://images-ext-1.discordapp.net/external/Np5C1pTnH-TzpjkymlStLb11uB_JqKsCgX56Tqn8ykc/https/tr.rbxcdn.com/0d0c68b68e1073c8c91b9cf29e98af4b/150/150/Image/Png")
        await cmd.channel.send(embed=embed)
        await cmd.response.send_message(content="Sent embed",ephemeral=True)

@tree.command(name="check-profile",description="Check a user's profile on roblox")
@app_commands.describe(user="User to check profile for")
async def checkprofile(interaction: discord.Interaction,user: int):
    profile = getProfile(user)
    joindate = parse(profile["created"][0:10]).strftime("%d/%m/%Y")


    embed = discord.Embed(title="Profile Check",description=f"Profile Check on {user}")
    embed.add_field(name="Username",value=profile["name"]).add_field(name="Roblox ID",value=profile["id"]).add_field(name="Join Date",value=joindate).add_field(name="Ban Status",value=profile["isBanned"]).add_field(name="Profile Description",value=profile["description"])
    await interaction.response.send_message(embed=embed)

@tree.command(name="verify",description="Verify your roblox account")
@app_commands.describe(username="Roblox account to connect")
async def verify(interaction: discord.Interaction,username: str):
    userid = str(getUserID(username))
    profile = getProfile(userid)
    
    with open("userData.json","r") as f:
        userData = json.load(f)

    try:
        if userData[userid]["verificationString"] in profile["description"]:
            userData[userid]["verified"] = True
            del userData[userid]["verificationString"]
            print(f"Verified {username} as {userid}.")

            try:
                await interaction.user.edit(nick=username)
            except:
                print(f"Unable to change nickname for {username}")

            embed = discord.Embed(title="Verification",description=f"You have successfully verified as {username}.")
            await interaction.response.send_message(embed=embed)
        else:
            userData[userid] = {"verificationString":"","verified":False}
            userData[userid]["verificationString"] = generateVerificationKey()

            embed = discord.Embed(title="Verification",description=f"Please enter the following verification key into your [roblox profile description](https://www.roblox.com/users/{userid}/profile).\nOnce complete, run this command again.")
            embed.add_field(name="Username",value=username).add_field(name="User ID",value=userid).add_field(name="Verification Key",value=userData[userid]["verificationString"])
            await interaction.response.send_message(embed=embed)
    except KeyError:
        userData[userid] = {"verificationString":"","verified":False}
        userData[userid]["verificationString"] = generateVerificationKey()

        embed = discord.Embed(title="Verification",description=f"Please enter the following verification key into your [roblox profile description](https://www.roblox.com/users/{userid}/profile).\nOnce complete, run this command again.")
        embed.add_field(name="Username",value=username).add_field(name="User ID",value=userid).add_field(name="Verification Key",value=userData[userid]["verificationString"])
        await interaction.response.send_message(embed=embed)
    
    with open("userData.json","w") as f:
        json.dump(userData,f)


client.run(TOKEN)
