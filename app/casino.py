import math
import random

class Player():
    def __init__(self, name, balance):
        self.name = name
        self.balance = balance

    def bet(self, amount):

        if self.balance >= amount:
            odds = random.choice(range(1, 101))
            if odds % 2 == 0:
                # even number, win
                print("You win!")
                self.balance = self.balance + amount
            else:
                # odd number, lose
                print("You suck.")
                self.balance = self.balance - amount
        else:
            print("Insufficient funds.")

        print("Balance: ", self.balance)

    def check(self):
        print("Your balance is: ", self.balance)

name = input("What is your name? ")
josh = Player(name, 1000)
print("Your balance has been set to $1,000.")
while josh.balance > 0:
    josh.bet(int(input("How much would you like to bet? ")))
print("Game over.")