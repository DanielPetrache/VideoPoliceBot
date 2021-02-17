import discord
from discord.ext import commands
import TicTacToeGame


class TicTacToe(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.game_map = {}

    @commands.command()
    async def tictactoe(self, ctx, p1: discord.Member, p2: discord.Member):
        check = True
        for value in self.game_map.values():
            if (p1.nick == value.player1 and p2.nick == value.player2) or (
                    p2.nick == value.player1 and p1.nick == value.player2):
                check = False
        if check:
            role = await ctx.guild.create_role(name="Xsi0")
            overwrites = {ctx.guild.default_role: discord.PermissionOverwrite(view_channel=False),
                          role: discord.PermissionOverwrite(view_channel=True)}
            channel = await ctx.guild.create_text_channel(str(p1.nick) + "-si-" + str(p2.nick), position=5,
                                                          overwrites=overwrites)
            await p1.add_roles(role)
            await p2.add_roles(role)

            self.game_map[channel.id] = TicTacToeGame.Game(p1.nick, p2.nick, role)

            await channel.send(p1.mention + ' ' + p2.mention)
            await channel.send("Comanda este !place linie coloana")
            for row in self.game_map[channel.id].board:
                message = ""
                for item in row:
                    message += " " + item
                await channel.send(message)
            await channel.send("E randul tau, " + self.game_map[channel.id].turn)
        else:
            await ctx.send("Deja exista un joc intre " + p1.nick + " si " + p2.nick)

    @commands.command()
    async def place(self, ctx, coord1: int, coord2: int):
        check = True
        for key, value in self.game_map.items():
            if key == ctx.channel.id:
                check = False
                if ctx.author.nick != value.turn:
                    await ctx.send("Nu e randul tau.")
                elif value.place(coord1, coord2) == 0:
                    await ctx.send("Nu poti sa pui acolo!")
                else:
                    for row in value.board:
                        message = ""
                        for item in row:
                            message += " " + item
                        await ctx.channel.send(message)
                    if value.check_win():
                        await ctx.send(value.winner + ", ai castigat!\nJucati din nou?")
                    else:
                        if value.check_stalemate():
                            await ctx.send("E egalitate.\nJucati din nou?")
                        else:
                            await ctx.send("E randul tau, " + value.turn)
        if check:
            await ctx.send("Nu e niciun joc de X si 0 in canalul asta.")


def setup(bot):
    bot.add_cog(TicTacToe(bot))
