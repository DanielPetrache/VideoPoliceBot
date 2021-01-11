import discord
from discord.ext import commands
import time
import random

TOKEN = 'Nzk2MzE3MzgwMTMyNDcwODA0.X_WKWg.EBj7bKGzh0t6gwtDoH8EaWtpJ-I'
intents = discord.Intents.default()
intents.members = True
VideoPoliceBot = discord.Client(intents=intents)
andries_counter = 0
radu_counter = 0

@VideoPoliceBot.event
async def on_ready():
    print('Logged in as {0} ({0.id})'.format(VideoPoliceBot.user))
    print('------')
    while True:
        for channel in VideoPoliceBot.get_all_channels():
            channel = await VideoPoliceBot.fetch_channel(channel.id)
            channel_members = []
            video_already_on = []
            if type(channel) == discord.channel.VoiceChannel:
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
                                new_channel = await VideoPoliceBot.fetch_channel(channel.id)
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
        time.sleep(10)


@VideoPoliceBot.event
async def on_message(message):
    global radu_counter, andries_counter
    if message.author.id == 134946430317101057 or message.author.id == 237625040181526528:
        if message.author.id == 134946430317101057:
            radu_counter += 1
            if random.randint(1, 50 + radu_counter) < 25:
                await message.channel.send(file=discord.File('ciocoflender.jpg'))
                print("L-am facut ciocoflender pe", message.author.name)
        else:
            andries_counter += 1
            if random.randint(1, 50 + andries_counter) < 25:
                await message.channel.send(file=discord.File('ciocoflender.jpg'))
                print("L-am facut ciocoflender pe", message.author.name)


VideoPoliceBot.run(TOKEN)
