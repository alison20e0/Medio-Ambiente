import discord
from discord.ext import commands
import random
import os

description = "Este es un programa donde vinculamos a Discord con VS Code para lanzar imagenes"

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix="$", description=description, intents=intents)

# Carga de imágenes
welcome_img = "Frases-sobre-el-dia-del-medio-ambiente-Los-Informativos.jpg" 
child_img = "que_es_el_medio_ambiente_para_ninos_1674_1_600.jpg"  
teen_adult_img = "c7f43c77ee9b8bd4e3efb632da14673d.jpg" 
child_more_info_img = "images_ni/df525f340b225faa15a0fb08a3437e9c.jpg" 
teen_adult_more_info_img = "images_ad/83db628286b8d696fee5baaf30cfb863.jpg"

# Carpeta de memes o datos informativos
memes_folder = "memes"

# Variables para almacenar información temporal del usuario
user_data = {}

@bot.event
async def on_ready():
    print(f"Logueado como {bot.user} (ID: {bot.user.id})")

@bot.command()
async def hola(ctx):
    member = ctx.author
    channel = ctx.channel
    await channel.send(f"¡Bienvenido/a! Aquí te enseñaremos sobre la importancia del cuidado del medio ambiente.")
    await channel.send(file=discord.File(welcome_img))
    await channel.send("¿Cuál es tu nombre?")
    user_data[member.id] = {'step': 'name'}

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if message.author.id in user_data:
        step = user_data[message.author.id]['step']
        if step == 'name':
            user_data[message.author.id]['name'] = message.content
            await message.channel.send(f"¿Qué edad tienes, {message.content}?")
            user_data[message.author.id]['step'] = 'age'
        elif step == 'age':
            try:
                age = int(message.content)
                name = user_data[message.author.id]['name']
                user_data[message.author.id]['age'] = age
                if 1 <= age <= 12:
                    await message.channel.send(f"{name}, tienes {age} años. Aquí tienes una imagen informativa:")
                    await message.channel.send(file=discord.File(child_img))
                else:
                    await message.channel.send(f"{name}, tienes {age} años. Aquí tienes una imagen informativa:")
                    await message.channel.send(file=discord.File(teen_adult_img))
                await message.channel.send("Es importante saber cuidar a nuestro planeta Tierra, ¿quisieras conocer cómo? (responde con 'si' o 'no')")
                user_data[message.author.id]['step'] = 'more_info'
            except ValueError:
                await message.channel.send("Por favor, introduce una edad válida.")
        elif step == 'more_info':
            if message.content.lower() == 'si':
                age = user_data[message.author.id]['age']
                if 1 <= age <= 12:
                    await message.channel.send("¡Genial! Aquí tienes más información sobre cómo cuidar el planeta:")
                    await message.channel.send(file=discord.File(child_more_info_img))
                else:
                    await message.channel.send("¡Genial! Aquí tienes más información sobre cómo cuidar el planeta:")
                    await message.channel.send(file=discord.File(teen_adult_more_info_img))
                await message.channel.send("¿Te gustaría aprender más datos con respecto a nuestro planeta? (responde con 'si' o 'no')")
                user_data[message.author.id]['step'] = 'more_facts'
            elif message.content.lower() == 'no':
                await message.channel.send("Listo, estaré aquí para cuando lo quieras saber.")
                del user_data[message.author.id]
            else:
                await message.channel.send("Por favor, responde con 'si' o 'no'.")
        elif step == 'more_facts':
            if message.content.lower() == 'si':
                meme_files = os.listdir(memes_folder)
                random_meme = random.choice(meme_files)
                await message.channel.send(file=discord.File(os.path.join(memes_folder, random_meme)))
                await message.channel.send("¿Quieres saber más? (responde con 'si' o 'no')")
            elif message.content.lower() == 'no':
                await message.channel.send("Entendido.")
                del user_data[message.author.id]
            else:
                await message.channel.send("Por favor, responde con 'si' o 'no'.")
    await bot.process_commands(message)

bot.run("Token")
