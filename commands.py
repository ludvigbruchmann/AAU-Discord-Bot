import json

class CustomCommands:

    def __init__(self):
        self.load()

    def load(self, commandsFile="commands.json"):

        commands = {}

        try:
            commands_file = open(commandsFile, "r")
            self.commands = commands_file.read()
            commands_file.close()
            try:
                self.commands = json.loads(self.commands)
            except json.JSONDecodeError as e:
                print("Commands file is corrupted, generating new commands file")
                self.commands = {}
                self.save(commandsFile)
        except FileNotFoundError as e:
            print("No commands file found, generating new commands file")
            self.commands = {}
            self.save(commandsFile)

    def addCommand(self, command, response): #make sure to only allow moderators access to this function

        if not self.commands.get(command):
            self.commands[command] = response
            self.save()
            return True
        else:
            return False #make this some kind of exception

    def editCommand(self, command, response): #make sure to only allow moderators access to this function

        if self.commands.get(command):
            self.commands[command] = response
            self.save()
            return True
        else:
            return False #make this some kind of exception

    def removeCommand(self, command): #make sure to only allow moderators access to this function

        if self.commands.get(command):
            del self.commands[command]
            self.save()
            return True
        else:
            return False #make this some kind of exception

    def command(self, command, args = ""):

        #TODO: Add variables like $user or $arg to allow commands like !slap [user] etc.

        if self.commands.get(command):
            return self.commands[command]
        else:
            return False

    def save(self, commandsFile="commands.json"):

        commands_file = open(commandsFile, "w")
        commands_file.write(json.dumps(self.commands))
        commands_file.close()
