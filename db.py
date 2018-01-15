import json
import config


class Database:

    """
    Database.
    """

    db = {}

    def __init__(self):
        self.load()

    def autosave(self, dbFile="db.json"):

        """
        Saves the database if config.autosave is True.
        """

        if config.autosave:
            self.save(dbFile)

    def load(self, dbFile="db.json"):

        """
        Loads the database.
        """

        try:
            db_file = open(dbFile, "r")
            self.db = db_file.read()
            db_file.close()
            try:
                self.db = json.loads(self.db)
            except json.JSONDecodeError as e:
                print("Database file is corrupted, generating new database")
                self.db = {}
                self.save(dbFile)
        except FileNotFoundError as e:
            print("No database found, generating new database")
            self.db = {}
            self.save(dbFile)

    def save(self, dbFile="db.json", data=None):

        """
        Saves the database.
        """

        if data is None:
            data = self.db

        db_file = open(dbFile, "w")
        db_file.write(json.dumps(data))
        db_file.close()

    def passphraseExists(self, passphrase):

        """
        Checks if a passphrase belongs to a user. Used when generating a new passphrase.
        """

        if self.getPassphrase(passphrase) != False:
            return True
        else:
            return False

    def emailUsed(self, email):

        """
        Checks if a passphrase belongs to a user. Used when generating a new passphrase.
        """

        if self.getEmail(email) != False:
            return True
        else:
            return False

    def addUser(self, username, id, passphrase):

        """"
        Adds a user to the database
        """

        username = str(username)
        id = str(id)

        self.db[id] = config.defaultUser.copy()
        self.db[id]["username"] = username
        self.db[id]["id"] = id
        self.db[id]["passphrase"] = passphrase

        self.autosave() #save the database if config.autosave is True

    def verify(self, id, email):

        """
        Verifies a user.
        """

        try:
            self.db[id]["verified"] = True
            self.db[id]["email"] = email
            self.db[id]["passphrase"] = ""

            self.autosave() #save the database if config.autosave is True
        except KeyError:
            print("User '%s' does not exist" % username)

    def getPassphrase(self, passphrase):

        """
        Returns the user with specified passphrase.
        """

        for user in self.db:
            if self.db[user]["passphrase"] == passphrase:
                return self.db[user]
        return False

    def getEmail(self, email):

        """
        Returns the user with specified passphrase.
        """

        for user in self.db:
            if self.db[user]["email"] == email:
                return user
        return False

    def getUser(self, id):

        try:
            return self.db[id]
        except KeyError as e:
            return False
