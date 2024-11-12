import discord
from discord.ext import commands
from main import gen_pass
import random
import os
import requests
from load_model import get_class

# Membaca token dari file token.txt
with open("token.txt", "r") as f:
    token = f.read()

sampah = {
    'kertas' : 'anorganik',
    'plastik' : 'anorganik',
    'kardus' : 'anorganik',
    'sisa_makanan': 'organik',
    'daun_kering' : 'organik',
    'kulit_buah' : 'organik',
    'baterai' : 'B3',
    'oli' : 'B3',
    'deterjen' : 'B3'
} 

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='$', intents=intents)

@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')

@bot.command()
async def hello(ctx):
    await ctx.send(f'Hi! I am a bot {bot.user}!')

@bot.command()
async def repeat(ctx, times: 3, content='repeating...'):
    """Repeats a message multiple times."""
    for i in range(times):
        await ctx.send(content)

@bot.command()
async def heh(ctx, count_heh = 5):
    await ctx.send("he" * count_heh)

@bot.command()
async def passw(ctx, panjang = 5):
    await ctx.send(gen_pass(panjang))

@bot.command()
async def mem(ctx):
    img_name = random.choice(os.listdir('images'))
    with open(f'images/{img_name}', 'rb') as f:
        picture = discord.File(f)
    await ctx.send(file=picture)

animal = {
    'animal1.jpg': 5, #common
    'animal2.jpg': 2, #uncommon
    'animal3.jpg': 1  #rare
}

def get_weighted_random_meme(animal):
    weighted_memes = []
    for animal, rarity in animal.items():
        weighted_memes.extend([animal] * rarity)
    return random.choice(weighted_memes)

@bot.command()
async def anim(ctx):
    anim_name = get_weighted_random_meme(animal)
    with open(f'animals/{anim_name}', 'rb') as f:
        picture = discord.File(f)
    await ctx.send(file=picture)

@bot.command()
async def check(ctx):
    if ctx.message.attachments:
        for attachment in ctx.message.attachments:
            file_name = attachment.filename
            file_url = attachment.url
            # save gambarnya
            await attachment.save(f"./{attachment.filename}")
            # await ctx.send(f"Menyimpan gambar ke ./{attachment.filename}")

            # proses gambar ke model
            class_name, confidence_score = get_class("converted_keras/keras_model.h5", "converted_keras/labels.txt", file_name)
            info = f"Gambar ini adalah: {class_name} \nDengan tingkat kepercayaan: {confidence_score}"

            if confidence_score < 0.5:
                info = f"maaf model tidak bisa mengenali objek"

            # tampilkan ke bot discord
            await ctx.send(info)
            # await ctx.send("dengan tingkat kepercayaan:", confidence_score)

    else:
        await ctx.send("Anda lupa mengunggah gambar :(")
    
def get_duck_image_url():    
    url = 'https://random-d.uk/api/random'
    res = requests.get(url)
    data = res.json()
    return data['url']

@bot.command('duck')
async def duck(ctx):
    '''Setelah kita memanggil perintah bebek (duck), program akan memanggil fungsi get_duck_image_url'''
    image_url = get_duck_image_url()
    await ctx.send(image_url)

@bot.command("sampah")
async def jenis_sampah(ctx, item:str):
    if item.lower() in sampah:
        await ctx.send(f"{item.capitalize()} merupakan jenis sampah: {sampah[item.lower()]}")
    else:
        await ctx.send(f"Maaf, {item.capitalize()} tidak tercatat di dalam daftar")

@bot.command()
async def organik(ctx):
    await ctx.send(f'Sampah jenis organik dapat diolah menjadi pupuk kompos, makanan hewan, eco enzyme, dan biogas')

@bot.command()
async def anorganik(ctx):
    await ctx.send(f'Sampah jenis anorganik dapat diolah menjadi kerajinan tangan, bahan daur ulang, eco brick')

@bot.command()
async def B3(ctx):
    await ctx.send(f'Sampah jenis B3 dapat diolah dengan melakukan pemilahan, membuangnya ke pembuangan khusus')

bot.run(token)