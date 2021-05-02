from dotenv import load_dotenv
load_dotenv()
import discord
import os
from discord.ext import commands
import asyncio
import json

from discord import Member, Role

TOKEN = os.getenv('TOKEN')
GUILD = os.getenv('GUILD')

intents = discord.Intents.default()
intents.members = True
client = commands.Bot(command_prefix='$', intents=intents)
amounts = {}


# This is a GLOBAL variable for the syllabus command
client.course_information= ""


@client.event
async def on_ready():
    global amounts
    try:
        with open('amounts.json') as f:
            amounts = json.load(f)
    except FileNotFoundError:
        print("Could not load amounts.json")
        amounts = {}
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

    for guild in client.guilds:
        
        if guild.name == GUILD:
            break
    
    print(
        f"{client.user} is connected to the following guild: \n"
        f"{guild.name}(id: {guild.id})"
    )
    
    members = '\n - '.join([member.name for member in guild.members])
    print(f'Guild Members:\n - {members}')

@client.event
async def on_member_join(member):
    for guild in client.guilds:
        if guild.name == GUILD:
            break

    id = str(member.id)
    if id not in amounts:
        amounts[id] = 0
        role_model = discord.utils.get(guild.roles, name= "Newbie")
        await member.add_roles(role_model)
        await member.create_dm()
        await member.dm_channel.send("You are now registered")
        _save()
    else:
        await member.create_dm()
        await member.dm_channel.send("You already have an account")


@client.event
async def on_guild_join(guild):
    await create_rank_roles()

    for channel in guild.text_channels:
        if channel.permissions_for(guild.me).send_messages:
            embed=discord.Embed(title="Thank you for using Dummy Bot!", description="Dummy bot will enhance your Discord learning experience by promoting communication between users in a classroom setting.", color=discord.Color.purple())
            embed.add_field(name="What does Dummy Bot do?", value="Dummy Bot implements a reputation system by awarding points to users who contribute helpful information. \
                                    Users can earn points by asking questions, responding to questions, upvoting comments, or having an Instructor (role) upvote their comment. \
                                        After earning a certain level of points, users are automatically promoted to the next tier role. \
                                            Upon promotion, users gain a new color in their nickname and have access to a variety of new name badges to use.\
                                                There are five tier levels for students: Newbie, Scholar, Enlightened, Transcended, and Literal Genius.", inline=False) 
            embed.add_field(name="To get started with dummy bot, please enter $setup", value="Setup allows users to upload course information and set remindres for important deadlines and exam dates.", inline=False)
            embed.add_field(name="$info", value="For a list of all user-commands, please enter $info", inline=False)
            await channel.send(embed=embed) #send the embed to the channel
            #Note: this channel.send should be placed immediately after all your embeds
        break

@client.event
async def on_reaction_add(reaction, member):
    if reaction.message.author == member:
        return

    for guild in client.guilds:
        if guild.name == GUILD:
            break

    id = str(reaction.message.author.id)
    if reaction.emoji == '❌':
        amounts[id] -= 2 
        _save()
    elif reaction.emoji == '✅':
        amounts[id] += 2
        _save()
    elif reaction.emoji == '🟥':
        amounts[id] -= 5
        _save()
    elif reaction.emoji == '⭐':
        role_model = discord.utils.get(guild.roles, name= "Instructor")
        if role_model not in member.roles:
            return
        amounts[id] += 5
        _save()

    if amounts[id] == 0:
        role_model = discord.utils.get(guild.roles, name= "Newbie")
        await reaction.message.author.add_roles(role_model)
        await reaction.message.author.edit(nick=reaction.message.author.name + " | Newbie")
        
    elif amounts[id] > 0 and amounts[id] < 50:
        role_model = discord.utils.get(guild.roles, name= "Newbie")
        await reaction.message.author.remove_roles(role_model)

        role_model = discord.utils.get(guild.roles, name= "Scholar")
        await reaction.message.author.add_roles(role_model)
        await reaction.message.author.edit(nick=reaction.message.author.name + " | Scholar")
        
    elif amounts[id] > 50 and amounts[id] < 100:
        role_model = discord.utils.get(guild.roles, name= "Scholar")
        await reaction.message.author.remove_roles(role_model)

        role_model = discord.utils.get(guild.roles, name= "Enlightened")
        await reaction.message.author.add_roles(role_model)
        await reaction.message.author.edit(nick=reaction.message.author.name + " | Enlightened")
        
    elif amounts[id] > 100 and amounts[id] < 150:
        role_model = discord.utils.get(guild.roles, name= "Enlightened")
        await reaction.message.author.remove_roles(role_model)

        role_model = discord.utils.get(guild.roles, name= "Transcended")
        await reaction.message.author.add_roles(role_model)
        await reaction.message.author.edit(nick=reaction.message.author.name + " | Transcended")
        
    elif amounts[id] > 150 and amounts[id] < 200:
        role_model = discord.utils.get(guild.roles, name= "Transcended")
        await reaction.message.author.remove_roles(role_model)

        role_model = discord.utils.get(guild.roles, name= "Literal Genius")
        await reaction.message.author.add_roles(role_model)
        await reaction.message.author.edit(nick=reaction.message.author.name + " | Literal Genius")


