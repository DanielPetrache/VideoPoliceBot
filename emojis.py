import discord
from discord.ext import commands
import sqlite3


class Emojis(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def topemoji(self, ctx, user: str, number: int):
        if type(number) != int or number < 1:
            await ctx.send("Trebuie sa folosesti un numar intreg intre 1 si 15!")
        else:
            if number > 15:
                await ctx.send("Ia-o mai usor, incearca un nr <= 15")
            else:
                id_user = "xxx"
                member_dict = {}
                for member in ctx.guild.members:
                    if not member.bot:
                        if member.nick:
                            member_dict[member.name.replace(" ", "")] = member.nick.replace(" ", "")
                        else:
                            member_dict[member.name.replace(" ", "")] = "nuamnickname"

                        try:
                            if user.lower() == member.name.lower().replace(" ", "") \
                                    or user.lower() == member.nick.lower().replace(" ", ""):
                                id_user = str(member.id)
                                break
                        except AttributeError:
                            if user.lower() == member.name.lower().replace(" ", ""):
                                id_user = str(member.id)
                                break

                if id_user == "xxx":
                    s = "Nu exista " + user + " pe server"
                    await ctx.send(s)
                else:
                    conn = sqlite3.connect('emojis.db')
                    curs = conn.cursor()
                    curs.execute("PRAGMA foreign_keys;")
                    nr = 1
                    message = ""

                    for row in curs.execute("SELECT user_name, emoji_name, emoji_id, counter FROM emoji_count WHERE "
                                            "user_id = ? ORDER BY counter DESC LIMIT ?", (id_user, number)):
                        if int(row[2]) < 999999999:
                            message += "Locul #" + str(nr) + " " + row[1] + ": " + str(row[3]) + " utilizari\n"
                        else:
                            message += "Locul #" + str(nr) + " <:" + row[1] + ":" + row[2] + "> : " + str(
                                row[3]) + " utilizari\n"
                        nr += 1
                    await ctx.send(message)
                    # print(row)
                    conn.commit()
                    conn.close()
                    # logging.info("Am afisat topul pentru " + user + " la comanda lui " + ctx.author.name)

    @topemoji.error
    async def missing_parameters(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            comand = ctx.message.content
            comand = comand.replace("!topemoji", "")
            if comand == "":
                await self.topemoji(ctx, ctx.author.name, 5)
            else:
                number = ""
                for char in comand:
                    if char.isdigit():
                        number += char
                if number == "":
                    comand = comand.replace(" ", "")
                    if comand == "":
                        await self.topemoji(ctx, ctx.author.name, 5)
                    else:
                        await self.topemoji(ctx, comand, 5)
                else:
                    comand = comand.replace(number, "")
                    comand = comand.replace(" ", "")
                    await self.topemoji(ctx, ctx.author.name, int(number))


def setup(bot):
    bot.add_cog(Emojis(bot))
