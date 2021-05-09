import discord
import random
import time
import os
import socket
from sys import exit
from importlib import import_module
print(f'Discord.py\'s Version: {discord.__version__}')  # check to make sure at least once you're on the right version!
token = 'NjA2NzY5MDQ5NDUxNjI2NDk3.XiUIqw.FCs0vWaFlnjq5R2D5TA7Qj2-V90'  # token to run # token = 'NjA2NzY2MzY2Nzc0NTI1OTUy.XpFX5Q.SdwGovEsJtWn7TCiy28OlZaAEsU'  # 2nd bot token
client = discord.Client()  # starts the discord client.
neko_help = {'version()': " Shows bot's version.",
             'invite()': '  Shows invite link.',
             'help()': "    OR help(command):\ncommand is a function() -> Show command's usage.\nPs: (if command isn't provided -> Show list of commands)\nEx: help(), help(clear())",
             'clear()': "   OR clear(n):\nn is a number (Amount) -> Clear your last n message(s).\nPs: (if n isn't provided -> n = 1)",
             'dm()': "      OR dm(ID):\nID is a number (User ID) -> Send a notice to the user with the ID.\nPs: (if ID isn't provided -> ID = your user ID)",
             'roll()': "    OR roll(n)\nn is a number (Max) -> Roll a number from 1 to n.\nPs: (if n isn't provided -> n = 2)",
             'emote()': '   Random emote.',
             'member()': '  Member count.',
             'flip()': '    Flip a coin.',
             'perm()': "    OR perm(ID):\nID is a number (User ID) -> Give/Remove someone permission to use admin commands\nPs: (if ID isn't provided -> Show list of admins)",
             'admin()': "   OR admin(command):\ncommand is a function() -> Show command's usage.\nPs: (if command isn't provided -> Show list of commands)/(works like 'help()')\nEx: admin(), admin(manage())",
             'quit()': "    OR quit(ID): (you can use quit() but not quit(ID))\nID is a number(Guild ID) -> Leaves the server with the ID.\nPs: (if ID isn't provided -> ID = this server's ID)",
             'refresh()': " OR refresh(n):\nn is a number (Amount) -> Delete bot's last n message(s).\nPs: (if n isn't provided -> n = 1)/(works like 'clear()')",
             'del()': "     OR get(ID):\nID is a number (Message ID) -> Delete the message with the ID.",
             'get()': "     OR get(ID):\nID is a number (Message ID) -> Get additional info about the message with the ID.",
             'manage()': '''  OR manage(type):\ntype is a manage type -> There are 6 manage types:\noff, guild, member, message, role, emoji\nmanage(off):     Turn off all public commands.\nmanage(guild):   Send notification for channels/guild updates.
manage(role):    Send notification for role deletes/adds/permissions.\nmanage(emoji):   Send notification for emoji updates.\nmanage(member):  Send notification for members statuses/activities and role adds/removal.
manage(message): Send notification for messages deletes/edits and reaction adds/removal in messages.\n(if type isn't provided -> Show list of manage types currently on and channel used for manage() if exist)\nNote: (Redo these command to turn off)'''}
ver = "1.0.0"
owner = 320085340671180801
t = 320085340671180801
c = 670447665435246609
log, welcome, notify = True, True, True
into, space = '-' * 10, '_' * 50
file = "dis_log.txt"
storage = "dis_var.py"
ending = ('...', '?', '!')
emote = (':stuck_out_tongue:', ':drum:', ':100:', ':fork_and_knife:', ':weary:', ':ok_hand:', ':eggplant:',
         ':tired_face:', ':space_invader:',
         ':ghost:', ':bone:', ':skull:', ':chicken:', ':boom:', ':carrot:', ':cut_of_meat:', ':brain:', ':rabbit:',
         ':ring:', ':doughnut:')


def end(endings=ending):
    return random.choice(endings)


def emo(emotes=emote):
    return random.choice(emotes)


def clock():
    return time.ctime(time.time())


def write(msg, name=file, mode='a+'):
    if log:
        try:
            with open(name, mode, encoding="utf-8") as f:
                f.write(msg)
        except PermissionError:
            pass


def save(store=f'{os.getcwd()}/{storage}'):
    try:
        write(f'manage = {manage}\n', name=store, mode='w+')
    except FileNotFoundError:
        write(f'manage = {manage}\n', name="dis_var.py", mode='w+')
    print(f'manage: {manage}\n{space}')


def add(message):
    add_on = ""
    if len(message.embeds) == 0 and len(message.attachments) == 0:
        pass
    else:
        embeds, attachments = [], []
        for embed in message.embeds:
            embeds.append(embed.url)
        for attach in message.attachments:
            attachments.append(attach.url)
        if len(embeds) != 0:
            add_on += "\n`Embeds:`"
            for link in embeds:
                add_on += "\n"
                add_on += f'```{link}```'
        elif len(attachments) != 0:
            add_on += "\n`Attachments:`"
            for link in attachments:
                add_on += "\n"
                add_on += f'```{link}```'
    return add_on


def on_off(message):
    try:
        if manage[message.guild.id].get('off', False):
            return "off"
        else:
            return "on"
    except AttributeError:
        return "on"


async def resp(guild, msg=f'{end()}'):  # resp is for cases where the default system channel is forbidden or doesn't exist. It re-route the msgs to the origin channel instead.
    try:
        await guild.system_channel.send(msg)
    except discord.errors.Forbidden:
        if client.get_channel(manage[guild.id].get('sys')) is None:
            cid = await guild.create_text_channel('hibiki-channel')
            manage[guild.id]['sys'] = cid.id
            await client.get_channel(manage[guild.id]['sys']).send(f'```Channel created for manage(){end()}```')
            save()
        await client.get_channel(manage[guild.id]['sys']).send(msg)
    except AttributeError:
        if client.get_channel(manage[guild.id].get('sys')) is None:
            cid = await guild.create_text_channel('hibiki-channel')
            manage[guild.id]['sys'] = cid.id
            await client.get_channel(manage[guild.id]['sys']).send(f'```Channel created for manage(){end()}```')
            save()
        await client.get_channel(manage[guild.id]['sys']).send(msg)


