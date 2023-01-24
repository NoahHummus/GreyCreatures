import dbm
from urllib import response
from database import *
import lightbulb
import hikari
import random


bot = lightbulb.BotApp(token="", default_enabled_guilds=(966169335431303198))

db = Database()


@bot.command
@lightbulb.option('name', 'Name of the creature to murde....euthanize', str, required=True)
@lightbulb.command('euthanize', 'Euthanize your creature. This kills the creature.')
@lightbulb.implements(lightbulb.PrefixCommand, lightbulb.SlashCommand)
async def give(ctx: lightbulb.Context) -> None:
    user = ctx.author
    name = ctx.options.name
    result = db.euthanize_creature(user,name)
    if result.get("notalive"):
        await ctx.respond(result.get("notalive"))
    if result.get("notowner"):
        await ctx.respond(result.get("notowner"))
    if result.get("notexist"):
        await ctx.respond(result.get("notexist"))
    if result.get("success"):
        await ctx.respond(result.get("success"))

@bot.command
@lightbulb.option('target', 'Enter a username', hikari.Member, required=True)
@lightbulb.command('attack', 'Send your creature to fight another creature. Its a fight to the death.')
@lightbulb.implements(lightbulb.PrefixCommand, lightbulb.SlashCommand)
async def attack(ctx: lightbulb.Context) -> None:
    user = ctx.author
    target = ctx.options.target
    duelresult = db.creature_dueldb(user,target)
    message = duelresult.get("message")
    combattext = duelresult.get("combattext")
    if message.get("oncooldown"):
        await ctx.respond(message.get("oncooldown"))    
    if message.get("nousercreature"):
        await ctx.respond(message.get("nousercreature"))
    if message.get("targetself"):
        await ctx.respond(message.get("targetself"))
    if message.get("notargetcreature"):
        await ctx.respond(message.get("notargetcreature"))
    if message.get("success"):
        #await ctx.respond(hikari.Embed(title=f'----------------------+ LEADERBOARD +----------------------',colour=0x3B9DFF,).add_field(name=f"<@{target}> VERSES <@{target}>",value = combattext))
        await ctx.respond(f"ATTACKER : <@{user.id}> --------- VERSUS --------- <@{target.id}> : DEFENDER")
        await ctx.respond(combattext)
        await ctx.respond(message.get("success"))

@bot.command
@lightbulb.command('harvest', 'skin that grey creature!')
@lightbulb.implements(lightbulb.PrefixCommand, lightbulb.SlashCommand)
async def harvest(ctx: lightbulb.Context) -> None:
    user = ctx.author
    result = db.farmcreature(user)
    if result.get("success"):
        await ctx.respond(result.get("success"))
    if result.get("tooearly"):
        await ctx.respond(result.get("tooearly"))
    if result.get("nocreature"):
        await ctx.respond(result.get("nocreature"))


@bot.command
@lightbulb.option( 'name', 'Name your creature! - 20 character limit', str, required=True)
@lightbulb.command('plant', 'get on your way to having your very own grey creature!')
@lightbulb.implements(lightbulb.PrefixCommand, lightbulb.SlashCommand)
async def plant(ctx: lightbulb.Context) -> None:
    user = ctx.author
    lowername = ctx.options.name
    name = lowername.upper()
    if len(name) > 20:
        await ctx.respond("Failure : name exceeded 16 characters")
        return
    check = db.select_creature_name(name)
    if check:
        await ctx.respond("Failure : creature already exists. Name needs to be unique")
        return
    result = db.plantcreature(user,name)
    if result.get("oncooldown"):
        await ctx.respond(result.get("oncooldown"))
    if result.get("spawned"):
        await ctx.respond(result.get("spawned"))
    if result.get("limitreached"):
        await ctx.respond(result.get("limitreached"))
    if result.get("nowork"):
        await ctx.respond(result.get("nowork"))
    if result.get("insufficientfunds"):
        await ctx.respond(result.get("insufficientfunds"))
    
@bot.command
@lightbulb.option('target', 'The person you want to give flakes', hikari.Member, required=True)
@lightbulb.option( 'amount', 'The amount you want to give', int, required=True)
@lightbulb.command('give', 'Give some of your flakes to another user.')
@lightbulb.implements(lightbulb.PrefixCommand, lightbulb.SlashCommand)
async def give(ctx: lightbulb.Context) -> None:
    amount = ctx.options.amount
    user = ctx.author
    target = ctx.options.target
    await ctx.respond(db.giveflakes(user,target,amount))

@bot.command
@lightbulb.option('target', 'who you attempting to steal from.', hikari.Member, required=True)
@lightbulb.command('rob', 'robin.')
@lightbulb.implements(lightbulb.PrefixCommand, lightbulb.SlashCommand)
async def rob(ctx: lightbulb.Context) -> None:
    user = ctx.author
    target = ctx.options.target
    await ctx.respond(db.robdb(user,target))



def getbabinpic():
    filelist = [r"C:\Discord bot\photos\babin\babin1.png", r"C:\Discord bot\photos\babin\babin2.png", r"C:\Discord bot\photos\babin\babin3.png", 
    r"C:\Discord bot\photos\monkey\monkey1.png", r"C:\Discord bot\photos\monkey\monkey2.png", r"C:\Discord bot\photos\monkey\monkey3.png", 
    r"C:\Discord bot\photos\babin\babin4.png", r"C:\Discord bot\photos\babin\babin5.png", r"C:\Discord bot\photos\babin\babin6.png", 
    r"C:\Discord bot\photos\babin\babin7.png", r"C:\Discord bot\photos\babin\babin8.png", r"C:\Discord bot\photos\babin\babin9.png", 
    r"C:\Discord bot\photos\babin\babin10.png", r"C:\Discord bot\photos\babin\babin11.png"]
    selector = random.randint(0,len(filelist)-1)
    t = hikari.File(filelist[selector])
    return t


