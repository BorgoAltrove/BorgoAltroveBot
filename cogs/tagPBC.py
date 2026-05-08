import discord
from discord import app_commands
from discord.ext import commands

class TagPBC(commands.Cog):

    last_tag_time = None

    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="pbc", description="Tagga tutti i membri che hanno il ruolo PBC")
    async def tag_pbc(self, ctx: discord.Interaction):
        
        # Controlla se è passato almeno 1 minuto dall'ultimo tag
        if self.last_tag_time and (discord.utils.utcnow() - self.last_tag_time).total_seconds() < 60:
            await ctx.response.send_message("⏳ Puoi usare questo comando solo una volta al minuto. Riprova tra qualche secondo!", ephemeral=True)
            return
        
        # Controlla che il comando sia stato usato nei canali di testo prefissati, manda un messaggio effimero se non è così
        # Canali di testo permessi: taverna, piazza, bot master
        allowed_channel_ids = [932644535132102696, 932644501888065557, 858785785104695297]
        if ctx.channel_id not in allowed_channel_ids:
            await ctx.response.send_message("❌ Questo comando può essere usato solo nei canali di testo specifici!", ephemeral=True)
            return
    
        # Aggiorna il tempo dell'ultimo tag
        self.last_tag_time = discord.utils.utcnow()

        # Manda un messaggio taggando tutti i membri con il ruolo PBC
        role = discord.utils.get(ctx.guild.roles, name="provaZaiross")
        if role:
            await ctx.response.send_message(f"{ctx.user.mention} si guarda attorno alla ricerca di qualcuno con cui fare qualche chiacchiera {role.mention}!", 
                                            allowed_mentions=discord.AllowedMentions(roles=True))
        else:
            await ctx.response.send_message("Il ruolo PBC non esiste nel server!", ephemeral=True)

async def setup(bot):
    await bot.add_cog(TagPBC(bot))
    