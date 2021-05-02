from dotenv import load_dotenv
load_dotenv()
import discord
import os
from discord.ext import commands, tasks
import asyncio, datetime
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
client.startdate = None
client.enddate = None
client.lectures = None
client.lecture_starttime_dict = {}

@client.event
async def on_ready():

    global amounts
    try:
        with open('amounts.json') as f:
            amounts = json.load(f)
    except FileNotFoundError:
        print("Could not load amounts.json")
        amounts = {}

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
async def on_guild_join(guild):
    await create_rank_roles()

    for channel in guild.text_channels:
        if channel.permissions_for(guild.me).send_messages:
            embed=discord.Embed(title="Thank you for using JiMJiM Bot!", description="JiMJiM bot will enhance your Discord learning experience by promoting communication between users in a classroom setting.", color=0xffc0cb )
            embed.add_field(name="What does JiMJiM Bot do?", value="JiMJiM Bot implements a reputation system by awarding points to users who contribute helpful information. \
                                    Users can earn points by asking questions, responding to questions, having upvoted comments, or having an Instructor (rank) endorse their comment. \
                                        After earning a certain level of points, users are automatically promoted to the next rank. \
                                            Upon promotion, users gain a new color in their nickname and have access to a variety of new name badges to use.\
                                                There are five ranks for students: Newbie, Scholar, Enlightened, Transcended, and Literal Genius.", inline=False) 
            embed.add_field(name="To get started with JiMJiM Bot, please enter $setup", value="Setup allows users to upload course information and set remindres for important deadlines and exam dates.", inline=False)
            embed.add_field(name="$info", value="For a list of all user-commands and more information of the JimJim Bot please enter $info", inline=False)
            await channel.send(embed=embed) #send the embed to the channel
            #Note: this channel.send should be placed immediately after all your embeds
        break

@client.command()
async def info(ctx):
    embed=discord.Embed(title=f"📋 List of Commands 📋", description="Below is a list of user accessible commands.", color=0xffc0cb )
    embed.add_field(name ="$setup", value ="Setup allows users to upload course information and set remindres for important deadlines and exam dates.", inline=False)
    embed.add_field(name="$course_info", value="Provides the user with a url of the course information or syllabus.", inline=False)
    embed.add_field(name="$add_Instructor", value="Adds an instructor role to the server. Only the server owner or another Instructor can use this command. The syntax is: $add_Instructor [USERNAME]", inline=False)
    embed.add_field(name ="$delete_user_role", value="Removes the current role of the user. Only the server owner or another Instructor can use this command. The syntax is: $delete_user_role [ROLE] [USERNAME]", inline=False)
    embed.add_field(name ="$course_dates", value ="Retrieves the course start and end dates.", inline=False)
    embed.add_field(name="$course_schedule", value="Retrieves the course schedule, lecture times, and exam dates.", inline = False)
    embed.add_field(name ="$shop", value ="Access the shop of emojis available to users who reach a certain rank.", inline=False)
    embed.add_field(name = "Earning Points", value ="Users can earn points by asking questions, responding to questions, upvoting comments, or having an Instructor (role) upvote their comment. \
                                There are four available reactions: \n Upvote <a:white_check_mark:838480444239380610> (+2 points) \n \
                                   Downvote <a:x:838480444239380610> (-2 points)\n  Spam :triangular_flag_on_post: (-5 points) \n Instructor Endorsed <a:star:838480444239380610> (+5 points)", inline= False)
    embed.add_field(name = "Ranks", value ="Students begin with Rank Newbie and progress up to Literal Genius. The ranks are as follows: \
                                Newbie 👶 \n Scholar 📚 \n Enlightened 💡 \n Transcended 💰 \n Literal Genius 🧙‍♂️ \n \
                                   The Instructor 🎓 rank is assigned by the server owner and other Instructors themselves.", inline= False)
    await ctx.send(embed=embed)

