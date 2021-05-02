from dotenv import load_dotenv
load_dotenv()
import discord
import os
from discord.ext import commands

#client = discord.Client()
bot = commands.Bot(command_prefix="$")

course_information =""


@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')

"""
@bot.command()
async def embed(ctx):
    embed=discord.Embed(title="Thank you for using Dummy Bot!", url="https://realdrewdata.medium.com/", description="Dummy bot will enhance your Discord experience", color=discord.Color.purple())
    await ctx.send(embed=embed)
"""

@bot.event
async def on_guild_join(guild):
    for channel in guild.text_channels:
        if channel.permissions_for(guild.me).send_messages:
            retStr = str("""'''css\nThis is some colored Text'''""")
            embed=discord.Embed(title="""'''css\nThank you for using Dummy Bot!'''""", url="https://realdrewdata.medium.com/", description="Dummy bot will enhance your Discord experience", color=discord.Color.purple())
            embed.add_field(name="What is dummy bot?", value="This is the value for field 1. This is NOT an inline field.", inline=False)
            embed.add_field(name="To get started with dummy bot, please enter $setup", value="It is inline with Field 3", inline=True)
            embed.add_field(name="Field 3 Title", value="It is inline with Field 2", inline=True)
            await channel.send(embed=embed) #send the embed to the channel
            #Note: this channel.send should be placed immediately after all your embeds
        break


@bot.command()
async def setup(ctx):
    embed=discord.Embed(title="Welcome to Setup", description="Let's go over some setup properties. To change multiple items in setup, simply call $setup again.", color=discord.Color.purple())
    embed.add_field(name ="0: Upload Course Information ", value ="To upload course information, press 0. Once you have uploaded the course information, use $course_info to access it again.")
    embed.add_field(name ="1: Number of Instructors ", value ="To set the number of instructors in this server, press 1.")
    embed.add_field(name ="2: Skip Setup ", value ="To skip the setup process, press 2.")
    await ctx.send(embed=embed)

    # This will make sure that the response will only be registered if the following
    # conditions are met:
    def check(msg):
        #Assume user enters perfect input
        return msg.author == ctx.author and msg.channel == ctx.channel

        # failed while loop to check if user entered a correct input or not
        # not sure how to format this with discord
        """
        invalid_response = True
        while(invalid_response):
            if msg.content.lower() not in ["1", "2", "0"]:
                ctx.send("Please enter a valid number.")
            elif msg.author == ctx.author and msg.channel == ctx.channel and \
            msg.content.lower() in ["1", "2", "0"]:
                invalid_response = False
        return True
        """

    #wait for user input
    msg = await bot.wait_for("message", check=check)

    if msg.content == "0":
        embed1=discord.Embed(title="<a:pencil:838150754912436288> Please upload your course information here:", color=discord.Color.purple())
        await ctx.send(embed = embed1)
        msg2 = await bot.wait_for("message", check=check)
        course_information=msg2.content #this does not update the global variable for some reason

        #print to server
        await ctx.send(course_information)
        await ctx.send(msg2.content)


    elif msg.content == "1":
        embed2=discord.Embed(title="<a:woman_teacher:838129346089582662> Please enter the number of instructors in this channel:", color=discord.Color.purple())
        await ctx.send(embed=embed2)
        msg3 = await bot.wait_for("message", check=check)
        #set number of instructor roles to user input heres
        if(msg3.content =="3"): #this is for testing
            await ctx.send("Three instructors total.")


    elif msg.content == "2":
        embed3=discord.Embed(title="You skipped the setup process", color=discord.Color.purple())
        await ctx.send(embed =embed3)

@bot.command()
async def course_info(ctx):
    if(course_information == ""):
        await ctx.send("No course information was provided")
    else:
        await ctx.send("course_information or syllabus link")

#the following is broken code....heh
"""
@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    if message.content.startswith('$hello'):
        await message.channel.send('Boo')
"""

"""
@bot.event
async def on_member_join(member):
   await bot.get_channel(idchannel).send(f"{member.name} has joined")
@bot.event
async def on_member_remove(member):
   await bot.get_channel(837927155677659190).send(f"{member.name} has left")
"""

#need this to run the bot
bot.run(os.getenv('TOKEN'))
