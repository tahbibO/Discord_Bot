# bot.py
import os
import discord
from discord import channel
from discord.state import ConnectionState
from dotenv import load_dotenv
from os import name
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from discord.ext import commands
import time


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




@bot.command(name = 'check', help="checks if product from bestbuy is available and returns check out link otherwise returns not available")
async def check(ctx, link):
    browser = webdriver.Chrome(options=chrome_options)
    browser.get(link)
    elem = browser.find_element_by_class_name('container_3LC03')
    print(elem.text)
    if elem.text == "Available to ship":
        await ctx.send('Avaiable to ship')
    else:
        await ctx.send("Not available to ship")

@bot.command(name = 'track', help= "track a given product and notify user when available to ship")
async def track(ctx,link):
    browser = webdriver.Chrome(options=chrome_options)
    browser.get(link)
    while True:
        elem = browser.find_element_by_class_name('container_3LC03')
        if elem.text == "Available to ship":
            await ctx.send('Available to ship')
            break
        else:
            time.sleep(15)
            browser.refresh()


bot.run(TOKEN)
