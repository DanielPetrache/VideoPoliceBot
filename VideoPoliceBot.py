import discord
from discord.ext import commands
import time
import random
import sqlite3
import numpy
# import logging
import TicTacToeGame

# logging.basicConfig(filename='bot.log', format='%(asctime)s %(message)s', level='INFO')
TOKEN = ''
intents = discord.Intents.default()
intents.members = True
descript = "!help - help me daddy \n!surveillance (on/off) - porneste politia sau o opreste\n!ciocoflender (on/off) - " \
           "se uita sau nu dupa ciocoflenderi\n!populate_db - numai pentru cine trebuie\n!topemoji (user, " \
           "emoji_count) - afiseaza un top al celor emoji_count cele mai " \
           "folosite emoji-uri de catre user (emoji_count <= 15)\n" \
           "!tictactoe @user1 @user2 - incepe un meci de X si 0 intre cei doi useri pe un canal privat\n" \
           "!place linie coloana - ii spune botului unde sa puna X-ul sau 0-ul"
VideoPoliceBot = commands.Bot(command_prefix='!', description=descript, intents=intents)
lista_jocuri = []
trigger_instanta = 0
ciocoflender_trigger = 0


@VideoPoliceBot.event
async def on_ready():
    print('Logged in as')
    print(VideoPoliceBot.user.name)
    print(VideoPoliceBot.user.id)
    print('-----------')
    # logging.info("-----Am pornit-----")


@VideoPoliceBot.command()
async def populate_db(ctx):
    if ctx.author == ctx.guild.owner:
        conn = sqlite3.connect('emojis.db')
        curs = conn.cursor()
        curs.execute("PRAGMA foreign_keys;")
        members_list = ctx.guild.members
        emojis_list = ctx.guild.emojis

        for member in members_list:
            if not member.bot:
                curs.execute("INSERT INTO users (id, user_name) VALUES (?, ?)", (member.id, member.name))

        for emoji in emojis_list:
            curs.execute("INSERT INTO emojis (id, emoji_name) VALUES (?, ?)", (emoji.id, emoji.name,))

        for member in members_list:
            if not member.bot:
                for emoji in emojis_list:
                    curs.execute("INSERT INTO emoji_count (user_id, emoji_id, user_name, emoji_name, counter) VALUES "
                                 "(?, ?, ?, ?, ?)", (member.id, emoji.id, member.name, emoji.name, 0))
        conn.commit()
        conn.close()
        await ctx.send("Am populat baza de date")
    else:
        await ctx.send(":stuck_out_tongue: Nu ai voie sa folosesti comanda! :stuck_out_tongue:")


