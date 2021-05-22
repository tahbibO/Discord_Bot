# bot.py
import os
import discord
from discord import embeds
from discord.gateway import DiscordClientWebSocketResponse
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
#chrome_options.headless = True
chrome_options.add_argument('--disable-blink-features=AutomationControlled')



load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')


bot = commands.Bot(command_prefix='$',help_command=None)


products = []

class Product:
    def __init__(self, link, author,channel):
        self.link = link
        self.author = author
        self.channel = channel


browser = webdriver.Chrome(options=chrome_options)


@bot.event
async def on_ready():
    print(f'{bot.user.name} is running')
    trackProduct.start()

@bot.command(name = 'check', help="checks if product from bestbuy is available and returns check out link otherwise returns not available")
async def check(ctx, link):
    print("calling check")
    browser.delete_all_cookies()
    browser.get(link)
    elem = browser.find_element_by_class_name('container_3LC03')
    
    #getting data for embed
    productName = browser.find_element_by_xpath('/html/body/div[1]/div/div[4]/div[1]/h1').text
    image = browser.find_element_by_xpath('//*[@id="root"]/div/div[4]/div[1]/div[2]/div[1]/div[1]/div/div[1]/div/div/div[1]/div/div/div/div/div/img').get_attribute('src')
    price = browser.find_element_by_class_name('large_3aP7Z').text
    description = browser.find_element_by_class_name('description_2Qiri').get_attribute('innerHTML')
    
    #creating embed
    response = discord.Embed()
    response.title = productName
    response.url = link
    response.add_field(name="Price: ", value=price, inline=True)
    response.add_field(name="Status: ",value=elem.text,inline=True)
    response.set_image(url=image)
    response.description = description



    if elem.text == "Available to ship":
        response.color = discord.Color.from_rgb(158, 206, 154)
        await ctx.send(content=ctx.author.mention+" "+f"**{'Available to ship'}**",embed=response)
    else:
        response.color = discord.Color.from_rgb(178, 13, 48)
        await ctx.send(content=ctx.author.mention+" "+f"**{'Not available to ship'}**",embed=response)
    
    await asyncio.sleep(0.01)
    print("check called")


@bot.event
async def on_command_error(ctx,error):
    response = discord.Embed()
    response.title = "Error"
    response.description = "Command not entered properly. Type `$help` to show a list of all commands and how to use them"
    response.color = discord.Color.from_rgb(178, 13, 48)
    await ctx.send(embed=response)
    await asyncio.sleep(0.01)



@bot.command(name = 'track', help= "track a given product and notify user when available to ship")
async def track(ctx,link):
    print("calling track")
    if link !="" and link.find("https://www.bestbuy.ca/en-ca/product/") != -1:
        p = Product(link,ctx.author,ctx.channel.id)
        products.append(p)
        await ctx.send('tracking product')
    else:
        response = discord.Embed()
        response.title = "Error"
        response.description = "Command not entered properly. Type `$help` to show a list of all commands and how to use them"
        response.color = discord.Color.from_rgb(178, 13, 48)
        await ctx.send(embed=response)
        await asyncio.sleep(0.01)
    print("track called")
    
@bot.command(name = 'help')
async def help(ctx):
    print("calling help")
    response = discord.Embed()
    response.title = "Commands"
    response.add_field(name="$track (link) :",value="Track a product from a given BestBuy link and notify user when products available to ship", inline=False)
    response.add_field(name="$check (link) :",value="Checks if a product from a given BestBuy link is available.", inline=False)
    response.add_field(name="$help :",value="Show description of all commands.", inline=False)

    response.color = discord.Color.from_rgb(158, 206, 154)
    
    await ctx.send(embed=response)
    print("help called")


@tasks.loop(seconds=10)
async def trackProduct():
    print("updating tracking List")
    browser.delete_all_cookies()
    for p in products:
        browser.get(p.link)
        elem = browser.find_element_by_class_name('container_3LC03')

        #getting data for embed
        productName = browser.find_element_by_xpath('/html/body/div[1]/div/div[4]/div[1]/h1').text
        image = browser.find_element_by_xpath('//*[@id="root"]/div/div[4]/div[1]/div[2]/div[1]/div[1]/div/div[1]/div/div/div[1]/div/div/div/div/div/img').get_attribute('src')
        price = browser.find_element_by_class_name('large_3aP7Z').text
        description = browser.find_element_by_class_name('description_2Qiri').get_attribute('innerHTML')
        
        #creating embed
        response = discord.Embed()
        response.title = productName
        response.url = p.link
        response.add_field(name="Price: ", value=price, inline=True)
        response.add_field(name="Status: ",value=elem.text,inline=True)
        response.set_image(url=image)
        response.description = description
        response.color = discord.Color.from_rgb(158, 206, 154)

        if elem.text == "Available to ship":
            await bot.get_channel(p.channel).send(content=p.author.mention+f'**{"Available to ship"}**',embed=response)
            products.remove(p)
        await asyncio.sleep(0.01)
    print("finished updating tracking list")
    pass



bot.run(TOKEN)
