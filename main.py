import discord
import config
import passphrase
import db
import mail
import asyncio

database = db.Database()
client = discord.Client()

class ServerInfo: #weird object to circumvent discord.py's blocking run function
    server = False
    role = False
serverInfo = ServerInfo()

async def mailLoop():
    await client.wait_until_ready()
    while not client.is_closed:
        print("tick")
        if len(database.db) > 0 and serverInfo.server != False and serverInfo.role != False:
            resultFromCheck = mail.check(database, client)
            if resultFromCheck != False:
                await client.add_roles(resultFromCheck, serverInfo.role)
                await client.send_message(serverInfo.server.get_channel(config.verifyChannel), "Verified user %s" % resultFromCheck.mention)
        await asyncio.sleep(config.wait)

@client.event
async def on_ready():
    print('Logged in')
    database.load()
    print('Database loaded')
    serverInfo.server = client.get_server(config.discordServer)
    serverInfo.role = discord.utils.get(serverInfo.server.roles, name=config.verified)

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    elif message.content.startswith('!thonk'):
        await client.send_message(message.channel, content = "<a:thinkspin:394968623753723905>") #AAU CPH discord animated emoji

    elif message.content.startswith('!verify'):
        keyword = passphrase.generatePassphrase(config.passphraseWords)

        while database.passphraseExists(keyword): #if passphrase is already used generate a new passphrase
            keyword = passphrase.generatePassphrase(config.passphraseWords)

        database.addUser(message.author, message.author.id, keyword)
        await client.send_message(
            message.channel,
            "%s this is your passphrase: `%s`\nPlease send an email to `aau@ludvig.xyz` from your Aalborg University email adress with the passphrase as the content to get verified. This process can take a few minutes" % (message.author.mention, keyword)
        )

client.loop.create_task(mailLoop())
client.run(config.token)
