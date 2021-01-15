import discord
from discord.ext import commands
import time
import random

TOKEN = ''
intents = discord.Intents.default()
intents.members = True
# VideoPoliceBot = discord.Client(intents=intents)
descript = '''!help - help me daddy \n!surveillance (on/off) - porneste politia sau o opreste \n!ciocoflender (on/off) - se uita sau nu dupa ciocoflenderi '''
VideoPoliceBot = commands.Bot(command_prefix='!', description=descript, intents=intents)
andries_counter = 0
radu_counter = 0
trigger_instanta = 0
ciocoflender_trigger = 0


@VideoPoliceBot.event
async def on_ready():
    print('Logged in as')
    print(VideoPoliceBot.user.name)
    print(VideoPoliceBot.user.id)
    print('SUNT BOT ON')
    print('-----------')


@VideoPoliceBot.command()
async def surveillance(ctx, trigger: str):
    global trigger_instanta
    if trigger == 'on':
        await ctx.send(":police_officer: A venit Politia! :police_officer:")
        trigger_instanta = 1
    else:
        await ctx.send(":police_car: A plecat Politia! :police_car:")
        trigger_instanta = 0
    while trigger_instanta:
        voice_channels = []
        channels = await ctx.guild.fetch_channels()
        for channel in channels:
            if (channel.type.name == 'voice'):
                voice_channels.append(channel)
        for channel in voice_channels:
            channel_members = []
            video_already_on = []
            video_number = 0
            no_video_number = 0
            # print(channel)
            for i in channel.voice_states:
                # print(i)
                if channel.voice_states[i].self_video:
                    video_number += 1
                else:
                    for member in channel.members:
                        if i == member.id:
                            if not member.bot:
                                no_video_number += 1
                                channel_members.append(i)
            # print(video_number, no_video_number)
            # print(channel_members)
            if video_number + no_video_number != 0:
                if video_number / (video_number + no_video_number) >= 0.5:
                    # print("######################")
                    member_with_no_video = False
                    for member in channel.members:
                        if not channel.voice_states[member.id].self_video and not member.bot and not \
                                channel.voice_states[member.id].self_deaf:
                            member_with_no_video = True
                            try:
                                await member.send(
                                    "Salut, ai 15 secunde sa pornesti webcam-ul, otherwise I will clap your "
                                    "cheeks. "
                                    ":wink:")
                                print("L-am avertizat pe ", member.name)
                            except Exception:
                                print("N-am putut sa trimit mesaj lui", member.name)
                        else:
                            video_already_on.append(member.id)
                    if member_with_no_video:
                        t1 = time.time()
                        while True:
                            if (time.time() - t1) >= 15:
                                break

                        for member in channel.members:
                            new_channel_list = await ctx.guild.fetch_channels()
                            for item in new_channel_list:
                                if item.id == channel.id:
                                    new_channel = item
                                    if (new_channel.voice_states[member.id].self_video is True) and (
                                            not (member.id in video_already_on)) and not member.bot:
                                        try:
                                            await member.send("Ai pornit, bravo! :hugging:")
                                        except Exception:
                                            print("N-am putut sa trimit mesaj lui", member.name)
                                    elif not new_channel.voice_states[member.id].self_video and not member.bot and not \
                                            channel.voice_states[member.id].self_deaf:
                                        await member.move_to(None)
                                        try:
                                            await member.send("N-ai ce cauta pe canal fara webcam! :police_officer:")
                                            print("I-am dat kick lui ", member.name)
                                        except Exception:
                                            print("N-am putut sa trimit mesaj lui", member.name)
        print("Monitorizez canale")
        time.sleep(10)


@VideoPoliceBot.command()
async def ciocoflender(ctx, value: str):
    global ciocoflender_trigger
    if value == 'on':
        ciocoflender_trigger = 1
        await ctx.send(":eyes: Ma uit dupa ciocoflenderi! :eyes:")
    else:
        ciocoflender_trigger = 0
        await ctx.send(":sleeping: Nu ma mai uit dupa ciocoflenderi! :sleeping:")


@VideoPoliceBot.event
async def on_message(message):
    await VideoPoliceBot.process_commands(message)
    global ciocoflender_trigger
    if ciocoflender_trigger == 1:
        global radu_counter, andries_counter
        if message.author.id == 134946430317101057 or message.author.id == 237625040181526528:
            if message.author.id == 134946430317101057:
                radu_counter += 1
                if random.randint(1, 10 ) == 1:
                    await message.channel.send(file=discord.File('ciocoflender.jpg'))
                    print("L-am facut ciocoflender pe", message.author.name)
            else:
                andries_counter += 1
                if random.randint(1, 10 ) == 1:
                    await message.channel.send(file=discord.File('ciocoflender.jpg'))
                    print("L-am facut ciocoflender pe", message.author.name)
    else:
        pass

VideoPoliceBot.run(TOKEN)