@client.command()
async def setup(ctx):
    embed=discord.Embed(title=f"🛠️ Welcome to Setup 🛠️", description="Let's go over some setup properties. To change multiple items in setup, simply call $setup again.", color=0xffc0cb )
    embed.add_field(name ="0: Upload Course Information 📝", value ="To upload course information, press 0. You will then be prompted to provide a url of the course page or syallbus. Once you have uploaded the course information, use $course_info to access it again.", inline=False)
    embed.add_field(name ="1: Set Course Reminders ⏰", value ="To set reminders for important deadlines and exam dates, press", inline = False)
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
         embed1 = discord.Embed(
            title="<a:pencil:838150754912436288> Please enter the link to your course information here:",
            color=0xffc0cb)
         await ctx.send(embed=embed1)
         client.course_information = await client.wait_for("message", check=check)
         embed2 = discord.Embed(title ="Course information has been saved. Enter $course_info command to access the link.",color=0xffc0cb )
         await ctx.send(embed=embed2)

    
    elif msg.content == "1":
        embed3 = discord.Embed(
            title="<a:woman_teacher:838129346089582662> Please enter course START DATE (format: mm/dd/yyyy)",
            color=0xffc0cb)
        await ctx.send(embed=embed3)
        msg_start = await client.wait_for("message", check=check)
        client.startdate = msg_start.content
        print("start date: ", client.startdate)

        embed3 = discord.Embed(
            title="<a:woman_teacher:838129346089582662> Please enter course END DATE (format: mm/dd/yyyy)",
            color=0xffc0cb)
        await ctx.send(embed=embed3)
        msg_end = await client.wait_for("message", check=check)
        client.enddate = msg_end.content
        print("end date: ", client.enddate)

        embed3 = discord.Embed(
            title="<a:woman_teacher:838129346089582662> Please enter LECTURE TIMES based on the following criteria---------:",
            color=0xffc0cb)
        embed3.add_field(
            name="DayOfWeek StartTime - EndTime",
            value="M/T/W/Th/F/Sat/Sun HH:MM - HH:MM",
            inline=False)
        embed3.add_field(
            name="Example:",
            value="M 10:30-11:00, Sun 00:30-18:00",
            inline=False)
        await ctx.send(embed=embed3)
        msg_lectures = await client.wait_for("message", check=check)
        client.lectures = msg_lectures.content
        print("lectures: ", client.lectures)

        embed3 = discord.Embed(
            title="<a:woman_teacher:838129346089582662> Lecture reminders will be sent prior to every lecture. ",
            color=0xffc0cb)
        await ctx.send(embed=embed3)
        # parse through user inputted lecture times and start the background task
        await format_lecture_times(ctx)
        
            
    elif msg.content == "2":
        embed3=discord.Embed(title="You skipped the setup process", color=0xffc0cb )
        await ctx.send(embed =embed3)

@client.command()
async def course_info(ctx):
    if client.course_information == "":
        embed = discord.Embed(title ="No course information has been provided.",color=0xffc0cb )
        
    else:  
        embed=discord.Embed(title="Course Information", url=client.course_information.content, color=0xffc0cb )
    await ctx.send(embed=embed)

@client.command()
async def course_dates(ctx):
    if client.startdate == "" or client.enddate == "":
        await ctx.send("No course dates have been provided.")
    else:
        embed = discord.Embed(
            title="Course Dates",
            description=f"Start Date: {client.startdate} ~ End Date: {client.enddate}",
            color=0xffc0cb)
        await ctx.send(embed=embed)

@client.command()
async def course_schedule(ctx):
    if client.lectures == "":
        await ctx.send("No course lecture times has been provided.")
    else:
        lecture_array = client.lectures.split(',')
        embed = discord.Embed(
            title="Course Lecture Times",
            description="",
            color=0xffc0cb)

        for lecture_time in lecture_array:
            embed.add_field(
                name=f'{lecture_time}',
                value="---",
                inline=False)

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
        color=0xffc0cb)
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
        color=0xffc0cb)
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
            color=0xffc0cb)
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
            color=0xffc0cb)
        await ctx.send(embed=msg)

# on member join, assign Newbie role
@client.event
async def on_member_join(member):
    id = str(member.id)
    if id not in amounts:
        amounts[id] = 0
        await member.create_dm()
        await member.dm_channel.send("You are now registered")
        _save()
    else:
        await member.create_dm()
        await member.dm_channel.send("You already have an account")

    for guild in client.guilds:
        if guild.name == GUILD:
            break
    role = discord.utils.get(guild.roles, name="Newbie")
    await member.add_roles(role)
    msg = discord.Embed(
        title=f'Welcome {member.name} to server {guild}! \
        You have been assigned the role: Newbie. To level up in rank, participate constructively in course Q&A to \
        earn points.', color=0xffc0cb)

    # Bot sends DM to member
    await member.send(embed=msg)