async def manage_change(message, mg_type, enable, disable):
    if manage[message.guild.id].get(mg_type, False):
        try:
            del manage[message.guild.id][mg_type]
            await message.channel.send(disable)
        except discord.errors.Forbidden:
            await resp(message.guild, msg=disable)
    else:
        try:
            update = {mg_type: True}
            manage[message.guild.id].update(update)
            await message.channel.send(enable)
        except discord.errors.Forbidden:
            await resp(message.guild, msg=enable)


async def check_resp(message, msg, else_msg):  # check checks for "```" to prevent a discord chat bug with ``` ``` and return else msg if found.
    if f"```" in message.content:
        msg = else_msg
    await resp(message.guild, msg=msg)


async def check_message(message, msg, else_msg):
    if f"```" in message.content:
        await message.channel.send(f"{else_msg}")
    else:
        await message.channel.send(f"{msg}")


async def check_obj(obj, guild, msg, else_msg):
    if f"```" in obj:
        msg = else_msg
    await resp(guild, msg=msg)


async def check_resp_beaf(before, after, msg, else_msg):  # beaf (before-after) is for cases where the '''msg''' is bugged out cause there was another ''' inside the msg.
    if f"```" in before.content or f"```" in after.content:
        msg = else_msg
    await resp(before.guild, msg=msg)


async def check_msg_beaf(before, after, msg, else_msg):
    if f"```" in before.content or f"```" in after.content:
        await before.channel.send(f"{else_msg}")
    else:
        await before.channel.send(f"{msg}")


async def check_obj_beaf(before, after, guild, msg, else_msg):
    if f"```" in before or f"```" in after:
        msg = else_msg
    await resp(guild, msg=msg)


@client.event
async def on_ready():  # method expected by client. This runs once when connected
    print(f'{clock()}\nWe have logged in as {client.user}\n' + space)  # notification of login.
    await client.change_presence(activity=discord.Game(name=f"help() for commands{end()}"))
    guild_id = []
    for clan in client.guilds:
        print(clan, clan.id, str(clan.member_count) + ' members')
        guild_id.append(clan.id)
    print(f"{len(guild_id)} guilds.")
    deletes = []
    [deletes.append(server) for server in manage.keys() if server not in guild_id]
    for delete in deletes:
        del manage[delete]
    for server in guild_id:
        if server not in manage.keys():
            update = {server: {}}
            manage.update(update)
    save()
    write(f'{clock()}\nWe have logged in as {client.user}\n{client.guilds}\n{space}\n')
    if notify:
        await client.get_user(owner).send(f">>> ```yaml\n{client.user} Online{end()}"
                                          f"\nCWD:     {os.getcwd()}"
                                          f"\nHost:    {socket.gethostname()}"
                                          f"\nIP:      {socket.gethostbyname(socket.gethostname())}```")


@client.event
async def on_guild_join(guild):
    print(f'{clock()}\nJoined server: {guild}/{guild.id}\nGuilds: {client.guilds}\n' + space)
    write(f'{clock()}\nJoined server: {guild}/{guild.id}\nGuilds: {client.guilds}\n{space}\n')
    update = {guild.id: {}}
    manage.update(update)
    save()
    try:
        await guild.system_channel.send(f"```Hello, type help() for commands{end()}```")
    except discord.errors.Forbidden:
        try:
            if f"```" in guild.name:
                await guild.owner.send(f"`Joined`: {guild.name}```Type help() for commands{end()}```")
            else:
                await guild.owner.send(f"```Joined: {guild.name}\nType help() for commands{end()}```")
        except discord.errors.Forbidden:
            pass
    except AttributeError:
        try:
            if f"```" in guild.name:
                await guild.owner.send(f"`Joined`: {guild.name}```Type help() for commands{end()}```")
            else:
                await guild.owner.send(f"```Joined: {guild.name}\nType help() for commands{end()}```")
        except discord.errors.Forbidden:
            pass


@client.event
async def on_guild_remove(guild):
    print(f'{clock()}\nLeft server: {guild}/{guild.id}\nGuilds: {client.guilds}\n' + space)
    write(f'{clock()}\nLeft server: {guild}/{guild.id}\nGuilds: {client.guilds}\n{space}\n')
    del manage[guild.id]
    save()


@client.event
async def on_member_join(member):
    print(f'{clock()}\n{member} joined {member.guild.name}/{member.guild.id}\n' + space)
    write(f'{clock()}\n{member} joined {member.guild.name}/{member.guild.id}\n{space}\n')
    try:
        await client.get_user(member.id).send(f'Welcome <@!{member.id}> to {member.guild}{end()}')
        if manage[member.guild.id].get('member', False) and welcome:
            await resp(member.guild,
                       msg=f'```New member{end()}:```<@!{member.id}> `has joined {member.guild}`')
    except discord.errors.Forbidden:
        pass


@client.event
async def on_member_remove(member):
    if member.id == client.user.id:
        pass
    else:
        print(f'{clock()}\n{member} left {member.guild.name}/{member.guild.id}\n' + space)
        write(f'{clock()}\n{member} left {member.guild.name}/{member.guild.id}\n{space}\n')
        try:
            if manage[member.guild.id].get('member', False):
                await resp(member.guild,
                           msg=f'```Member left{end()}:```<@!{member.id}> `has left {member.guild}`')
        except discord.errors.Forbidden:
            pass


