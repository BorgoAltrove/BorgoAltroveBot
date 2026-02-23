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
            

            # Data finale = oggi
            today_date_raw = datetime.date.today()
            today_date = datetime.datetime.combine(
                today_date_raw,
                datetime.time.min,
                tzinfo=datetime.timezone.utc
            )



            # Data iniziale presa dal comando
            start_date_raw = datetime.date.fromisoformat(data)
            start_date = datetime.datetime.combine(
                start_date_raw,
                datetime.time.min,
                tzinfo=datetime.timezone.utc
            )
            start_date = start_date - timedelta(days=1)  # Per includere il giorno stesso

            categories = [1197337817924247644]
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
                        
            await ctx.channel.send(
                f"Le settimane in cui l'utente ha scritto almeno 3 messaggi sono: {count_settimane}"
            )