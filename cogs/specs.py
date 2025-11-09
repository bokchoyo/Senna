import discord
from discord.ext import commands
from orjson import orjson


class Specs(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.cache = {}
        self.cars_list = {}
        self.load_data()
        self.load_cache()

    def load_data(self):
        with open(r'C:\Users\bokch\PyCharm\W1\data\cars_list.json', 'rb') as f:
            self.cars_list = orjson.loads(f.read())

    def load_cache(self):
        with open(r'C:\Users\bokch\PyCharm\W1\data\specs_cache.json', 'rb') as f:
            self.cache = orjson.loads(f.read())

    def close(self):
        self.save_cache()
        print("Saved Cache")

    def save_cache(self):
        with open(r'C:\Users\bokch\PyCharm\W1\data\specs_cache.json', 'wb') as f:
            f.write(orjson.dumps(self.cache, option=orjson.OPT_INDENT_2))

    # async def get_nested_list(self, keys, fallback):
    #     target = self.cars_list
    #     for key in keys:
    #         target = target.get(key, {})
    #     return target.get(fallback, [])

    # if list_type == 'make':
    #     prev_list = cache.get(val[:-1], self.cars_list['makes'])
    # else:
    #     # Extract make, model, and trim from options for nested lookups
    #     make = ctx.options.get('make', '')
    #     model = ctx.options.get('model', '')
    #     trim = ctx.options.get('trim', '')
    #
    #     # Determine the path based on the list_type
    #     keys = [make, model, trim][:['model', 'trim', 'year'].index(list_type) + 1]
    #     fallback_key = f"{list_type}_list"
    #
    #     # Cache setup for specific make, model, or trim level
    #     current_cache = cache
    #     for key in keys:
    #         current_cache = current_cache.setdefault(key, {})
    #
    #     if val in current_cache:
    #         return current_cache[val]
    #     prev_list = await self.get_nested_list(keys, fallback_key)
    #
    # # Filter the list based on the input value
    # new_list = [item for item in prev_list if item.lower().startswith(val)]
    # cache[val] = new_list
    # return new_list

    # async def get_list(self, ctx: discord.AutocompleteContext, list_type, parent_key=None):
    #     user_id = str(ctx.interaction.user.id)
    #     val = ctx.value
    #     cache = self.cache[list_type]
    #     list_key = f"{list_type}_list"
    #     if not val:
    #         cache[user_id] = {}
    #         if not parent_key:
    #             return self.cars_list[list_key]
    #         else:
    #             parent_data = await self.get_nested_key(parent_key)
    #             if list_type == 'year':
    #                 return parent_data
    #             return parent_data[list_key]
    #     user_cache = cache.setdefault(user_id, {})
    #     if len(val) != 1:
    #         prev_list = user_cache.get(val[:-1], None)
    #         if not prev_list:
    #             last_cache = next(reversed(user_cache), None)
    #             if last_cache:
    #                 prev_list = user_cache[last_cache]
    #                 if len(prev_list) == 1:
    #                     return prev_list
    #             else:
    #                 if not parent_key:
    #                     prev_list = self.cars_list[list_key]
    #                 else:
    #                     parent_data = await self.get_nested_key(parent_key)
    #                     if list_type == 'year':
    #                         prev_list = parent_data
    #                     else:
    #                         prev_list = parent_data[list_key]
    #     else:
    #         if not parent_key:
    #             prev_list = self.cars_list[list_key]
    #         else:
    #             parent_data = await self.get_nested_key(parent_key)
    #             if list_type == 'year':
    #                 prev_list = parent_data
    #             else:
    #                 prev_list = parent_data[list_key]
    #     new_list = [item for item in prev_list if item.lower().startswith(val.lower())]
    #     user_cache[val] = new_list
    #     return new_list

    async def get_list(self, ctx: discord.AutocompleteContext, list_type):
        val = ctx.value.lower()
        cache = self.cache[list_type]
        if list_type == 'make':
            if val in cache:
                return cache[val]
            prev_list = cache.get(val[:-1], self.cars_list['makes'])
        elif list_type == 'model':
            make = ctx.options.get('make')
            cache = cache.setdefault(make, {})
            if val in cache:
                return cache[val]
            prev_list = cache.get(val[:-1], self.cars_list[make]['models'])
        elif list_type == 'trim':
            make = ctx.options.get('make')
            model = ctx.options.get('model')
            cache = cache.setdefault(make, {}).setdefault(model, {})
            if val in cache:
                return cache[val]
            prev_list = cache.get(val[:-1], self.cars_list[make][model]['trims'])
        else:
            make = ctx.options.get('make')
            model = ctx.options.get('model')
            trim = ctx.options.get('trim')
            cache = cache.setdefault(make, {}).setdefault(model, {}).setdefault(trim, {})
            if val in cache:
                return cache[val]
            prev_list = cache.get(val[:-1], self.cars_list[make][model][trim])
        new_list = [item for item in prev_list if item.lower().startswith(val)]
        if new_list:
            cache[val] = new_list
        return new_list
    #
    # async def list_makes(self, ctx: discord.AutocompleteContext):
    #     return await self.get_list(ctx, 'make')
    #
    # async def list_models(self, ctx: discord.AutocompleteContext.options):
    #     return await self.get_list(ctx, 'model')
    #
    # async def list_trims(self, ctx: discord.AutocompleteContext.options):
    #     return await self.get_list(ctx, 'trim')
    #
    # async def list_years(self, ctx: discord.AutocompleteContext.options):
    #     return await self.get_list(ctx, 'year')

    async def has_trim(self, make, model):
        return self.cars_list[make][model].get("trims", []) != ["-"]

    # async def get_list(self, ctx: discord.AutocompleteContext, list_type):
    #     val = ctx.value.lower()
    #
    #     if list_type == 'make':
    #         options = self.cars_list['makes']
    #     elif list_type == 'model':
    #         make = ctx.options.get('make')
    #         if not make:
    #             return []
    #         options = self.cars_list[make].get('models', [])
    #     elif list_type == 'trim':
    #         make = ctx.options.get('make')
    #         model = ctx.options.get('model')
    #         if not make or not model:
    #             return []
    #         options = self.cars_list[make][model].get('trims', [])
    #     else:
    #         make = ctx.options.get('make')
    #         model = ctx.options.get('model')
    #         trim = ctx.options.get('trim')
    #         if not make or not model or not trim:
    #             return []
    #         options = self.cars_list[make][model].get(trim, [])
    #
    #     new_list = [item for item in options if item.lower().startswith(val)]
    #     return new_list

    async def list_makes(self, ctx: discord.AutocompleteContext):
        return await self.get_list(ctx, 'make')

    async def list_models(self, ctx: discord.AutocompleteContext):
        return await self.get_list(ctx, 'model')

    async def list_trims(self, ctx: discord.AutocompleteContext):
        return await self.get_list(ctx, 'trim')

    async def list_years(self, ctx: discord.AutocompleteContext):
        return await self.get_list(ctx, 'year')

    @commands.slash_command(description='View the specifications of a car')
    async def specs(self, ctx: discord.ApplicationContext,
                    make: discord.Option(str, "Select a make", autocomplete=list_makes, required=True),
                    model: discord.Option(str, "Select a model", autocomplete=list_models, required=True),
                    trim: discord.Option(str, "Select a trim", autocomplete=list_trims, required=False),
                    year: discord.Option(str, "Select a year", autocomplete=list_years, required=False)):
        user_id = ctx.author.id
        metric = await self.bot.user_db.get_metric(user_id)
        car = await (self.bot.car_db.get_specs_metric(make, model, trim, year) if metric
                     else self.bot.car_db.get_specs_imperial(make, model, trim, year))
        if car is None:
            await ctx.respond('Car could not be found.\n'
                              'There may be a typo or it has not been added to the bot yet.', ephemeral=True)
            return
        car_name = f'{year} {make} {model} {trim}' if year else f"{car.get('year')} {make} {model} {trim}"
        embed = discord.Embed(color=self.bot.embed_color, title=car_name)
        embed.set_image(url=self.bot.attachment_head + car.get('url'))
        general = (f"Nationality: `{car.get('nation')}`\n"
                   f"Class: `{car.get('class')}`\n"
                   f"Performance Rating: `{car.get('rating')}`\n"
                   f"Value: `₪ {car.get('value'):,}`")
        embed.add_field(name='General', inline=True, value=general)
        embed.add_field(name='', value='', inline=True)
        units = {
            True: ["kW", "Nm", "kg", "kW/kg", "kph", "0-100", "kpl"],
            False: ["hp", "lb-ft", "lb", "hp/lb", "mph", "0-60", "mpg"]
        } [metric]
        metrics = "\n".join([
            f"Power: `{car.get(units[0])} {units[0]}`",
            f"Torque: `{car.get(units[1])} {units[1]}`",
            f"Weight: `{car.get(units[2])} {units[2]}`",
            f"Pwr-to-wt: `{car.get(units[3])} {units[3]}`"
        ])
        embed.add_field(name='Metrics', inline=True, value=metrics)
        performance = "\n".join([
            f"Top Speed: `{car.get(units[4])} {units[4]}`",
            f"0-{('100 kph' if metric else '60 mph')}: `{car.get(units[5])} s`",
            f"Fuel: `{car.get(units[6])} {units[6]}`",
            f"Handling: `{car.get('G')} G`"
        ])
        embed.add_field(name='Performance', inline=True, value=performance)
        embed.add_field(name='', value='', inline=True)
        rating = (f"\nTop Speed: `{car.get('spd_r')}`\n"
                  f"Acceleration: `{car.get('acc_r')}`\n"
                  f"Fuel: `{car.get('fuel_r')}`\n"
                  f"Handling: `{car.get('hand_r')}`")
        embed.add_field(name='Rating', inline=True, value=rating)
        await ctx.respond(embed=embed)

def setup(bot):
    bot.add_cog(Specs(bot))