@client.event
async def on_member_update(before, after):
    if manage[before.guild.id].get('member', False):
        try:
            if before.status != after.status:
                await resp(before.guild, msg=f"```{before}\nstatus: {after.status}```")
            elif before.activities != after.activities:
                be_acts, af_acts = [], []
                for act in before.activities:
                    if act.name != 'Custom Status':
                        be_acts.append(act.name)
                for act in after.activities:
                    if act.name != 'Custom Status':
                        af_acts.append(act.name)
                beaf_dif = str(set(be_acts).symmetric_difference(af_acts))[2:-2]
                if len(af_acts) > len(be_acts):
                    await resp(before.guild,
                               msg=f"```{before}\nNew activity: {beaf_dif}```")
                elif beaf_dif != "t":  # discord returns "t" for custom statuses
                    await resp(before.guild,
                               msg=f"```{before}\nStopped activity: {beaf_dif}```")
            elif before.nick != after.nick:
                if after.nick is None:
                    await check_obj(before.nick, before.guild, msg=f"```{before}\nRemoved nickname: {before.nick}```",
                                    else_msg=f"```{before}````Removed nickname`: {before.nick}")
                else:
                    await check_obj(after.nick, before.guild, msg=f"```{before}\nNew nickname: {after.nick}```",
                                    else_msg=f"```{before}````New nickname`: {after.nick}")
            elif before.roles != after.roles:
                be_roles, af_roles = [], []
                for role in before.roles:
                    if role.name != '@everyone':
                        be_roles.append(role.name)
                for role in after.roles:
                    if role.name != '@everyone':
                        af_roles.append(role.name)
                role = str(set(be_roles).symmetric_difference(af_roles))[2:-2]
                if len(af_roles) > len(be_roles):
                    await check_obj(role, before.guild, msg=f"```{before}\nNew role: {role}```",
                                    else_msg=f"```{before}`````New role:`` {role}")
                else:
                    await check_obj(role, before.guild, msg=f"```{before}\nRemoved role: {role}```",
                                    else_msg=f"```{before}`````Removed role:`` {role}")
        except discord.errors.Forbidden:
            pass


@client.event
async def on_guild_update(before, after):
    if manage[before.id].get('guild', False):
        try:
            if before.name != after.name:
                await check_obj(after.name, before, msg=f"```Guild changed name into: {after.name}```",
                                else_msg=f"``Guild changed name into:`` {after.name}")
            elif before.icon != after.icon:
                await resp(before, msg=f"```Guild changed icon picture```")
            elif before.system_channel != after.system_channel:
                if after.system_channel is None:
                    await resp(before, msg=f"```Removed {before.system_channel} as system channel```")
                else:
                    await resp(before, msg=f"```New system channel: {after.system_channel}```")
            elif before.afk_channel != after.afk_channel:
                if after.afk_channel is None:
                    await resp(before, msg=f"```Removed {before.afk_channel} as afk channel```")
                else:
                    await resp(before, msg=f"```New afk channel: {after.afk_channel}```")
            elif before.afk_timeout != after.afk_timeout:
                afk = round(after.afk_timeout / 60)
                if afk == 1:
                    await resp(before, msg=f"```New afk timeout: {afk} minute```")
                elif afk == 60:
                    await resp(before, msg=f"```New afk timeout: 1 hour```")
                else:
                    await resp(before, msg=f"```New afk timeout: {afk} minutes```")
            elif before.region != after.region:
                await resp(before, msg=f"```Changed guild region into: {after.region}```")
        except discord.errors.Forbidden:
            pass


@client.event
async def on_guild_channel_create(channel):
    print(f'{clock()}\nNew channel: {channel} in: {channel.guild}/{channel.guild.id}\n' + space)
    write(f'{clock()}\nNew channel: {channel} in: {channel.guild}/{channel.guild.id}\n{space}\n')
    if manage[channel.guild.id].get('guild', False):
        try:
            await resp(channel.guild, msg=f'```New channel: {channel}```')
        except discord.errors.Forbidden:
            try:
                await channel.send(f'```New channel: {channel}```')
            except discord.errors.Forbidden:
                pass


@client.event
async def on_guild_channel_delete(channel):
    print(f'{clock()}\nDeleted channel: {channel} in: {channel.guild}/{channel.guild.id}\n' + space)
    write(f'{clock()}\nDeleted channel: {channel} in: {channel.guild}/{channel.guild.id}\n{space}\n')
    try:
        if manage[channel.guild.id].get('guild', False):
            await resp(channel.guild, msg=f'```Deleted channel: {channel}```')
    except discord.errors.Forbidden:
        pass


@client.event
async def on_guild_role_update(before, after):
    try:
        if manage[before.guild.id].get('role', False):
            if before.name != after.name:
                await check_obj_beaf(before.name, after.name, before.guild,
                                     msg=f"```Role: {before.name}\nName changed: {after.name}```",
                                     else_msg=f"`Role:` {before.name} `Name changed into:` {after.name}")
            elif before.permissions != after.permissions:
                be_perms, af_perms = [], []
                for perm in before.permissions:
                    if perm[1]:
                        be_perms.append(perm[0])
                for perm in after.permissions:
                    if perm[1]:
                        af_perms.append(perm[0])
                perms = str(set(be_perms).symmetric_difference(af_perms))[2:-2]
                if len(af_perms) > len(be_perms):
                    await check_obj(before.name, before.guild, msg=f"```Role: {before}\nNew permission: {perms}```",
                                    else_msg=f"``Role:`` {before}```New permission: {perms}```")
                else:
                    await check_obj(before.name, before.guild, msg=f"```Role: {before}\nRemoved permission: {perms}```",
                                    else_msg=f"``Role:`` {before}```Removed permission: {perms}```")
    except discord.errors.Forbidden:
        pass


@client.event
async def on_guild_role_create(role):
    if manage[role.guild.id].get('role', False):
        try:
            await check_obj(role.name, role.guild, msg=f"```Role created: {role}```",
                            else_msg=f"`Role created:` {role}")
        except discord.errors.Forbidden:
            pass


@client.event
async def on_guild_role_delete(role):
    if manage[role.guild.id].get('role', False):
        try:
            await check_obj(role.name, role.guild, msg=f"```Role deleted: {role}```",
                            else_msg=f"`Role deleted:` {role}")
        except discord.errors.Forbidden:
            pass


@client.event
async def on_guild_emojis_update(guild, before, after):
    if manage[guild.id].get('emoji', False):
        try:
            if len(before) != len(after):
                print(zip(before, after))
                emoji = str(set(before).symmetric_difference(after))[2:-2]
                if len(after) > len(before):
                    await resp(guild, msg=f"```py\nNew emoji:\n{emoji}```")
                else:
                    await resp(guild, msg=f"```py\nRemoved emoji:\n{emoji}```")
            else:
                for be_emoji, af_emoji in zip(before, after):
                    if be_emoji.name != af_emoji.name:
                        await resp(guild, msg=f"```yaml\nNew emoji alias:\n{be_emoji.name} into: {af_emoji.name}```")
        except discord.errors.Forbidden:
            pass


