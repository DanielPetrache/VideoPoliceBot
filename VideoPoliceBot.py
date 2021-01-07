import discord
from discord.ext import commands
import time

TOKEN = 'YourToken'
intents = discord.Intents.default()
intents.members = True
VideoPoliceBot = discord.Client(intents=intents)


class MyClient(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def connect(self, ctx, *, channel: discord.VoiceChannel):
        if ctx.voice_client is not None:
            return await ctx.voice_client.move_to(channel)
        await channel.connect()


@VideoPoliceBot.event
async def on_ready():
    print('Logged in as {0} ({0.id})'.format(VideoPoliceBot.user))
    print('------')
    while True:
        for channel in VideoPoliceBot.get_all_channels():
            nr_members = 0
            channel_members = []
            video_already_on = []
            if type(channel) == discord.channel.VoiceChannel:
                video_number = 0
                no_video_number = 0
                # print(channel)
                for y in channel.members:
                    nr_members += 1
                    # if y != None:
                    # print(y, y.id, y.name, y.bot)
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
                        for member in channel.members:
                            if not channel.voice_states[member.id].self_video:
                                await member.send(
                                    "Salut, ai un minut sa pornesti webcam-ul, otherwise I will clap your cheeks. "
                                    ":wink:")
                            else:
                                video_already_on.append(member.id)

                        t1 = time.time()
                        while True:
                            if (time.time() - t1) >= 5:
                                break

                        for member in channel.members:
                            new_channel = await VideoPoliceBot.fetch_channel(channel.id)
                            if (new_channel.voice_states[member.id].self_video == True) and (
                                    not (member.id in video_already_on)):
                                await member.send("Ai pornit, bravo! :hugging:")
                            elif not new_channel.voice_states[member.id].self_video:
                                await member.move_to(None)
        time.sleep(10)

VideoPoliceBot.run(TOKEN)
