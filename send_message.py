import discord
from discord.ext import commands

bot_token = 'MTE3NjI5OTEyNzk4Mjc4ODYxOA.GyNyVf.5TMJdZd--lRvZAehGiQzWprM-CSAMm7yv1Irks'
prefixo = '/'

intencoes = discord.Intents.default()
intencoes.message_content = True

bot = commands.Bot(command_prefix=prefixo, intents=intencoes)


@bot.event
async def on_ready():
    print(f'Bot {bot.user.name} está online!')


@bot.command(name='send')
async def enviar_mensagem(ctx, *, mensagem):
    await ctx.send(mensagem)


@bot.command(name='kick')
@commands.has_permissions(administrator=True)
async def kick(ctx, member: discord.Member, *, reason=None):
    motivo = 'Desrespeitou alguma das regras do servidor.'
    await member.kick(reason=motivo)
    await ctx.send(f'{member.mention} foi kickado do servidor por @We Mess Clan. Motivo: {reason}')


@kick.error
async def kick_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("Você não tem permissão para usar este comando.")

bot.run(bot_token)