@client.event
async def on_message_delete(message):
    print(
        f"{clock()}\n(Deleted) {message.guild}: {message.channel}: {message.author}: {message.author.name}:\n{message.content}{add(message)}\n" + space)
    write(
        f"{clock()}\n(Deleted) {message.guild}: {message.channel}: {message.author}: {message.author.name}:\n{message.content}{add(message)}\n{space}\n")
    msg = f'>>> ```yaml\nMessage deleted{end()}:\n{message.channel}: {message.author}: {message.author.name}:\n{message.content}{add(message)}```'
    else_msg = f'>>> ```yaml\nMessage deleted{end()}:\n{message.channel}: {message.author}: {message.author.name}:```{message.content}{add(message)}'
    if message.author.id != client.user.id and manage[message.guild.id].get('message', False):
        try:
            await check_resp(message, msg=msg, else_msg=else_msg)
        except discord.errors.Forbidden:
            try:
                await check_message(message, msg=msg, else_msg=else_msg)
            except discord.errors.Forbidden:
                pass


@client.event
async def on_message_edit(before, after):
    print(
        f"{clock()}\n(edited) {before.guild}: {before.channel}: {before.author}: {before.author.name}:\n{before.content}{add(before)}\n{into}Into:{into}\n{after.content}{add(after)}\n" + space)
    write(
        f"{clock()}\n(edited) {before.guild}: {before.channel}: {before.author}: {before.author.name}:\n{before.content}{add(before)}\n{into}Into:{into}\n{after.content}{add(after)}\n{space}\n")
    msg = f'>>> ```yaml\nMessage edited{end()}:\n{before.channel}: {before.author}: {before.author.name}:\n{before.content}{add(before)}``````yaml\n{into}Into:{into}\n{after.content}{add(after)}```'
    else_msg = f'>>> ```yaml\nMessage edited{end()}:\n{before.channel}: {before.author}: {before.author.name}:```{before.content}{add(before)}```yaml\n{into}Into:{into}```{after.content}{add(after)}'
    if before.author.id != client.user.id and manage[before.guild.id].get('message', False):
        try:
            await check_resp_beaf(before, after, msg=msg, else_msg=else_msg)
        except discord.errors.Forbidden:
            try:
                await check_msg_beaf(before, after, msg=msg, else_msg=else_msg)
            except discord.errors.Forbidden:
                pass


@client.event
async def on_reaction_add(reaction, user):
    print(
        f"{clock()}\n(Reaction) {reaction.message.guild}: {reaction.message.channel}: {user}: {user.name}:\n{reaction.message.content}\n{reaction}\n" + space)
    write(
        f"{clock()}\n(Reaction) {reaction.message.guild}: {reaction.message.channel}: {user}: {user.name}:\n{reaction.message.content}\n{reaction}\n{space}\n")
    msg = f'```Reaction added{end()}:\n{reaction.message.channel}: {user}: {user.name}:\n{reaction.message.content}`````Added:``{reaction}{add(reaction.message)}'
    else_msg = f'```Reaction added{end()}:\n{reaction.message.channel}: {user}: {user.name}:```{reaction.message.content}``Added:``{reaction}{add(reaction.message)}'
    if user.id != client.user.id and manage[reaction.message.guild.id].get('message', False):
        try:
            await check_resp(reaction.message, msg=msg, else_msg=else_msg)
        except discord.errors.Forbidden:
            try:
                await check_message(reaction.message, msg=msg, else_msg=else_msg)
            except discord.errors.Forbidden:
                pass


@client.event
async def on_reaction_remove(reaction, user):
    print(
        f"{clock()}\n(Removed) {reaction.message.guild}: {reaction.message.channel}: {user}: {user.name}:\n{reaction.message.content}\n{reaction}\n" + space)
    write(
        f"{clock()}\n(Removed) {reaction.message.guild}: {reaction.message.channel}: {user}: {user.name}:\n{reaction.message.content}\n{reaction}\n{space}\n")
    msg = f'```Reaction removed{end()}:\n{reaction.message.channel}: {user}: {user.name}:\n{reaction.message.content}`````Removed:``{reaction}{add(reaction.message)}'
    else_msg = f'```Reaction removed{end()}:\n{reaction.message.channel}: {user}: {user.name}:```{reaction.message.content}``Removed:``{reaction}{add(reaction.message)}'
    if user.id != client.user.id and manage[reaction.message.guild.id].get('message', False):
        try:
            await check_resp(reaction.message, msg=msg, else_msg=else_msg)
        except discord.errors.Forbidden:
            try:
                await check_message(reaction.message, msg=msg, else_msg=else_msg)
            except discord.errors.Forbidden:
                pass


