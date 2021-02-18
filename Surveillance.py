from discord.ext import commands
import time


class Surveillance(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.trigger_instanta = False

    @commands.command()
    async def surveillance(self, ctx, trigger: str):
        if trigger == 'on':
            if self.trigger_instanta:
                await ctx.send(":cop: Politia e deja aici! :cop:")
            else:
                await ctx.send(":police_officer: A venit Politia! :police_officer:")
                self.trigger_instanta = True
                # logging.info(ctx.author.name + " a chemat politia.")
        else:
            if not self.trigger_instanta:
                await ctx.send(":police_car: Politia a plecat deja! :police_car:")
            else:
                await ctx.send(":police_car: A plecat Politia! :police_car:")
                # logging.info(ctx.author.name + " a izgonit politia.")
                self.trigger_instanta = False

        while self.trigger_instanta:
            voice_channels = []
            channels = await ctx.guild.fetch_channels()
            for channel in channels:
                if channel.type.name == 'voice':
                    voice_channels.append(channel)
            for channel in voice_channels:
                channel_members = []
                video_already_on = []
                video_number = 0
                no_video_number = 0
                for i in channel.voice_states:
                    if channel.voice_states[i].self_video:
                        video_number += 1
                    else:
                        for member in channel.members:
                            if i == member.id:
                                if not member.bot:
                                    no_video_number += 1
                                    channel_members.append(i)
                if video_number + no_video_number != 0:
                    if video_number / (video_number + no_video_number) >= 0.5:
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
                                    # logging.info("L-am avertizat pe ", member.name)
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
                                new_channel = await self.bot.fetch_channel(channel.id)
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
                                        # logging.info("I-am dat kick lui ", member.name)
                                    except Exception:
                                        print("N-am putut sa trimit mesaj lui", member.name)
            print("Monitorizez canale")
            time.sleep(10)


def setup(bot):
    bot.add_cog(Surveillance(bot))
