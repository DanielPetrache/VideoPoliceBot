import discord
from discord.ext import commands
import random
import sqlite3
import numpy
from Emojis import Emojis_class
from TicTacToe import TicTacToe_class
# import logging


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

extentions = ['TicTacToe', 'Emojis', 'Surveillance']
for item in extentions:
    VideoPoliceBot.load_extension(item)

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
    await TicTacToe_class.check_tictactoe_response(mesaj.lower(), message, VideoPoliceBot)

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
                    for x in curs.execute("SELECT emoji_name FROM emojis WHERE emoji_name = ?", (emoji,)):
                        test_str = x[0]
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
                        for y in curs.execute(
                                "SELECT user_id, emoji_name, counter FROM emoji_count WHERE user_id = ? AND "
                                "emoji_name = ?;", (message.author.id, emoji)):
                            curs.execute("UPDATE emoji_count SET counter = ? WHERE user_id = ? "
                                         "AND emoji_name = ?", (y[2] + 1, y[0], y[1]))
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
            # emoji_id = mesaj_old[poz + 1:poz + 19]
            mesaj_old = mesaj_old[:mesaj_old.find("<")] + "" + mesaj_old[mesaj_old.find(">") + 3:]

            conn = sqlite3.connect('emojis.db')
            curs = conn.cursor()
            curs.execute("PRAGMA foreign_keys;")
            for x in curs.execute("SELECT user_id, emoji_name, counter FROM emoji_count WHERE user_id = ? AND "
                                  "emoji_name = ?;", (before.author.id, emoji)):
                curs.execute("UPDATE emoji_count SET counter = ? WHERE user_id = ? "
                             "AND emoji_name = ?", (x[2] - 1, x[0], x[1]))
                conn.commit()
            conn.close()

    # count the default emojis
    for char in mesaj_old:
        if ord(char) > 1000:
            conn = sqlite3.connect('emojis.db')
            curs = conn.cursor()
            curs.execute("PRAGMA foreign_keys;")

            for y in curs.execute("SELECT user_id, emoji_name, counter FROM emoji_count WHERE user_id = ? AND "
                                  "emoji_name = ?;", (before.author.id, char)):
                curs.execute("UPDATE emoji_count SET counter = ? WHERE user_id = ? "
                             "AND emoji_name = ?", (y[2] - 1, y[0], y[1]))
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
            for x in curs.execute("SELECT user_id, emoji_name, counter FROM emoji_count WHERE user_id = ? AND "
                                  "emoji_name = ?;", (after.author.id, emoji)):
                curs.execute("UPDATE emoji_count SET counter = ? WHERE user_id = ? "
                             "AND emoji_name = ?", (x[2] + 1, x[0], x[1]))
                conn.commit()
            conn.close()

    # count the default emojis
    for char in mesaj_new:
        if ord(char) > 1000:
            conn = sqlite3.connect('emojis.db')
            curs = conn.cursor()
            curs.execute("PRAGMA foreign_keys;")

            for x in curs.execute("SELECT user_id, emoji_name, counter FROM emoji_count WHERE user_id = ? AND "
                                  "emoji_name = ?;", (after.author.id, char)):
                curs.execute("UPDATE emoji_count SET counter = ? WHERE user_id = ? "
                             "AND emoji_name = ?", (x[2] + 1, x[0], x[1]))
                conn.commit()
            conn.close()


# Adjusts emoji counter based on the emoji added via a reaction to a message
@VideoPoliceBot.event
async def on_raw_reaction_add(payload):
    await Emojis_class.handle_reaction_add(payload)


# Adjust the emoji counter after a reaction has been removed
@VideoPoliceBot.event
async def on_raw_reaction_remove(payload):
    await Emojis_class.handle_reaction_edit(payload)


VideoPoliceBot.run(TOKEN, bot=True, reconnect=True)
