import asyncio
import os
import time
import discord
from helpers.config import Config
from discord.ext import commands
from database.users import Users
from database.cars import Cars
from database.garages import Garages

users = Users()
cars = Cars()
garages = Garages()
config = Config()
intents = discord.Intents.default()
intents.message_content = True
intents.members = True
bot = commands.Bot(intents=intents)
embed_color = config.get_embed_color()
attachment_head = config.get_attachment_head()
makes = asyncio.run(cars.get_makes())

async def list_makes():
    return makes

async def list_models(ctx: discord.AutocompleteContext.options):
    return await cars.get_models(ctx.options['make'])

async def list_trims(ctx: discord.AutocompleteContext.options):
    return await cars.get_trims(ctx.options['make'], ctx.options['model'])

async def list_years(ctx: discord.AutocompleteContext.options):
    return await cars.get_years(ctx.options['make'], ctx.options['model'], ctx.options['trim'])

@bot.event
async def on_ready():
    print(f'Successfully logged in as {bot.user}')

@bot.slash_command()
async def ignite(ctx):
    user_id = ctx.author.id
    user_name = ctx.author.name
    embed = discord.Embed(color=embed_color)
    if not await users.contains(user_id):
        await users.add_user(user_id, user_name)
        embed.title = 'Welcome to Artura!'
        embed.set_thumbnail(url=ctx.author.avatar.url)
        embed.set_image(url=attachment_head + '1303478655766495272/MTC.png')
        embed.description = f"You have now ignited your engine {ctx.author.mention}\nEnjoy your adventure!"
        await ctx.respond(embed=embed)
    else:
        embed.title = f'Welcome {user_name}!'
        embed.set_thumbnail(url=ctx.author.avatar.url)
        embed.description = f"Your engine is already ignited!"
        await ctx.respond(embed=embed)

@bot.slash_command()
async def purchase(ctx: discord.ApplicationContext,
                   make: discord.Option(str, "Select a make", autocomplete=list_makes, required=True),
                   model: discord.Option(str, "Select a model", autocomplete=list_models, required=True),
                   trim: discord.Option(str, "Select a trim", autocomplete=list_trims, required=False),
                   year: discord.Option(str, "Select a year", autocomplete=list_years, required=False)):
    return

@bot.slash_command(description='View the specifications of a car')
async def specs(ctx: discord.ApplicationContext,
                make: discord.Option(str, "Select a make", autocomplete=list_makes, required=True),
                model: discord.Option(str, "Select a model", autocomplete=list_models, required=True),
                trim: discord.Option(str, "Select a trim", autocomplete=list_trims, required=False),
                year: discord.Option(str, "Select a year", autocomplete=list_years, required=False)):
    metric = await users.get_metric(ctx.author.id)
    car = await (cars.get_specs_metric(make, model, trim, year) if metric else cars.get_specs_imperial(make, model, trim, year))
    if car is None:
        await ctx.respond("Car could not be found.\nThere may be a typo or it has not been added to the bot yet.", ephemeral=True)
        return
    if trim and year:
        car_name = f'{year} {make} {model} {trim}'
    else:
        car_name = f'{car.get('year')} {car.get('name')}'
    embed = discord.Embed(color=embed_color, title=car_name)
    embed.set_image(url=attachment_head + car.get('url'))
    general = (f"Nationality: `{car.get('nation')}`\n"
               f"Class: `{car.get('class')}`\n"
               f"Performance Rating: `{car.get('rating')}`\n"
               f"Value: `₪ {car.get('value'):,}`")
    embed.add_field(name='General', inline=True, value=general)
    embed.add_field(name='', value='', inline=True)
    metrics = (f"Power: `{car.get('kW' if metric else 'hp')} {('kW' if metric else 'hp')}`\n"
               f"Torque: `{car.get('Nm' if metric else 'lb-ft')} {('Nm' if metric else 'lb-ft')}`\n"
               f"Weight: `{car.get('kg' if metric else 'lb')} {('kg' if metric else 'lb')}`\n"
               f"Pwr-to-wt: `{car.get('kW/kg' if metric else 'hp/lb')} {('kW/kg' if metric else 'hp/lb')}`")
    embed.add_field(name='Metrics', inline=True, value=metrics)
    performance = (f"Top Speed: `{car.get('kph' if metric else 'mph')} {('kph' if metric else 'mph')}`\n"
                   f"0-{('100 kph' if metric else '60 mph')}: `{car.get('0-100' if metric else '0-60')} s`\n"
                   f"Fuel: `{car.get('kpl' if metric else 'mpg')} {('kpl' if metric else 'mpg')}`\n"
                   f"Handling: `{car.get('G')} G`")
    embed.add_field(name='Performance', inline=True, value=performance)
    embed.add_field(name='', value='', inline=True)
    rating = (f"\nTop Speed: `{car.get('spd_r')}`\n"
              f"Acceleration: `{car.get('acc_r')}`\n"
              f"Fuel: `{car.get('fuel_r')}`\n"
              f"Handling: `{car.get('hand_r')}`")
    embed.add_field(name='Rating', inline=True, value=rating)
    await ctx.respond(embed=embed)



bot.run(config.get_bot_token())