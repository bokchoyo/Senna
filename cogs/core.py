# @commands.slash_command()
# async def ignite(self, ctx):
#     user_id = ctx.author.id
#     user_name = ctx.author.name
#     embed = discord.Embed(color=self.bot.embed_color)
#     if not await self.bot.user_db.contains(user_id):
#         await self.bot.user_db.add_user(user_id, user_name)
#         embed.title = 'Welcome to Artura!'
#         embed.set_thumbnail(url=ctx.author.avatar.url)
#         embed.set_image(url=self.bot.attachment_head + '1303478655766495272/MTC.png')
#         embed.description = f"You have now ignited your engine {ctx.author.mention}\nEnjoy your adventure!"
#         await ctx.respond(embed=embed)
#     else:
#         embed.title = f'Welcome {user_name}!'
#         embed.set_thumbnail(url=ctx.author.avatar.url)
#         embed.description = f"Your engine is already ignited!"
#         await ctx.respond(embed=embed)