@client.event
async def on_reaction_remove(reaction, member):
    if reaction.message.author == member:
        return

    for guild in client.guilds:
        if guild.name == GUILD:
            break

    id = str(reaction.message.author.id)
    if reaction.emoji == '❌':
        amounts[id] += 2 
        _save()
    elif reaction.emoji == '✅':
        amounts[id] -= 2
        _save()
    elif reaction.emoji == '🟥':
        amounts[id] += 5
        _save()
    elif reaction.emoji == '⭐':
        if member.roles != "Instructor":
            return
        amounts[id] -= 5
        _save()

    if amounts[id] == 0:
        role_model = discord.utils.get(guild.roles, name= "Scholar")
        await reaction.message.author.remove_roles(role_model)

        role_model = discord.utils.get(guild.roles, name= "Newbie")
        await reaction.message.author.add_roles(role_model)
        await reaction.message.author.edit(nick=reaction.message.author.name + " | Newbie")
        
    elif amounts[id] > 0 and amounts[id] < 50:
        role_model = discord.utils.get(guild.roles, name= "Enlightened")
        await reaction.message.author.remove_roles(role_model)

        role_model = discord.utils.get(guild.roles, name= "Scholar")
        await reaction.message.author.add_roles(role_model)
        await reaction.message.author.edit(nick=reaction.message.author.name + " | Scholar")
        
    elif amounts[id] > 50 and amounts[id] < 100:
        role_model = discord.utils.get(guild.roles, name= "Transcended")
        await reaction.message.author.remove_roles(role_model)

        role_model = discord.utils.get(guild.roles, name= "Enlightened")
        await reaction.message.author.add_roles(role_model)
        await reaction.message.author.edit(nick=reaction.message.author.name + " | Enlightened")
        
    elif amounts[id] > 100 and amounts[id] < 150:
        role_model = discord.utils.get(guild.roles, name= "Literal Genius")
        await reaction.message.author.remove_roles(role_model)

        role_model = discord.utils.get(guild.roles, name= "Transcended")
        await reaction.message.author.add_roles(role_model)
        await reaction.message.author.edit(nick=reaction.message.author.name + " | Transcended")
        
    elif amounts[id] > 150 and amounts[id] < 200:
        role_model = discord.utils.get(guild.roles, name= "Literal Genius")
        await reaction.message.author.add_roles(role_model)
        await reaction.message.author.edit(nick=reaction.message.author.name + " | Literal Genius")

@client.command()
async def points(ctx):
    if ctx.author == client.user:
        return

    id = str(ctx.author.id)
    if id in amounts:
        await ctx.send("You have {} reputation points".format(amounts[id]))
    else:
        await ctx.send("You do not have an account")

@client.command()
async def info(ctx):
    embed=discord.Embed(title=f"List of Commands", description="Below is a list of user accessible commands.", color=discord.Color.purple())
    embed.add_field(name ="$setup", value ="Setup allows users to upload course information and set remindres for important deadlines and exam dates.", inline=False)
    embed.add_field(name="$course_info", value="Provides the user with a url of the course information or syllabus.", inline=False)
    embed.add_field(name="$add_Instructor", value="Adds an instructor role to the server. Only the server owner or another Instructor can use this command. The syntax is: $add_Instructor [USERNAME]", inline=False)
    embed.add_field(name ="$delete_user_role", value="Removes the current role of the user. Only the server owner or another Instructor can use this command. The syntax is: $delete_user_role [ROLE] [USERNAME]", inline=False)
    await ctx.send(embed=embed)

@client.command()
async def setup(ctx):
    embed=discord.Embed(title="Welcome to Setup", description="Let's go over some setup properties. To change multiple items in setup, simply call $setup again.", color=discord.Color.purple())
    embed.add_field(name ="0: Upload Course Information ", value ="To upload course information, press 0. You will then be prompted to provide a url of the course page or syallbus. Once you have uploaded the course information, use $course_info to access it again.", inline=False)
    embed.add_field(name ="1: Set Course Reminders ", value ="To set reminders for important deadlines and exam dates, press", inline = False)
    embed.add_field(name ="2: Skip Setup ", value ="To skip the setup process, press 2.", inline = False)
    await ctx.send(embed=embed)
    
    # This will make sure that the response will only be registered if the following
    # conditions are met:
    def check(msg):
        #Assume user enters perfect input
        return msg.author == ctx.author and msg.channel == ctx.channel 

    #wait for user input
    msg = await client.wait_for("message", check=check)
    #global course_information
    if msg.content == "0":
        embed1=discord.Embed(title="<a:pencil:838150754912436288> Please enter the link to your course information here:", color=discord.Color.purple())
        await ctx.send(embed = embed1)
        client.course_information = await client.wait_for("message", check=check)
        

    
    elif msg.content == "1":
        # ---------------------CHANGE THIS----------------------------------------------------
        embed2=discord.Embed(title="<a:woman_teacher:838129346089582662> Please enter the number of instructors in this channel:", color=discord.Color.purple())
        await ctx.send(embed=embed2)
        msg3 = await client.wait_for("message", check=check)
        #set number of instructor roles to user input heres
        if(msg3.content =="3"): #this is for testing
            await ctx.send("Three instructors total.")
        
            
    elif msg.content == "2":
        embed3=discord.Embed(title="You skipped the setup process", color=discord.Color.purple())
        await ctx.send(embed =embed3)

@client.command()
async def course_info(ctx):
    if client.course_information == "":
        await ctx.send("No course information has been provided.")
    else:  
        embed=discord.Embed(title="Course Information", url=client.course_information.content, color=discord.Color.purple())
        await ctx.send(embed=embed)



#------------- Role Functions ------------------------

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
        await member.edit(nick=member.name + " | Instructor 🎓")
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
        await member.edit(nick=member.name)
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
    await create_new_role("Literal Genius", 0xFF6663)
    await create_new_role("Transcended", 0xFEB144)
    await create_new_role("Enlightened", 0x9EE09E)
    await create_new_role("Scholar", 0x9EC1CF)
    await create_new_role("Newbie", 0xCC99C9)
 
    print("Rank Roles have been added to the Server")

def _save():
    with open('amounts.json', 'w+') as f:
        json.dump(amounts, f)

@client.event
async def save():
    _save()
    
client.run(TOKEN)