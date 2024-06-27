import discord
from discord.ext import commands
import random

description = "Este es un programa donde vinculamos a Discord con VS Code para lanzar imagenes"

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix="$", description=description, intents=intents)

# Carga de imágenes
welcome_img = "Frases-sobre-el-dia-del-medio-ambiente-Los-Informativos.jpg" 
child_img = "que_es_el_medio_ambiente_para_ninos_1674_1_600.jpg"  
teen_adult_img = "c7f43c77ee9b8bd4e3efb632da14673d.jpg" 

# Variables para almacenar información temporal del usuario
user_data = {}

@bot.event
async def on_ready():
    print(f"Logueado como {bot.user} (ID: {bot.user.id})")

@bot.command()
async def hola(ctx):
    member = ctx.author
    channel = ctx.channel
    await channel.send(f"¡Bienvenido/a {member.mention}! Aquí te enseñaremos sobre la importancia del cuidado del medio ambiente.")
    await channel.send(file=discord.File(welcome_img))
    await channel.send("¿Cuál es tu nombre?")
    user_data[member.id] = {'step': 'name'}

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if message.author.id in user_data:
        if user_data[message.author.id]['step'] == 'name':
            user_data[message.author.id]['name'] = message.content
            await message.channel.send(f"¿Qué edad tienes, {message.content}?")
            user_data[message.author.id]['step'] = 'age'
        elif user_data[message.author.id]['step'] == 'age':
            try:
                age = int(message.content)
                name = user_data[message.author.id]['name']
                if 1 <= age <= 12:
                    await message.channel.send(f"{name}, tienes {age} años. Aquí tienes una imagen informativa:")
                    await message.channel.send(file=discord.File(child_img))
                else:
                    await message.channel.send(f"{name}, tienes {age} años. Aquí tienes una imagen informativa:")
                    await message.channel.send(file=discord.File(teen_adult_img))
                del user_data[message.author.id]
            except ValueError:
                await message.channel.send("Por favor, introduce una edad válida.")
    await bot.process_commands(message)

bot.run("Token")
