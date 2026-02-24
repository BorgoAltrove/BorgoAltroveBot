import discord
from discord import app_commands
from discord.ext import commands, tasks
import asyncio
import datetime
from datetime import timedelta
from collections import defaultdict


class araldiche(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="araldica", description="Calcola l'araldica di un utente")
    async def araldica(self, ctx: discord.Interaction, user: discord.Member, data: str):
        await ctx.response.defer()
        
        try:
            # Data finale = oggi
            today_date_raw = datetime.date.today()
            today_date = datetime.datetime.combine(
                today_date_raw,
                datetime.time.min,
                tzinfo=datetime.timezone.utc
            )



            # Data iniziale presa dal comando
            try:
                start_date_raw = datetime.date.fromisoformat(data)
            except ValueError:
                await ctx.followup.send(f"Errore nella data, il formato corretto è: YYYY-MM-DD")
                return

            start_date = datetime.datetime.combine(
                start_date_raw,
                datetime.time.min,
                tzinfo=datetime.timezone.utc
            )
            start_date = start_date - timedelta(days=1)  # Per includere il giorno stesso

            categories = [932644393578557560, 932645350706143292, 932648960424824962, 932646119392034916, 932649755484491836, 932651979572916304, 1096496538240434196, 1096496263819694211, 1096494403058667621, 1159167397584969889, 1096497043679223818, 1216043165744762924, 1293136475357184041, 1362788676249063545, 1098509198855258133]
            count_settimane = 0
            guild = ctx.guild

            end_date = start_date + timedelta(days=7)

            while(end_date.date() <= today_date.date()):

                count_messaggi = 0
                print(end_date.date())

                for channel in guild.text_channels:  # tutti i canali di testo del server
                    if channel.category and channel.category.id in categories:
                        async for message in channel.history(
                                after=start_date,
                                before=end_date+timedelta(days=1),
                                oldest_first=True
                            ):
                                if message.author.id == user.id:
                                    count_messaggi +=1
                                    if count_messaggi >= 3:
                                        count_settimane += 1
                                        break
                        if count_messaggi >= 3:
                            break
                start_date = end_date
                if end_date + timedelta(days=7) > today_date and end_date.date() != today_date.date():
                    end_date = today_date
                else:
                    end_date = end_date + timedelta(days=7)
                        
            await ctx.followup.send(
                f"Le settimane in cui {user} ha scritto almeno 3 messaggi sono: {count_settimane}"
            )
        except Exception as e:
            await ctx.followup.send(f"❌ Errore: {str(e)}")
            print(f"Errore araldica: {e}")

async def setup(bot):
    await bot.add_cog(araldiche(bot))