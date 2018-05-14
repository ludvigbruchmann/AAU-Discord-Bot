#db
autosave = True #recommended
defaultUser = {
    "verified": False,
    "passphrase": "",
    "username": "",
    "email": "",
    "id": ""
}
passphraseWords = 4

#discord
token = '#'
discordServer = '#'
commandPrefix = "!"
printChat = True

verified = 'Verified Student'
verifyChannel = '#'
assignChannel = '#'

moderatorRole = 'Moderators'

studyProgrammes = [
    'ITCOM'
]

#mail
server = '#'
username = '#'
password = '#'
universityDomain = "aau.dk"
wait = 60 #seconds to wait in between refreshing email
casUrl = 'https://signon.aau.dk/cas/login'
redirectUrl = 'http://localhost:5000/verify/'
verifyUrl = 'https://signon.aau.dk/cas/serviceValidate'
