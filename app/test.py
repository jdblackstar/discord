from player import *

name = input("What is your name? ")
josh = Player(name, 1000)
print("Your balance has been set to $1,000.")
while josh.balance > 0:
    josh.bet(int(input("How much would you like to bet? ")))
print("Game over.")
