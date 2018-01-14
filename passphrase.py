import random

animals_file = open("animals.txt", "r")
animals = animals_file.read()
animals_file.close()

adjectives_file = open("adjectives.txt", "r")
adjectives = adjectives_file.read()
adjectives_file.close()

animals = animals.split("\n")
adjectives = adjectives.split("\n")

def generatePassphrase(words):

    tempPassphrase = ""

    tempPassphrase += "".join(random.sample(adjectives, words - 1))
    tempPassphrase += random.choice(animals)

    return tempPassphrase
