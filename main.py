import os
import discord
import asyncio

from discord import Member, Role
from dotenv import load_dotenv
from discord.ext.commands import Bot

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('GUILD')

intents = discord.Intents.default()
intents.members = True
client = Bot(command_prefix='$', intents=intents)


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
    await assign_owner()
    # await create_new_role("User", 0xc775c9)
    # await updateRank(guild.owner.id)

# ------------ Bot Commands ------------------------------

# create a new Server Role
@client.command()
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
@client.command()
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
async def add_user_role(ctx, username, role):
    for guild in client.guilds:
        if guild.name == GUILD:
            break

    for member in guild.members:
        if member.name == username:
            break

    role_model = discord.utils.get(guild.roles, name=role)
    await member.add_roles(role_model)

    msg = discord.Embed(
        title=f'{username} has been assigned the role: {role}',
        color=0x67e0c4)

    await ctx.send(embed=msg)


# delete a Server Role from a user
@client.command()
async def delete_user_role(ctx, username, role):
    for guild in client.guilds:
        if guild.name == GUILD:
            break

    for member in guild.members:
        if member.name == username:
            break

    role_model = discord.utils.get(guild.roles, name=role)
    await member.remove_roles(role_model)
    await ctx.send(f'{username} has been stripped of Role: {role}')


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


# Assign Guild owner the "Instructor" Role
async def assign_owner():
    channel = client.get_channel(837965366767779854)
    for guild in client.guilds:
        if guild.name == GUILD:
            break

    # create Instructor role
    await guild.create_role(name="Instructor🏫", mentionable=True, color=0xf5d442)

    # assign guild owner instructor role
    owner = guild.get_member(guild.owner.id)
    instructor_role = discord.utils.get(guild.roles, name="Instructor🏫")
    await Member.add_roles(owner, instructor_role)
    msg = discord.Embed(
        title=f'{guild.owner} has been assigned the Instructor🏫 role.',
        color=0x67e0c4)
    await channel.send(embed=msg)


# Create Rank Roles (add to Guild)
async def create_rank_roles():
    await create_new_role("Newbie 👶", 0xCC99C9)
    await create_new_role("Community 📚", 0x9EC1CF)
    await create_new_role("Active 💡", 0x9EE09E)
    await create_new_role("Experienced 💰", 0xFEB144)
    await create_new_role("Literal Genius 🧙", 0xFF6663)
    print("Rank Roles have been added to the Server")

# Update the rank of member (not fully implemented)
# async def updateRank(member_id):
#     for guild in client.guilds:
#         if guild.name == GUILD:
#             break
#
#     member = guild.get_member(member_id)
#     print("before update: ", member.roles)
#     current_rankrole = [r for r in member.roles if r.name != '@everyone'][0]
#     role_to_remove = discord.utils.get(guild.roles, name=current_rankrole)
#     await Member.remove_roles(guild.id, member.id, role_to_remove)
#     print("after update: ", member.roles)

client.run(TOKEN)

# async def assign_instructor():
#     for guild in client.guilds:
#         if guild.name == GUILD:
#             break
#     print(guild.roles)
#
#     channel = client.get_channel(837965366767779854)
#     await channel.send(guild.owner)
#     embed_welcome = discord.Embed(
#         title="Assigning Instructor Role",
#         description="Please type in the username of the user that you would like to assign the Instructor role to.",
#         color=0x67e0c4)
#     await channel.send(embed=embed_welcome)
#
#     def check(m):
#         return m.channel == channel
#
#     try:
#         msg = await client.wait_for("message", check=check, timeout=60.0)
#     except asyncio.TimeoutError:
#         await channel.send("sorry, timed out!")
#     else:
#         # add instructor role to the member specified by user input
#         member = guild.get_member(652683959695704064)
#         print(member)
#         instructor_role = discord.utils.get(guild.roles, name="Instructor")
#         await Member.add_roles(member, instructor_role)
#         msg = discord.Embed(
#             title=f'{msg.content} has been assigned the Instructor role.',
#             color=0x67e0c4)
#         await channel.send(embed=msg)
# @client.event
# async def on_message(message):
#     # client.user => EduBot
#
#     if message.author == client.user:
#         return
#
#     if message.content.startswith('!'):
#         await message.channel.send("Command")