@VideoPoliceBot.command()
async def topemoji(ctx, user: str, number: int):
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
async def missing_parameters(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        comand = ctx.message.content
        comand = comand.replace("!topemoji", "")
        if comand == "":
            await topemoji(ctx, ctx.author.name, 5)
        else:
            number = ""
            for char in comand:
                if char.isdigit():
                    number += char
            if number == "":
                comand = comand.replace(" ", "")
                if comand == "":
                    await topemoji(ctx, ctx.author.name, 5)
                else:
                    await topemoji(ctx, comand, 5)
            else:
                comand = comand.replace(number, "")
                comand = comand.replace(" ", "")
                await topemoji(ctx, ctx.author.name, int(number))


@VideoPoliceBot.command()
async def surveillance(ctx, trigger: str):
    global trigger_instanta

    if trigger == 'on':
        if trigger_instanta == 1:
            await ctx.send(":cop: Politia e deja aici! :cop:")
        else:
            await ctx.send(":police_officer: A venit Politia! :police_officer:")
            trigger_instanta = 1
            # logging.info(ctx.author.name + " a chemat politia.")
    else:
        if trigger_instanta == 0:
            await ctx.send(":police_car: Politia a plecat deja! :police_car:")
        else:
            await ctx.send(":police_car: A plecat Politia! :police_car:")
            # logging.info(ctx.author.name + " a izgonit politia.")
            trigger_instanta = 0

    while trigger_instanta:
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
                                    # logging.info("I-am dat kick lui ", member.name)
                                except Exception:
                                    print("N-am putut sa trimit mesaj lui", member.name)
        print("Monitorizez canale")
        time.sleep(10)


@VideoPoliceBot.command()
async def ciocoflender(ctx, value: str):
    global ciocoflender_trigger
    if value == 'on':
        if ciocoflender_trigger == 1:
            await ctx.send(
                ":face_with_symbols_over_mouth: Deja ma uit dupa ciocoflenderi! :face_with_symbols_over_mouth:")
        else:
            ciocoflender_trigger = 1
            await ctx.send(":eyes: Ma uit dupa ciocoflenderi! :eyes:")
            # logging.info(ctx.author.name + " a pornit ciocoflenderii")
    else:
        if ciocoflender_trigger == 0:
            await ctx.send(":face_with_symbols_over_mouth: Sunt oprit deja! :face_with_symbols_over_mouth:")
        else:
            ciocoflender_trigger = 0
            await ctx.send(":sleeping: Nu ma mai uit dupa ciocoflenderi! :sleeping:")
            # logging.info(ctx.author.name + " a oprit ciocoflenderii")


# Tic Tac Toe
@VideoPoliceBot.command()
async def tictactoe(ctx, p1: discord.Member, p2: discord.Member):
    check = True
    for joc in lista_jocuri:
        if (p1.nick == joc.player1 and p2.nick == joc.player2) or (p2.nick == joc.player1 and p1.nick == joc.player2):
            check = False
    if check:
        role = await ctx.guild.create_role(name="Xsi0")
        overwrites = {ctx.guild.default_role: discord.PermissionOverwrite(view_channel=False),
                      role: discord.PermissionOverwrite(view_channel=True)}
        channel = await ctx.guild.create_text_channel(str(p1.nick) + "-si-" + str(p2.nick), position=5,
                                                      overwrites=overwrites)
        await p1.add_roles(role)
        await p2.add_roles(role)
        lista_jocuri.append(TicTacToeGame.Game(p1.nick, p2.nick, channel, role))
        await channel.send(p1.mention + ' ' + p2.mention)
        await channel.send("Comanda este !place linie coloana")
        for row in lista_jocuri[-1].board:
            message = ""
            for item in row:
                message += " " + item
            await channel.send(message)
        await channel.send("E randul tau, " + lista_jocuri[-1].turn)
    else:
        await ctx.send("Deja exista un joc intre " + p1.nick + " si " + p2.nick)


@VideoPoliceBot.command()
async def place(ctx, coord1: int, coord2: int):
    check = True
    for joc in lista_jocuri:
        if joc.channel.id == ctx.channel.id:
            check = False
            if ctx.author.nick != joc.turn:
                await ctx.send("Nu e randul tau.")
            elif joc.place(coord1, coord2) == 0:
                await ctx.send("Nu poti sa pui acolo!")
            else:
                for row in lista_jocuri[-1].board:
                    message = ""
                    for item in row:
                        message += " " + item
                    await joc.channel.send(message)
                if joc.check_win():
                    await ctx.send(joc.winner + ", ai castigat!\nJucati din nou?")
                else:
                    if joc.check_stalemate():
                        await ctx.send("E egalitate.\nJucati din nou?")
    if check:
        await ctx.send("Nu e niciun joc de X si 0 in canalul asta.")


# Counts the emojis from a regular message(if they are present)
@VideoPoliceBot.event
async def on_message(message):
    global ciocoflender_trigger
    if ciocoflender_trigger == 1:
        if not message.author.bot:
            if random.randint(1, 100) <= 5:
                await message.channel.send(file=discord.File('ciocoflender.jpg'))
                print("L-am facut ciocoflender pe", message.author.name)
    else:
        pass
    mesaj = message.content

    # check if message is tictactoe response
    mesaj2 = mesaj.lower()
    for joc in lista_jocuri:
        if message.channel.id == joc.channel.id and message.author.bot == False:
            if (mesaj2 == "n" or mesaj2 == "nu") and (joc.gameOver == True):
                await joc.channel.delete()
                await joc.role.delete()
                lista_jocuri.remove(joc)
                del joc
            elif mesaj2 == "y" or mesaj2 == "da":
                joc.gameOver = False
                joc.board = [[":white_large_square:", ":white_large_square:", ":white_large_square:"],
                             [":white_large_square:", ":white_large_square:", ":white_large_square:"],
                             [":white_large_square:", ":white_large_square:", ":white_large_square:"]]
                for row in joc.board:
                    message2 = ""
                    for item in row:
                        message2 += " " + item
                    await joc.channel.send(message2)
                await joc.channel.send("E randul tau, " + joc.turn)

    # check for emojis
    if not message.author.bot:
        # count the custom emojis
        while True:
            x = mesaj.find("<")
            y = mesaj.find(">")
            if x == -1:
                break
            else:
                if mesaj[x + 1] != '@' and mesaj[x + 1] != '!':
                    mesaj2 = mesaj[x + 2:mesaj.find(">")]
                    emoji = mesaj2[:mesaj2.find(":")]
                    emoji_id = mesaj2[mesaj2.find(":") + 1:]
                    mesaj = mesaj[y + 1:]
                    conn = sqlite3.connect('emojis.db')
                    curs = conn.cursor()
                    curs.execute("PRAGMA foreign_keys;")
                    test_str = "A"
                    for item in curs.execute("SELECT emoji_name FROM emojis WHERE emoji_name = ?", (emoji,)):
                        test_str = item[0]
                    if test_str == "A":
                        curs.execute("INSERT INTO emojis (id, emoji_name) "
                                     "VALUES (?, ?);", (emoji_id, emoji))
                        curs.execute("INSERT INTO emoji_count (user_id, emoji_id, user_name, emoji_name, counter) "
                                     "VALUES (?, ?, ?, ?, ?);",
                                     (message.author.id, emoji_id, message.author.name, emoji, 1))
                        conn.commit()
                        print("Am adaugat " + emoji + " la baza de date")
                        # logging.info("Am adaugat " + emoji + " la baza de date. Mesajul a fost: " + message.content)
                    else:
                        for item in curs.execute(
                                "SELECT user_id, emoji_name, counter FROM emoji_count WHERE user_id = ? AND "
                                "emoji_name = ?;", (message.author.id, emoji)):
                            curs.execute("UPDATE emoji_count SET counter = ? WHERE user_id = ? "
                                         "AND emoji_name = ?", (item[2] + 1, item[0], item[1]))
                            conn.commit()
                        conn.close()
                else:
                    break

        # count the default emojis
        for char in mesaj:
            if ord(char) >= 8986:
                conn = sqlite3.connect('emojis.db')
                curs = conn.cursor()
                curs.execute("PRAGMA foreign_keys;")
                test_str = "A"
                for item in curs.execute("SELECT id, emoji_name FROM emojis WHERE emoji_name = ?", (char,)):
                    test_str = item[0]

                if test_str == "A":
                    id = numpy.random.randint(low=1000, high=999999999)
                    curs.execute("INSERT INTO emojis (id, emoji_name) "
                                 "VALUES (?, ?);", (id, char))
                    curs.execute("INSERT INTO emoji_count (user_id, emoji_id, user_name, emoji_name, counter) "
                                 "VALUES (?, ?, ?, ?, ?);",
                                 (message.author.id, id, message.author.name, char, 1))
                    conn.commit()
                    print("Am adaugat " + char + " la baza de date")
                    # logging.info("Am adaugat " + char + " la baza de date. Mesajul a fost: " + message.content)
                else:
                    for item in curs.execute("SELECT user_id, emoji_name, counter FROM emoji_count WHERE user_id = ? "
                                             "AND emoji_name = ?;", (message.author.id, char)):
                        curs.execute("UPDATE emoji_count SET counter = ? WHERE user_id = ? "
                                     "AND emoji_name = ?", (item[2] + 1, item[0], item[1]))
                        conn.commit()
                conn.close()
    await VideoPoliceBot.process_commands(message)


# Adjusts emoji counter when a message is deleted
@VideoPoliceBot.event
async def on_message_delete(message):
    mesaj = message.content
    # count the custom emojis
    while True:
        x = mesaj.find(":")
        if x == -1:
            break
        else:
            mesaj = mesaj[:x] + "" + mesaj[x + 1:]
            poz = mesaj.find(":")
            emoji = mesaj[x:poz]
            poz = mesaj.find(":")
            emoji_id = mesaj[poz + 1:poz + 19]
            mesaj = mesaj[:mesaj.find("<")] + "" + mesaj[mesaj.find(">") + 3:]

            conn = sqlite3.connect('emojis.db')
            curs = conn.cursor()
            curs.execute("PRAGMA foreign_keys;")
            for item in curs.execute("SELECT user_id, emoji_name, counter FROM emoji_count WHERE user_id = ? AND "
                                     "emoji_name = ?;", (message.author.id, emoji)):
                curs.execute("UPDATE emoji_count SET counter = ? WHERE user_id = ? "
                             "AND emoji_name = ?", (item[2] - 1, item[0], item[1]))
                conn.commit()
            conn.close()

    # count the default emojis
    for char in mesaj:
        if ord(char) > 1000:
            conn = sqlite3.connect('emojis.db')
            curs = conn.cursor()
            curs.execute("PRAGMA foreign_keys;")

            for item in curs.execute("SELECT user_id, emoji_name, counter FROM emoji_count WHERE user_id = ? AND "
                                     "emoji_name = ?;", (message.author.id, char)):
                curs.execute("UPDATE emoji_count SET counter = ? WHERE user_id = ? "
                             "AND emoji_name = ?", (item[2] - 1, item[0], item[1]))
                conn.commit()
            conn.close()


# Adjusts the emoji counter after a message has been edited
@VideoPoliceBot.event
async def on_message_edit(before, after):
    # Handling the old message:
    mesaj_old = before.content
    # count the custom emojis
    while True:
        x = mesaj_old.find(":")
        if x == -1:
            break
        else:
            mesaj_old = mesaj_old[:x] + "" + mesaj_old[x + 1:]
            poz = mesaj_old.find(":")
            emoji = mesaj_old[x:poz]
            poz = mesaj_old.find(":")
            emoji_id = mesaj_old[poz + 1:poz + 19]
            mesaj_old = mesaj_old[:mesaj_old.find("<")] + "" + mesaj_old[mesaj_old.find(">") + 3:]

            conn = sqlite3.connect('emojis.db')
            curs = conn.cursor()
            curs.execute("PRAGMA foreign_keys;")
            for item in curs.execute("SELECT user_id, emoji_name, counter FROM emoji_count WHERE user_id = ? AND "
                                     "emoji_name = ?;", (before.author.id, emoji)):
                curs.execute("UPDATE emoji_count SET counter = ? WHERE user_id = ? "
                             "AND emoji_name = ?", (item[2] - 1, item[0], item[1]))
                conn.commit()
            conn.close()

    # count the default emojis
    for char in mesaj_old:
        if ord(char) > 1000:
            conn = sqlite3.connect('emojis.db')
            curs = conn.cursor()
            curs.execute("PRAGMA foreign_keys;")

            for item in curs.execute("SELECT user_id, emoji_name, counter FROM emoji_count WHERE user_id = ? AND "
                                     "emoji_name = ?;", (before.author.id, char)):
                curs.execute("UPDATE emoji_count SET counter = ? WHERE user_id = ? "
                             "AND emoji_name = ?", (item[2] - 1, item[0], item[1]))
                conn.commit()
            conn.close()

    # Handling the new message
    mesaj_new = after.content
    # count the custom emojis
    while True:
        x = mesaj_new.find(":")
        if x == -1:
            break
        else:
            mesaj_new = mesaj_new[:x] + "" + mesaj_new[x + 1:]
            poz = mesaj_new.find(":")
            emoji = mesaj_new[x:poz]
            poz = mesaj_new.find(":")
            emoji_id = mesaj_new[poz + 1:poz + 19]
            mesaj_new = mesaj_new[:mesaj_new.find("<")] + "" + mesaj_new[mesaj_new.find(">") + 3:]

            conn = sqlite3.connect('emojis.db')
            curs = conn.cursor()
            curs.execute("PRAGMA foreign_keys;")
            for item in curs.execute("SELECT user_id, emoji_name, counter FROM emoji_count WHERE user_id = ? AND "
                                     "emoji_name = ?;", (after.author.id, emoji)):
                curs.execute("UPDATE emoji_count SET counter = ? WHERE user_id = ? "
                             "AND emoji_name = ?", (item[2] + 1, item[0], item[1]))
                conn.commit()
            conn.close()

    # count the default emojis
    for char in mesaj_new:
        if ord(char) > 1000:
            conn = sqlite3.connect('emojis.db')
            curs = conn.cursor()
            curs.execute("PRAGMA foreign_keys;")

            for item in curs.execute("SELECT user_id, emoji_name, counter FROM emoji_count WHERE user_id = ? AND "
                                     "emoji_name = ?;", (after.author.id, char)):
                curs.execute("UPDATE emoji_count SET counter = ? WHERE user_id = ? "
                             "AND emoji_name = ?", (item[2] + 1, item[0], item[1]))
                conn.commit()
            conn.close()


# Adjusts emoji counter based on the emoji added via a reaction to a message
@VideoPoliceBot.event
async def on_raw_reaction_add(payload):
    conn = sqlite3.connect('emojis.db')
    curs = conn.cursor()
    curs.execute("PRAGMA foreign_keys;")

    if payload.emoji.id is None:
        test_str = "A"
        for item in curs.execute("SELECT id, emoji_name FROM emojis WHERE emoji_name = ?", (payload.emoji.name,)):
            test_str = item[0]

        if test_str == "A":
            id = numpy.random.randint(low=1000, high=999999999)
            curs.execute("INSERT INTO emojis (id, emoji_name) "
                         "VALUES (?, ?);", (id, payload.emoji.name))
            curs.execute("INSERT INTO emoji_count (user_id, emoji_id, user_name, emoji_name, counter) "
                         "VALUES (?, ?, ?, ?, ?);",
                         (payload.user_id, id, payload.member.name, payload.emoji.name, 1))
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


# Adjust the emoji counter after a reaction has been removed
@VideoPoliceBot.event
async def on_raw_reaction_remove(payload):
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


VideoPoliceBot.run(TOKEN)
