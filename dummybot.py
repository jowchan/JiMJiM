from dotenv import load_dotenv
load_dotenv()
import discord
import os
from discord.ext import commands
import asyncio

from discord import Member, Role

TOKEN = os.getenv('TOKEN')
GUILD = os.getenv('GUILD')

intents = discord.Intents.default()
intents.members = True
client = commands.Bot(command_prefix='$', intents=intents)


client.course_information= ""


@client.event
async def on_ready():
    for guild in client.guilds:
        if guild.name == GUILD:
            break
    # guild = discord.utils.get(client.guilds, name=GUILD)

    print(
        f'{client.user} is connected to the following guild:\n'
        f'{guild.name}(id: {guild.id})'
    )

    members = '\n - '.join([member.name for member in guild.members])
    print(f'Guild Members:\n - {members}')

    await create_rank_roles()
   



@client.event
async def on_guild_join(guild):
    
    for channel in guild.text_channels:
        if channel.permissions_for(guild.me).send_messages:
            embed=discord.Embed(title="Thank you for using Dummy Bot!", url="https://realdrewdata.medium.com/", description="Dummy bot will enhance your Discord experience", color=discord.Color.purple())
            embed.add_field(name="What is dummy bot?", value="This is the value for field 1. This is NOT an inline field.", inline=False) 
            embed.add_field(name="To get started with dummy bot, please enter $setup", value="It is inline with Field 3", inline=True)
            embed.add_field(name="Field 3 Title", value="It is inline with Field 2", inline=True)
            await channel.send(embed=embed) #send the embed to the channel
            #Note: this channel.send should be placed immediately after all your embeds
        break


@client.command()
async def setup(ctx):
    
    embed=discord.Embed(title="Welcome to Setup", description="Let's go over some setup properties. To change multiple items in setup, simply call $setup again.", color=discord.Color.purple())
    embed.add_field(name ="0: Upload Course Information ", value ="To upload course information, press 0. Once you have uploaded the course information, use $course_info to access it again.", inline=False)
    embed.add_field(name ="1: Assign Instructor Role ", value ="Instructors have the ability to endorse student comments, giving extra points to that student. To assign an Instructor role to a member, type the command $instructor", inline = False)
    embed.add_field(name ="2: Skip Setup ", value ="To skip the setup process, press 2.", inline = False)
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
    msg = await client.wait_for("message", check=check)
    #global course_information
    if msg.content == "0":
        embed1=discord.Embed(title="<a:pencil:838150754912436288> Please enter the link to your course information here:", color=discord.Color.purple())
        await ctx.send(embed = embed1)
        client.course_information = await client.wait_for("message", check=check)
        

    """
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
"""
@client.command()
async def course_info(ctx):
    if client.course_information == "":
        await ctx.send("No course information has been provided.")
    else:  
        embed=discord.Embed(title="Course Information", url=client.course_information.content, color=discord.Color.purple())
        await ctx.send(embed=embed)

#the following is broken code....heh
"""  
@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if message.content.startswith('$hello'):
        await message.channel.send('Boo')
"""

# ------------ Bot Commands ------------------------------

# create a new Server Role

async def create_role(ctx, name):
    for guild in client.guilds:
        if guild.name == GUILD:
            break
    await guild.create_role(name=name, mentionable=True, hoist=True)
    msg = discord.Embed(
        title=f'Role: {name} has been created',
        color=0x67e0c4)
    await ctx.send(embed=msg)


# delete a Server Role

async def delete_role(ctx, name):
    for guild in client.guilds:
        if guild.name == GUILD:
            break
    role = discord.utils.get(guild.roles, name=name)
    await Role.delete(role)
    msg = discord.Embed(
        title=f'Role: {name} has been deleted',
        color=0x67e0c4)
    await ctx.send(embed=msg)


# add a Server Role for a user
@client.command()
async def add_Instructor(ctx, *usernames):
    user = ctx.author
    for guild in client.guilds:
        if guild.name == GUILD:
            break

    if user != guild.owner and user.roles != "Instructor":
        return
    

    for user in usernames:
        
        for member in guild.members:

            if member.name == user:
                break
        
        role_model = discord.utils.get(guild.roles, name= "Instructor")
        await member.add_roles(role_model)
        msg = discord.Embed(
            title=f'{user} has been assigned the role: Instructor',
            color=0x67e0c4)
        await ctx.send(embed=msg)


# delete a Server Role for a single or multiple users
@client.command()
async def delete_user_role(ctx,role, *usernames):
    user = ctx.author
    for guild in client.guilds:
        if guild.name == GUILD:
            break

    if user != guild.owner and user.roles != "Instructor":
        return

    for user in usernames:
        
        for member in guild.members:
            if member.name == user:
                break
        role_model = discord.utils.get(guild.roles, name=role)
        
        await member.remove_roles(role_model)
        msg = discord.Embed(
            title=f'{user} has been stripped of the role: {role}',
            color=0x67e0c4)
        await ctx.send(embed=msg)


# ------------ Helper functions ------------------------------

# Create roles (for emojis, include in the role string)
async def create_new_role(role, color):
    for guild in client.guilds:
        if guild.name == GUILD:
            break
    print(guild.roles)

    existing_roles = [r for r in guild.roles if r.name == role]

    if len(existing_roles) == 0:
        await guild.create_role(name=role, mentionable=True, hoist=True, color=color)
        print(f'New Role: {role} has been created.')
    else:
        print("Role name already exists, please create a different role!")




# Create Rank Roles (add to Guild)
async def create_rank_roles():
    await create_new_role("Instructor", 0xf5d442)
    await create_new_role("Newbie", 0xCC99C9)
    await create_new_role("Scholar", 0x9EC1CF)
    await create_new_role("Enlightened", 0x9EE09E)
    await create_new_role("Transcended ", 0xFEB144)
    await create_new_role("Literal Genius", 0xFF6663)
    print("Rank Roles have been added to the Server")
client.run(os.getenv('TOKEN'))
