# bot.py
import os
from dotenv import load_dotenv
from selenium import webdriver
from discord.ext import commands
import time
import asyncio
from discord.ext import tasks



# Stay Logged In
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("user-data-dir=/tmp/tarun")

# Tell Chrome that you are not a robot
chrome_options.add_experimental_option("excludeSwitches", ['enable-automation'])
chrome_options.add_experimental_option('useAutomationExtension', False)
chrome_options.headless = True
chrome_options.add_argument('--disable-blink-features=AutomationControlled')



load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')


bot = commands.Bot(command_prefix='$')


products = []

@bot.event
async def on_ready():
    print(f'{bot.user.name} is running')
    browser = webdriver.Chrome(options=chrome_options)
    trackProduct.start()

@bot.command(name = 'check', help="checks if product from bestbuy is available and returns check out link otherwise returns not available")
async def check(ctx, link):
    browser.get(link)
    elem = browser.find_element_by_class_name('container_3LC03')
    print(elem.text)
    if elem.text == "Available to ship":
        await ctx.send('Avaiable to ship')
    else:
        await ctx.send("Not available to ship")
    await asyncio.sleep(0.01)
    

@bot.command(name = 'track', help= "track a given product and notify user when available to ship")
async def track(ctx,link):
    #products.append(link)
    print(ctx.channel.id)
    await ctx.send('tracking product')
    
    
@tasks.loop(seconds=5)
async def trackProduct():
    for p in products:
        browser.get(p)
        elem = browser.find_element_by_class_name('container_3LC03')
        if elem.text == "Available to ship":
            await bot.get_channel(745755478986063893).send(f'Available to ship\n{p}')
            products.remove(p)
        await asyncio.sleep(0.01)
        pass



bot.run(TOKEN)
