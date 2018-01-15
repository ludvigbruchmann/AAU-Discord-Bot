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
    verifiedRole = False
serverInfo = ServerInfo()

def cmd(command):
    return config.commandPrefix + command

async def mailLoop():
    await client.wait_until_ready()
    while not client.is_closed:
        if len(database.db) > 0 and serverInfo.server != False and serverInfo.verifiedRole != False:
            resultFromCheck = mail.check(database, client)
            if resultFromCheck != False:
                await client.add_roles(resultFromCheck, serverInfo.verifiedRole)
                await client.send_message(serverInfo.server.get_channel(config.verifyChannel), "Verified user %s" % resultFromCheck.mention)
        await asyncio.sleep(config.wait)

@client.event
async def on_ready():
    print('Logged in')
    database.load()
    print('Database loaded')
    serverInfo.server = client.get_server(config.discordServer)
    serverInfo.verifiedRole = discord.utils.get(serverInfo.server.roles, name=config.verified)

@client.event
async def on_message(message):

    if config.printChat:
        print('[%s] %s: %s' % (message.channel, message.author, message.content))

    if message.author == client.user:
        return

    elif message.content.startswith(cmd('assign')):
        if serverInfo.verifiedRole in message.author.roles:
            if len(message.content.split()) > 1:
                tempRole = message.content.split()[1]
                if tempRole in config.studyProgrammes:
                    for role in config.studyProgrammes:
                        tempRole2 = discord.utils.get(serverInfo.server.roles, name=role)
                        if tempRole2 in message.author.roles:
                            client.remove_roles(message.author, tempRole2)
                    await client.add_roles(message.author, discord.utils.get(serverInfo.server.roles, name=tempRole))
                    await client.send_message(message.channel, "Added user %s to %s" % (message.author.mention, tempRole))
                else:
                    await client.send_message(message.channel, "Study programme %s does not exist" % tempRole)
            else:
                await client.send_message(message.channel, "Please specify a study programme")

    elif message.content.startswith(cmd('thonk')):
        await client.send_message(message.channel, content = "<a:thinkspin:394968623753723905>") #AAU CPH discord animated emoji

    elif message.content.startswith(cmd('verify')):
        keyword = passphrase.generatePassphrase(config.passphraseWords)

        while database.passphraseExists(keyword): #if passphrase is already used generate a new passphrase
            keyword = passphrase.generatePassphrase(config.passphraseWords)

        if database.getUser(message.author.id) == False:
            database.addUser(message.author, message.author.id, keyword)

            try: #try sending the passphrase to user in a dm
                await client.send_message(
                    message.author,
                    "%s this is your passphrase: `%s`\nPlease send an email to `%s` from your Aalborg University email adress with the passphrase as the content to get verified. This process can take a few minutes" % (message.author.mention, keyword, config.username)
                )
            except discord.errors.Forbidden as e: #If user does not allow dm's from server members we will send the passphrase in the verify channel instead
                await client.send_message(
                    serverInfo.server.get_channel(config.verifyChannel),
                    "%s this is your passphrase: `%s`\nPlease send an email to `%s` from your Aalborg University email adress with the passphrase as the content to get verified. This process can take a few minutes" % (message.author.mention, keyword, config.username)
                )

client.loop.create_task(mailLoop())
client.run(config.token)
