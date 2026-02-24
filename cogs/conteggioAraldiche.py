import discord
from discord import app_commands
from discord.ext import commands, tasks
import asyncio
import datetime
from datetime import timedelta
from collections import defaultdict
from Araldica import Araldica

class ConteggioAraldiche(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="araldica", description="Calcola l'araldica di un utente")
    async def araldica(self, ctx: discord.Interaction, user: discord.Member, data: str, settimane_precedenti: int):
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

            # Lista delle categorie da considerare (solo ingame)
            categories = [932644393578557560, 932645350706143292, 932648960424824962, 932646119392034916, 932649755484491836, 932651979572916304, 1096496538240434196, 1096496263819694211, 1096494403058667621, 1159167397584969889, 1096497043679223818, 1216043165744762924, 1293136475357184041, 1362788676249063545, 1098509198855258133]
            count_settimane = settimane_precedenti
            guild = ctx.guild

            end_date = start_date + timedelta(days=7)

            while(end_date.date() <= today_date.date()):

                count_messaggi = 0
                print(end_date.date())

                for channel in guild.text_channels:  # tutti i canali di testo del server
                    if channel.category and channel.category.id in categories:
                        # Controlla i messaggi in questo canale tra start_date e end_date
                        async for message in channel.history(
                                after=start_date,
                                before=end_date+timedelta(days=1),
                                oldest_first=True
                            ):
                                # Se il messaggio è dell'utente specificato, incrementa il contatore
                                if message.author.id == user.id:
                                    count_messaggi +=1
                                    if count_messaggi >= 3:
                                        count_settimane += 1
                                        break
                        if count_messaggi >= 3:
                            break
                start_date = end_date
                # Per controllare anche l'ultima settimana se è meno di 7 giorni
                if end_date + timedelta(days=7) > today_date and end_date.date() != today_date.date():
                    end_date = today_date
                else:
                    end_date = end_date + timedelta(days=7)
            
            if(count_settimane >= 102):
                araldica = Araldica.ARCONTE_ARCONTESSA
            elif(count_settimane >= 52):
                araldica = Araldica.SAVIO_A
            elif(count_settimane >= 28):
                araldica = Araldica.LORD_LADY
            elif(count_settimane >= 14):
                araldica = Araldica.SIR_MISS
            elif(count_settimane >= 6):
                araldica = Araldica.MESSERE_DAMA
            elif(count_settimane >= 2):
                araldica = Araldica.CITTADINO_A
            else:
                araldica = "Nessuna araldica"

            await ctx.followup.send(
                f"Le settimane in cui {user.nick} ha scritto almeno 3 messaggi sono: {count_settimane}, quindi l'araldica è: {araldica.name if isinstance(araldica, Araldica) else araldica}"
            )
        except Exception as e:
            await ctx.followup.send(f"❌ Errore: {str(e)}")
            print(f"Errore araldica: {e}")

async def setup(bot):
    await bot.add_cog(ConteggioAraldiche(bot))