@client.command()
async def register(ctx):
    id = str(ctx.message.author.id)
    if id not in amounts:
        amounts[id] = 100
        await ctx.send("You are now registered")
        _save()
    else:
        await ctx.send("You already have an account")

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
        print("upvote")
        amounts[id] -= 2
        _save()
    elif reaction.emoji == '🚩':
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
        msg = discord.Embed(title="Reputation Points", color=0xffc0cb)
        msg.add_field(name="Points:", value="You have {} reputation points".format(amounts[id]), inline=False)

        # Bot sends DM to member
        await ctx.author.send(embed=msg)
    else:
        await ctx.author.create_dm()
        await ctx.author.dm_channel.send("You do not have an account")


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

# ------------------Course Notifications------------------
# set up lecture notifications
async def format_lecture_times(ctx):
    print("lecture times: ", client.lectures)
    days_of_week = {
        "M": 0,
        "T": 1,
        "W": 2,
        "Th": 3,
        "F": 4,
        "Sat": 5,
        "Sun": 6,
    }
    lecture_array = client.lectures.split(',')
    for lecture in lecture_array:
        split = lecture.strip().split(' ')
        day = split[0]
        starttime = split[1].split('-')[0]
        client.lecture_starttime_dict[days_of_week[day]] = starttime
    print(lecture_array)
    print(client.lecture_starttime_dict)

    # start infinite background notification task loop
    lectureNotifications.start(ctx)


@tasks.loop()
async def lectureNotifications(ctx):

    current_day = datetime.date.today().weekday()
    current_hour = datetime.datetime.now().hour
    current_minute = datetime.datetime.now().minute

    if current_day in client.lecture_starttime_dict:
        starthour = client.lecture_starttime_dict[current_day].split(":")[0]
        startmins = client.lecture_starttime_dict[current_day].split(":")[1]
        starting_datetime = datetime.datetime(2020, 1, 1, int(starthour), int(startmins), 0)
        print("lecture start datetime: ", starting_datetime)

        ten_minutes = datetime.timedelta(minutes=10)

        # ten minutes earlier than starting_datetime (disregard the date, we just want the time)
        final_datetime = starting_datetime - ten_minutes
        print("notification datetime: ", final_datetime)
        notification_hour = final_datetime.hour
        notification_minute = final_datetime.minute

        # print('notification hour', notification_hour)
        # print('notification minute', notification_minute)
        print(f'current time: {current_hour}:{current_minute}')

        # if current time is between notification time & start of lecture
        if current_hour == notification_hour \
                and (notification_minute <= current_minute) \
                and (abs(notification_minute - current_minute) <= 10):
            reminder = discord.Embed(
                title=f'<a:woman_teacher:838129346089582662> Lecture TODAY @ {client.lecture_starttime_dict[current_day]}',
                color=0xffc0cb)
            await ctx.send(embed=reminder)

        await asyncio.sleep(60*3)

def _save():
    with open('amounts.json', 'w+') as f:
        json.dump(amounts, f)

@client.event
async def save():
    _save()

@client.command()
async def shop(ctx):
    embed= discord.Embed(
        title="Shop",
        value="Decorate your name with emojis! Only emoji associated to your rank can be added.",
        color= 0xffc0cb)
    embed.add_field(
        name="Scholar Emoji :books:",
        value="Choose from the following list of emojis: :deer: :ox: :pretzel: :taco: :golf:", 
        inline = False)
    embed.add_field(
        name="Enlightened Emoji :bulb:",
        value="Choose from the following list of emojis: :monkey_face: :zebra: :chestnut: :salad: :fishing_pole_and_fish:",
        inline = False)
    embed.add_field(
        name="Transcended Emoji :moneybag:",
        value="Choose from the following list of emojis: :whale2: :sauropod: :sushi: :coconut: :chess_pawn:", 
        inline = False)
    embed.add_field(
        name="Literal Genius Emoji :man_mage:", 
        value="Choose from the following list of emojis: :unicorn: :dragon_face: :bento: :hot_pepper: :8ball:", 
        inline = False)
    await ctx.send(embed=embed)

client.run(TOKEN)