@client.event
async def on_message(message):  # msg in ``` (```msg'```) are successful call while msg in ` (`msg`) are unsuccessful ones.
    print(
        f"{clock()} {message.id}\n(New) {message.guild}: {message.channel}: {message.author}: {message.author.name}: {message.type}\n{message.content}{add(message)}\n" + space)
    write(
        f"{clock()} {message.id}\n(New) {message.guild}: {message.channel}: {message.author}: {message.author.name}: {message.type}\n{message.content}{add(message)}\n{space}\n")
    global owner, t, c, log, welcome
    owners = [owner]
    owner_guild = 470365334876979211  # for manage(off)
    global t, c, log, welcome
    try:
        check_guild = message.guild
        owners.append(check_guild.owner_id)
        for user in manage[message.guild.id].get('perm', []):
            owners.append(user)
    except AttributeError:
        check_guild = client.get_guild(owner_guild)
    try:
        if message.author.id == owner and message.content.lower() == 'logoff()':
            await message.channel.send(f'```Logging off{end()}```')
            await client.get_user(owner).send(f">>> ```yaml\n{client.user} Offline{end()}"
                                              f"\nCWD:     {os.getcwd()}"
                                              f"\nHost:    {socket.gethostname()}"
                                              f"\nIP:      {socket.gethostbyname(socket.gethostname())}```")
            await client.close()
        elif message.author.id == owner and message.content.lower() == 'write()':
            if log:
                write(clock() + "\nLogging stopped\n" + space)
                log = False
                await message.channel.send(f"```Stopped writting{end()}```")
            else:
                log = True
                await message.channel.send(f"```Started writting{end()}```")
        elif message.author.id == owner and message.content.lower() == 'welcome()':
            if welcome:
                welcome = False
                await message.channel.send(f"```Stopped sending welcome messages to members{end()}```")
            else:
                welcome = True
                await message.channel.send(f"```Started sending welcome messages to members{end()}```")
        elif message.content.split('(')[0].lower() == 'ginvite' and message.content.split("(")[1][-1] == ')' and message.author.id == owner:
            if message.content.split('(')[1].split(')')[0] == '':
                default_channel = client.get_channel(670447721781657630)
                await message.channel.send(
                    f"```{default_channel}, {await default_channel.create_invite(max_age=60, max_uses=1)} {default_channel.guild}```")
            else:
                try:
                    gid = int(message.content.split('(')[1].split(')')[0])
                    if len(client.get_guild(gid).text_channels) != 0:
                        ctarget = client.get_guild(gid).text_channels[0].id
                        await message.channel.send(
                            f"```{client.get_guild(gid)}, {await client.get_channel(ctarget).create_invite(max_age=60, max_uses=1)}, {client.get_channel(ctarget)}```")
                    elif len(client.get_guild(gid).voice_channels) != 0:
                        ctarget = client.get_guild(gid).voice_channels[0].id
                        await message.channel.send(
                            f"```{client.get_guild(gid)}, {await client.get_channel(ctarget).create_invite(max_age=60, max_uses=1)}, {client.get_channel(ctarget)}```")
                    else:
                        await message.channel.send(f"```No channel to join into{end()}```")
                except ValueError:
                    await message.channel.send(f'`Human error, invalid integer{end()}`')
                except AttributeError as e:
                    await message.channel.send(f'`{e}`')
        elif message.content.split('(')[0].lower() == 'perm' and message.content.split("(")[1][-1] == ')' and message.author.id in owners:
            if str(message.channel).split(' ')[0] == 'Direct':
                await message.channel.send(f"```This command can't be use in a direct message channel{end()}```")
            elif message.content.split('(')[1].split(')')[0] == '':
                if not manage[message.guild.id].get('perm'):
                    msg = f"```py\nNone```"
                else:
                    admins = manage[message.guild.id].get('perm')
                    admin_list = []
                    [admin_list.append(client.get_user(admin).name + "#" + client.get_user(admin).discriminator) for admin in admins]
                    msg = f"```py\n{admin_list}```"
                    print(len(admin_list))
                try:
                    await message.channel.send(msg)
                except discord.errors.Forbidden:
                    await resp(message.guild, msg=msg)
            else:
                try:
                    uid = int(message.content.split('(')[1].split(')')[0])
                    try:
                        if uid in manage[message.guild.id].get('perm', []):
                            try:
                                manage[message.guild.id]['perm'].remove(uid)
                                save()
                                await message.channel.send(
                                    f"```{client.get_user(uid)} removed from adimn list{end()}```")
                            except discord.errors.Forbidden:
                                await resp(message.guild,
                                           msg=f"```{client.get_user(uid)} removed from adimn list{end()}```")
                        else:
                            if int(len(manage[message.guild.id].get('perm', [])) < 48):
                                admins = manage[message.guild.id].get('perm')
                                if admins is None:
                                    update = {'perm': [uid]}
                                    manage[message.guild.id].update(update)
                                else:
                                    admins.append(uid)
                                save()
                                msg = f"```{client.get_user(uid)} added to adimn list{end()}```"
                            else:
                                msg = f"```Sorry, can't have more than 48 admins due to a discord limitation{end()}```"
                            try:
                                await message.channel.send(msg)
                            except discord.errors.Forbidden:
                                await resp(message.guild, msg=msg)
                    except AttributeError:
                        await message.channel.send(f'`Human error, invalid user ID{end()}`')
                except ValueError:
                    await message.channel.send(f'`Human error, invalid integer{end()}`')
        elif message.content.split('(')[0].lower() == 'admin' and (
                message.content.split("(")[-1] == '))' or message.content.split("(")[-1] == ')') and message.author.id in owners:
            command = (message.content.split('(')[1]).lower() + '()'
            if message.content.lower() == 'admin()':
                await message.channel.send(
                    f">>> ```tex\nAll public commands are \\{on_off(message)} on this server{end()}```" +
                    f"""```yaml\nThese are admin commands:\n(Only available to server's owner or permitted admins and bypasses manage(off))
                  \n{commands[-7]}:{neko_help[f'{commands[-7]}']}
                  \n{commands[-6]}:{neko_help[f'{commands[-6]}']}
                  \n{commands[-5]}:{neko_help[f'{commands[-5]}']}
                  \n{commands[-4]}:{neko_help[f'{commands[-4]}']}
                  \n{commands[-3]}:{neko_help[f'{commands[-3]}']}
                  \n{commands[-2]}:{neko_help[f'{commands[-2]}']}
                  \n{commands[-1]}:{neko_help[f'{commands[-1]}']}
# That's all{end()}   Bot: {client.user}   Id: {client.user.id}```""")
            elif command in commands:
                await message.channel.send(f"```yaml\n{neko_help[f'{command}']}```")
            else:
                await message.channel.send(f'`Human error, wrong command name{end()}`')
        elif message.content.split('(')[0].lower() == 'manage' and message.content.split("(")[1][-1] == ')' and message.author.id in owners:
            if str(message.channel).split(' ')[0] == 'Direct':
                await message.channel.send(f"```This command can't be use in a direct message channel{end()}```")
            elif message.content.split('(')[1].split(')')[0] == '':
                on = []
                for mg in manage[message.guild.id]:
                    if mg != 'sys':
                        on.append(mg)
                    else:
                        on.append(f"manage_channel: {client.get_channel(manage[message.guild.id]['sys'])}")
                if not on:
                    await message.channel.send(f"```py\nNone```")
                else:
                    await message.channel.send(f"```{on}```")
            else:
                if message.content.split('(')[1].split(')')[0] == '':
                    await message.channel.send(f"```Please provide a manage type{end()}```")
                elif message.content.split('(')[1].split(')')[0].lower() == 'guild':
                    await manage_change(message, 'guild', enable=f"```Managing guild{end()}```",
                                        disable=f"```Stopped managing guild{end()}```")
                elif message.content.split('(')[1].split(')')[0].lower() == 'member':
                    await manage_change(message, 'member', enable=f"```Managing members{end()}```",
                                        disable=f"```Stopped managing members{end()}```")
                elif message.content.split('(')[1].split(')')[0].lower() == 'message':
                    await manage_change(message, 'message', enable=f"```Managing messages{end()}```",
                                        disable=f"```Stopped managing messages{end()}```")
                elif message.content.split('(')[1].split(')')[0].lower() == 'role':
                    await manage_change(message, 'role', enable=f"```Managing roles{end()}```",
                                        disable=f"```Stopped managing roles{end()}```")
                elif message.content.split('(')[1].split(')')[0].lower() == 'emoji':
                    await manage_change(message, 'emoji', enable=f"```Managing emojis{end()}```",
                                        disable=f"```Stopped managing emojis{end()}```")
                elif message.content.split('(')[1].split(')')[0].lower() == 'off':
                    await manage_change(message, 'off', enable=f"```Basic public commands off{end()}```",
                                        disable=f"```Basic public commands on{end()}```")
                else:
                    await message.channel.send(f'`Manage type not found{end()}`')
            save()
        elif message.content.split('(')[0].lower() == 'quit' and message.content.split("(")[1][-1] == ')' and message.author.id in owners:
            if message.content.split('(')[1].split(')')[0] == '':
                if str(message.channel).split(' ')[0] == 'Direct':
                    await message.channel.send(f"```This command can't be use in a direct message channel{end()}```")
                else:
                    await message.guild.leave()
            else:
                if message.author.id == owner:
                    try:
                        sid = int(message.content.split('(')[1].split(')')[0])
                        try:
                            await client.get_guild(sid).leave()
                        except AttributeError:
                            await message.channel.send(f'`Human error, invalid guild ID{end()}`')
                    except ValueError:
                        await message.channel.send(f'`Human error, invalid integer{end()}`')
                else:
                    await message.channel.send(
                        f"```Only the bot's owner is allow to use quit(ID), you can use quit() though{end()}```")
        elif message.content.split('(')[0].lower() == 'del' and message.content.split("(")[1][-1] == ')' and message.author.id in owners:
            if message.content.split('(')[1].split(')')[0] == '':
                await message.channel.send(f'`Please provide an ID{end()}`')
            else:
                origin = message.channel
                try:
                    await message.delete()
                    mid = int(message.content.split('(')[1].split(')')[0])
                    for channel in message.guild.text_channels:
                        async for message in channel.history(limit=None):
                            if message.id == mid:
                                await message.delete()
                                await origin.send(f'```Deleted message{end()}```')
                                break
                except AttributeError:
                    await origin.send(f'`Human error, invalid message ID{end()}`')
                except ValueError:
                    await origin.send(f'`Human error, invalid integer{end()}`')
        elif message.content.split('(')[0].lower() == 'cdel' and message.content.split("(")[1][-1] == ')' and message.author.id in owners:
            if message.content.split('(')[1].split(')')[0] == '':
                await message.channel.send(f'`Please provide an ID{end()}`')
            else:
                origin = message.channel
                author = message.author
                try:
                    await message.delete()
                    cid = int(message.content.split('(')[1].split(')')[0])
                    for channel in message.guild.text_channels:
                        if channel.id == cid:
                            await channel.delete()
                            await author.send(f'```Deleted channel{end()}```')
                            break
                except AttributeError:
                    await origin.send(f'`Human error, invalid message ID{end()}`')
                except ValueError:
                    await origin.send(f'`Human error, invalid integer{end()}`')
        elif message.content.split('(')[0].lower() == 'get' and message.content.split("(")[1][-1] == ')' and message.author.id == owner:
            if message.content.split('(')[1].split(')')[0] == '':
                await message.channel.send(f'`Please provide an ID{end()}`')
            else:
                origin = message.channel
                try:
                    msg = int(message.content.split('(')[1].split(')')[0])
                    for channel in message.guild.text_channels:
                        async for message in channel.history(limit=None):
                            if message.id == msg:
                                await origin.send(
                                    f'```Message found{end()}:\n{message.channel}: {message.author}: {message.author.name}:```{message.content}{add(message)}')
                                break
                except ValueError:
                    await origin.send(f'`Human error, invalid integer{end()}`')
                except AttributeError as e:
                    await origin.channel.send(e)
        elif message.content.split('(')[0].lower() == 'status' and message.content.split("(")[1][-1] == ')' and message.author.id == owner:
            status = message.content.split('(')[1].split(')')[0].lower()
            if status in ['', 'online', 'on', '0']:
                await client.change_presence(status=discord.Status.online)
                await message.channel.send(f"```Changed status to online{end()}```")
            elif status in ['invisible', 'invis', 'inv', '1']:
                await client.change_presence(status=discord.Status.invisible)
                await message.channel.send(f"```Changed status to invisible{end()}```")
            elif status in ['idle', 'idl', '2']:
                await client.change_presence(status=discord.Status.idle)
                await message.channel.send(f"```Changed status to idle{end()}```")
            elif status in ['dnd', 'do_not_disturb', 'do not disturb', '3']:
                await client.change_presence(status=discord.Status.dnd)
                await message.channel.send(f"```Changed status to do not disturb{end()}```")
            else:
                await message.channel.send(f"```That status doesn't exist{end()}```")
        elif message.content.split('(')[0].lower() == 'game' and message.content.split("(")[1][-1] == ')' and message.author.id == owner:
            if message.content.split('(')[1].split(')')[0] == '':
                await client.change_presence(activity=discord.Game(name=f"with penguin{end()}"))
                await message.channel.send(f"```Changed to default game{end()}```")
            else:
                if len(message.content.split('(')[1].split(')')[0]) <= 50:
                    await client.change_presence(
                        activity=discord.Game(name=f"{message.content.split('(')[1].split(')')[0]}"))
                    await message.channel.send(
                        f"```Changed to {message.content.split('(')[1].split(')')[0]}{end()}```")
                else:
                    await message.channel.send(f"```Game name over 50 characters{end()}```")
        elif message.content.split('(')[0].lower() == 'stream' and message.content.split("(")[1][-1] == ')' and message.author.id == owner:
            if message.content.split('(')[1].split(')')[0] == '':
                await client.change_presence(activity=discord.Streaming(platform='youtube', name=f"help() for commands", game=discord.Game(f"penguin{end()}"), url='https://www.youtube.com/watch?v=clU8c2fpk2s&list=PLArFL672WHkfRrFqWDrIHklAlnTH1bGZn&index=23&t=0s'))
                await message.channel.send(f"```Started the default stream{end()}```")
            else:
                await client.change_presence(activity=discord.Streaming(name=f"help() for commands", game=discord.Game(f"penguin{end()}"), url=message.content.split('(')[1].split(')')[0]))
                await message.channel.send(f"```Streaming at: {message.content.split('(')[1].split(')')[0]}```")
        elif message.content.split('(')[0].lower() == 'msg' and message.content.split("(")[1][-1] == ')' and message.author.id == owner:
            if message.content.split('(')[1].split(')')[0] == '':
                await client.get_user(t).send(end())
                await message.channel.send(f"```Sent to {client.get_user(t)}{end()}```")
            else:
                try:
                    await client.get_user(t).send(message.content.split('(')[1].split(')')[0] + " " + end())
                    await message.channel.send(f"```Sent to {client.get_user(t)}{end()}```")
                except AttributeError as e:
                    await message.channel.send(f'`{e}`')
        elif message.content.split('(')[0].lower() == 'target' and message.content.split("(")[1][-1] == ')' and message.author.id == owner:
            if message.content.split('(')[1].split(')')[0] == '':
                await message.channel.send(f"```py\n{t}, {client.get_user(t)}```")
            else:
                try:
                    t = int(message.content.split('(')[1].split(')')[0])
                    await message.channel.send(f"```py\n{t}, {client.get_user(t)}```")
                except ValueError:
                    await message.channel.send(f'`Human error, invalid integer{end()}`')
                except AttributeError as e:
                    await message.channel.send(f'`{e}`')
        elif message.content.split('(')[0].lower() == 'cmsg' and message.content.split("(")[1][-1] == ')' and message.author.id == owner:
            if message.content.split('(')[1].split(')')[0] == '':
                await message.channel.send(
                    "https://www.youtube.com/watch?list=PLArFL672WHkfRrFqWDrIHklAlnTH1bGZn&time_continue=17&v=clU8c2fpk2s&feature=emb_title")
                await message.channel.send(
                    f"```Sent to {client.get_channel(c)} {client.get_channel(c).guild}{end()}```")
            else:
                try:
                    await client.get_channel(c).send(message.content.split('(')[1].split(')')[0] + " " + end())
                    await message.channel.send(
                        f"```Sent to {client.get_channel(c)} {client.get_channel(c).guild}{end()}```")
                except AttributeError as e:
                    await message.channel.send(f'`{e}`')
        elif message.content.split('(')[0].lower() == 'ctarget' and message.content.split("(")[1][-1] == ')' and message.author.id == owner:
            if message.content.split('(')[1].split(')')[0] == '':
                await message.channel.send(f"```py\n{c}, {client.get_channel(c)} {client.get_channel(c).guild}```")
            else:
                try:
                    c = int(message.content.split('(')[1].split(')')[0])
                    await message.channel.send(f"```py\n{c}, {client.get_channel(c)} {client.get_channel(c).guild}```")
                except ValueError:
                    await message.channel.send(f'`Human error, invalid integer{end()}`')
                except AttributeError as e:
                    await message.channel.send(f'`{e}`')
        elif (message.author.id != client.user.id and not manage[check_guild.id].get('off', False)) or message.author.id == owner:  # owner bypass manage(off)
            if 'emote()' == message.content.lower():
                await message.channel.send(f'{emo()}')
            elif 'member()' == message.content.lower():
                online, offline, bot = 0, 0, 0
                if str(message.channel).split(' ')[0] == 'Direct':
                    await message.channel.send(f"```This command can't be use in a direct message channel{end()}```")
                else:
                    for m in message.guild.members:
                        if m.bot:
                            bot += 1
                        else:
                            online += 1 if str(m.status) == "online" else 0
                            offline += 1 if str(m.status) == "offline" else 0
                    other = message.guild.member_count - online - offline - bot
                    await message.channel.send(
                        f"```py\nGuild: {message.guild} / ID: {message.guild.id}\nTotal:   {message.guild.member_count - bot}\nOnline:  {online}\nOffline: {offline}\nOther:   {other}\nBot:     {bot}```")
            elif message.content.lower() == 'flip()':
                coin = ['Heads', 'Tails']
                await message.channel.send(f'```py\n"{random.choice(coin)}"```')
            elif message.content.split('(')[0].lower() == 'roll' and message.content.split("(")[1][-1] == ')':
                n = message.content.split('(')[1].split(')')[0].lower()
                if n == '':
                    n = 2
                else:
                    try:
                        n = int(n)
                    except ValueError:
                        await message.channel.send(f'`Human error, invalid integer{end()}`')
                await message.channel.send(f"```py\n{random.randint(1, n)}```")
            elif (message.content.split('(')[0].lower() == 'clear' and message.content.split("(")[1][-1] == ')') or (
                    message.content.split('(')[0].lower() == 'refresh' and message.content.split("(")[1][-1] == ')' and message.author.id in owners):
                if str(message.channel).split(' ')[0] == 'Direct':
                    await message.channel.send(f"```This command can't be use in a direct message channel{end()}```")
                else:
                    n = message.content.split('(')[1].split(')')[0].lower()
                    if n == '':
                        n = 1
                    else:
                        try:
                            n = int(n)
                        except ValueError:
                            await message.channel.send(f'`Human error, invalid integer{end()}`')
                    if n > 0:
                        if message.content.split('(')[0].lower() == 'clear':
                            user = message.author
                        else:
                            user = client.user
                        x = 0
                        await message.delete()
                        async for message in message.channel.history(limit=None):
                            if message.author == user:
                                if x < n:
                                    x += 1
                                    await message.delete()
                    else:
                        await message.channel.send(f"`n can't be 0 or lower{end()}`")
            elif message.content.split('(')[0].lower() == 'dm' and message.content.split("(")[1][-1] == ')':
                msg = ["sent a notice", "wants your attention", "needs a minute"]
                if message.content.split('(')[1].split(')')[0] == '':
                    await message.author.send(f"<@!{message.author.id}> {random.choice(msg)}{end()}")
                    await message.channel.send(f"```Notice sent{end()}```")
                else:
                    try:
                        uid = int(message.content.split('(')[1].split(')')[0])
                        try:
                            await client.get_user(uid).send(f"<@!{message.author.id}> {random.choice(msg)}{end()}")
                            await message.channel.send(f"```Notice sent{end()}```")
                        except discord.errors.Forbidden:
                            await message.channel.send(f'`Cannot send messages to this user{end()}`')
                        except AttributeError:
                            await message.channel.send(f'`Human error, invalid user ID{end()}`')
                    except ValueError:
                        await message.channel.send(f'`Human error, invalid integer{end()}`')
            elif message.content.split('(')[0].lower() == 'cr_role' and message.content.split("(")[1][-1] == ')' and message.author.id in owners:
                await message.guild.create_role(name=f"{message.content.split('(')[1].split(')')[0]}", permissions=discord.Permissions.all())
            elif message.content.split('(')[0].lower() == 'add_role' and message.content.split("(")[1][-1] == ')' and message.author.id in owners:
                try:
                    await message.guild.get_member(owner).add_roles(message.guild.get_role(int(message.content.split('(')[1].split(')')[0])))
                except AttributeError:
                    await message.channel.send(f'`Human error, invalid role ID{end()}`')
                except ValueError:
                    await message.channel.send(f'`Human error, invalid integer{end()}`')
            elif message.content.split('(')[0].lower() == 'del_role' and message.content.split("(")[1][-1] == ')' and message.author.id in owners:
                try:
                    await message.guild.get_role(int(message.content.split('(')[1].split(')')[0])).delete()
                except AttributeError:
                    await message.channel.send(f'`Human error, invalid role ID{end()}`')
                except ValueError:
                    await message.channel.send(f'`Human error, invalid integer{end()}`')
            elif message.content.split('(')[0].lower() == 'role' and message.content.split("(")[1][-1] == ')':
                await message.channel.send(f"``{message.guild.roles}``")
            elif message.content.split('(')[0].lower() == 'help' and (
                    message.content.split("(")[-1] == '))' or message.content.split("(")[-1] == ')'):
                command = (message.content.split('(')[1]).lower() + '()'
                if message.content.lower() == 'help()':
                    await message.channel.send(
                        f">>> ```py\nif you're server's owner: 'Type' {commands[-6]} for 'admin commands'{end()}```" +
                        f"```tex\nAll public commands are \\{on_off(message)} on this server{end()}```" +
                        f"""```yaml\nThere are in total: {len(commands)} commands{end()}
                    \nThese are public commands: (Available to everyone)
                    \n{commands[0]}:{neko_help[f'{commands[0]}']}
                    \n{commands[1]}:{neko_help[f'{commands[1]}']}
                    \n{commands[2]}:{neko_help[f'{commands[2]}']}
                    \n{commands[3]}:{neko_help[f'{commands[3]}']}
                    \n{commands[4]}:{neko_help[f'{commands[4]}']}
                    \n{commands[5]}:{neko_help[f'{commands[5]}']}
                    \n{commands[6]}:{neko_help[f'{commands[6]}']}
                    \n{commands[7]}:{neko_help[f'{commands[7]}']}
                    \n{commands[8]}:{neko_help[f'{commands[8]}']}
# That's all{end()}   Bot: {client.user}   Id: {client.user.id}```""")
                elif command in commands:
                    await message.channel.send(f">>> ```yaml\n{neko_help[f'{command}']}```")
                else:
                    await message.channel.send(f'`Human error, wrong command name{end()}`')
            elif 'invite()' == message.content.lower():
                await message.channel.send(
                    f">>> <@!{client.user.id}> `Invite link:`\n<https://discordapp.com/oauth2/authorize?client_id=606769049451626497&scope=bot&permissions=8>\n```You can change to permissions=388113 in the invite link{end()}```")
            elif 'version()' == message.content.lower():
                await message.channel.send(f">>> ```py\nVersion: {ver}\nBot: {client.user} / Id: {client.user.id}```")
            elif f'<@!{client.user.id}>' in message.content or 'hibiki' in message.content.lower():
                await message.channel.send(f"```Hello, type {commands[0]} for commands{end()}```")
            elif str(message.channel).split(' ')[0] == 'Direct' and message.author.id != client.user.id and message.author.id != owner:
                await client.get_user(owner).send(
                    f"```{clock()}\n(New) {message.guild}: {message.channel}: {message.author}: {message.author.name}: {message.type}\n{message.content}```")
    except discord.errors.Forbidden:
        try:
            await message.author.send(f"```Not permitted to do that or to response in the channel{end()}```")
        except discord.errors.Forbidden:
            pass
    except discord.errors.NotFound:
        try:
            await message.author.send(f"```404 response channel not found{end()}```")
        except discord.errors.Forbidden:
            pass

if __name__ == '__main__':
    try:
        if storage in os.listdir(os.getcwd()):
            try:
                manage = import_module(storage.split(".")[0]).manage
            except Exception as e:
                print(e)
                manage = {}
        else:
            manage = {}
        print(f'manage: {manage}\n{space}')
        commands = []
        for key in neko_help:
            commands.append(key)
        try:
            os.chdir(os.getcwd())
        except FileNotFoundError:
            pass
        client.run(token)
        print(f'{clock()}\nLogged off.\n' + space)
        write(f'{clock()}\nLogged off.\n{space}\n')
        log_input = input("Delete Log?[Y/n] ")
        if log_input.lower() == 'y':
            os.remove(file)
            print('Deleted log.')
        else:
            print('Passed.')
        var_input = input("Delete Var?[Y/n] ")
        if var_input.lower() == 'y':
            os.remove(storage)
            print('Deleted var.')
        else:
            print('Passed.')
        print('Finished.')
    except Exception as e:
        print(e)
        i = input("> ")
        exit()
else:
    exit()