@bot.command
@lightbulb.option('target', 'who you attempting to steal from.', hikari.Member, required=True)
@lightbulb.command('test', 'test')
@lightbulb.implements(lightbulb.SlashCommand)   
async def test(ctx):
    username = ctx.author.id
    target = ctx.options.target.id
    await ctx.respond(f"<@{target}>")


@bot.command
@lightbulb.command('pukeypants', 'puke in the pants')
@lightbulb.implements(lightbulb.SlashCommand)   
async def pukepant(ctx):
    f = hikari.File('C:\Discord bot\photos\pukeypants.png')
    await ctx.respond(f)




@bot.command
@lightbulb.command('babinhype', 'babin HYPE')
@lightbulb.implements(lightbulb.SlashCommand)   
async def babinhype(ctx):
    await ctx.respond(getbabinpic())


@bot.command
@lightbulb.command('work', 'Get flakes')
@lightbulb.implements(lightbulb.SlashCommand)   
async def work(ctx):
    workusername = ctx.author
    await ctx.respond(db.workdb(workusername))

@bot.command
@lightbulb.command('daily', 'Once a day yield!')
@lightbulb.implements(lightbulb.SlashCommand)   
async def daily(ctx):
    workusername = ctx.author
    await ctx.respond(db.dailydb(workusername))   

@bot.command
@lightbulb.option('amount', 'Bet amount', int, required=True)
@lightbulb.command('slot', '/slotinfo for payouts')
@lightbulb.implements(lightbulb.SlashCommand)   
async def slot(ctx):
    amount = ctx.options.amount
    slotusername = ctx.author
    result = db.slotdb(slotusername, amount)
    if type(result) == str:
        await ctx.respond(result)
    else:
        if result.get("winresponse"):
            response = result.get("winresponse")
            roll = result.get("roll")
            await ctx.respond(f"{roll} : {response}")
        else:
            response = result.get("lossresponse")
            roll = result.get("roll")
            await ctx.respond(f"{roll} : {response}")


@bot.command
@lightbulb.command('doubleornothing', 'You feeling lucky?')
@lightbulb.implements(lightbulb.SlashCommand)   
async def slot(ctx):
    doubleusername = ctx.author
    await ctx.respond(db.doubleornothingdb(doubleusername))

@bot.command
@lightbulb.command('leaderboard', 'who got them flakes')
@lightbulb.implements(lightbulb.SlashCommand)   
async def leaderboard(ctx):
    await ctx.respond(hikari.Embed(
title=f'----------------------+ LEADERBOARD +----------------------',
colour=0x3B9DFF,
)
.add_field(
name=f'NAME - GREY FLAKES :',
value = db.flakeleaderboard()
))


@bot.command
@lightbulb.command('xpleaderboard', 'who got them xp')
@lightbulb.implements(lightbulb.SlashCommand)   
async def leaderboard(ctx):
    await ctx.respond(hikari.Embed(
title=f'----------------------+ XP LEADERBOARD +----------------------',
colour=0x3B9DFF,
)
.add_field(
name=f'NAME - XP :',
value = db.xpleaderboard()
))


@bot.command
@lightbulb.command('slotinfo', 'Check payouts & odds')
@lightbulb.implements(lightbulb.SlashCommand)   
async def leaderboard(ctx):
    await ctx.respond(hikari.Embed(
title=f'----------------------+ SLOT INFO +----------------------',
colour=0x3B9DFF,
)
.add_field(
name=f'Slot info:',
value = db.slotinfo()
))

@bot.command
@lightbulb.option( 'name', '/creaturelist to get names', str, required=True)
@lightbulb.command('creatureinfo', 'Get more info on a creach')
@lightbulb.implements(lightbulb.PrefixCommand, lightbulb.SlashCommand)
async def creatureinfo(ctx: lightbulb.Context) -> None:
    target = ctx.options.name
    if db.creatureinfodb(target.upper()) == "fail":
        await ctx.respond(f"A creature with the name of {target} does not exist")
        return
    text,name = db.creatureinfodb(target.upper())
    await ctx.respond(hikari.Embed(
title=f'----------------------+ Creature Info +----------------------',
colour=0x3B9DFF,
)
.add_field(
name=f'{name.upper()} :',
value = text
))

@bot.command
@lightbulb.command('creaturelist', 'Check dem creatures out')
@lightbulb.implements(lightbulb.SlashCommand)   
async def creaturelist(ctx):
    await ctx.respond(hikari.Embed(
title=f'----------------------+ Creatures who have yet to die +----------------------',
colour=0x3B9DFF,
)
.add_field(
name=f'Creaturename : Owner : Confirmed Kills',
value = db.creaturelistdb()
))


@bot.command
@lightbulb.command('halloffame', 'Top 10 creatures')
@lightbulb.implements(lightbulb.SlashCommand)   
async def halloffame(ctx):
    await ctx.respond(hikari.Embed(
title=f'----------------------+ TOP 10 killas (DEAD & ALIVE) +----------------------',
colour=0x3B9DFF,
)
.add_field(
name=f'Creaturename (Alive): Owner : Confirmed Kills',
value = db.creaturelist_top10_db()
))




bot.run()