import discord
from discord.ext import commands
from classifier import get_class

# Configuração das permissões (intents) do Bot
intents = discord.Intents.default()
intents.message_content = True  # Necessário para ler o conteúdo e anexos das mensagens

bot = commands.Bot(command_prefix='$', intents='intents')

@bot.event
async def on_ready():
    print(f'Bot conectado com sucesso como {bot.user}')

@bot.command()
async def check(ctx):
    if ctx.message.attachments:
        for attachment in ctx.message.attachments:
            file_name = attachment.filename
            file_url = attachment.url
            await attachment.save(f"./{attachment.filename}")
            await ctx.send(get_class(model_path="./keras_model.h5", labels_path="labels.txt", image_path=f"./{attachment.filename}"))
    else:
        await ctx.send("Você esqueceu de enviar a imagem :(")

bot.run('TOKEN')
