import datetime
import discord
from discord.ext import commands
import random as rand
import asyncio

bot_token = 'MTE3NjI5OTEyNzk4Mjc4ODYxOA.GyNyVf.5TMJdZd--lRvZAehGiQzWprM-CSAMm7yv1Irks'
prefixo = '/'

intencoes = discord.Intents.default()
intencoes.message_content = True

bot = commands.Bot(command_prefix=prefixo, intents=intencoes)


@bot.event
async def on_ready():
    print(f'Bot {bot.user.name} está online!')


# Task 1: Comando send
@bot.command(name='send')
async def send(ctx, *, mensagem):
    await ctx.send(mensagem)
    if ctx.author == bot.user:
        return
    await ctx.message.delete()


# Task 2: Comando kick (Oculto)
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


# Task 3: Comando random
frases = [
        "E a Vanessa Lopes?", "E o Santos, hein?", "É o gigante da colina! Não tem jeito",
        "O que ta acontecendo no BBB, rapaziada?"
    ]


@bot.command(name='random')
async def random(ctx):

    random_phrase = rand.choice(frases)
    await ctx.send(random_phrase)
    if ctx.author == bot.user:
        return
    await ctx.message.delete()


# Task 4: Anti-Raid
members_join_time = {}
datetime_now = datetime.datetime.now()
delta_tempo = datetime.timedelta(minutes=50)        # Dentro de X minutos


@bot.event
async def on_member_join(member):

    members_join_time[member.id] = datetime_now

    barreira = int(15)      # Considera Raid à partir de X usuários entrando no servidor
    if len(member.guild.member) > barreira:
        oldest_member_time = min(members_join_time.values())
        date_diff = datetime_now - oldest_member_time

        motivo_ban_de_raid = f"Possível Raid! Anti-Raid Ativado: mais de {barreira} pessoas tentaram entrar  no " \
                             f"servidor em menos de 50 Minutos"

        if date_diff < delta_tempo:
            await member.ban(motivo_ban_de_raid)


@bot.event
async def clear_list_members_join_time():
    while True:
        await asyncio.sleep(3000)       # 50 Minutos

        for member_id, join_time in list(members_join_time.items()):
            if datetime_now - join_time > delta_tempo:
                del members_join_time[member_id]


# Task 5: Comando help
help_list = "/send [Mensagem] - Faz com que o bot envie uma mensagem personalizada" \
            "/random - Envia mensagens aleatórias"


@bot.command(name="help")
async def help_list():
    await send(help_list)

bot.run(bot_token)
