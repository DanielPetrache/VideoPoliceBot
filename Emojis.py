import numpy
from discord.ext import commands
import sqlite3


class Emojis_class(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @staticmethod
    async def handle_reaction_add(payload):
        conn = sqlite3.connect('emojis.db')
        curs = conn.cursor()
        curs.execute("PRAGMA foreign_keys;")
        if payload.emoji.id is None:
            test_str = "A"
            for item in curs.execute("SELECT id, emoji_name FROM emojis WHERE emoji_name = ?", (payload.emoji.name,)):
                test_str = item[0]

            if test_str == "A":
                emoji_id = numpy.random.randint(low=1000, high=999999999)
                curs.execute("INSERT INTO emojis (id, emoji_name) "
                             "VALUES (?, ?);", (emoji_id, payload.emoji.name))
                curs.execute("INSERT INTO emoji_count (user_id, emoji_id, user_name, emoji_name, counter) "
                             "VALUES (?, ?, ?, ?, ?);",
                             (payload.user_id, emoji_id, payload.member.name, payload.emoji.name, 1))
                conn.commit()
                print("Am adaugat " + payload.emoji.name + " la baza de date")
                # logging.info("Am adaugat " + payload.emoji.name + " la baza de date. Mesajul a fost: ")
            else:
                for item in curs.execute("SELECT user_id, emoji_name, counter FROM emoji_count WHERE user_id = ? AND "
                                         "emoji_name = ?;", (payload.user_id, payload.emoji.name)):
                    curs.execute("UPDATE emoji_count SET counter = ? WHERE user_id = ? "
                                 "AND emoji_name = ?", (item[2] + 1, item[0], item[1]))
                    conn.commit()

        else:
            for item in curs.execute("SELECT user_id, emoji_name, counter FROM emoji_count WHERE user_id = ? AND "
                                     "emoji_name = ?;", (payload.user_id, payload.emoji.name)):
                curs.execute("UPDATE emoji_count SET counter = ? WHERE user_id = ? "
                             "AND emoji_name = ?;", (item[2] + 1, item[0], item[1]))
                conn.commit()
                # print(item[2] + 1, item[0], item[1])
        conn.close()

    @staticmethod
    async def handle_reaction_edit(payload):
        conn = sqlite3.connect('emojis.db')
        curs = conn.cursor()
        curs.execute("PRAGMA foreign_keys;")
        for item in curs.execute("SELECT user_id, emoji_name, counter FROM emoji_count WHERE user_id = ? AND "
                                 "emoji_name = ?;", (payload.user_id, payload.emoji.name)):
            curs.execute("UPDATE emoji_count SET counter = ? WHERE user_id = ? "
                         "AND emoji_name = ?;", (item[2] - 1, item[0], item[1]))
            conn.commit()
            # print(item[2] + 1, item[0], item[1])
        conn.close()

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
    bot.add_cog(Emojis_class(bot))
