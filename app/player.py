import math
import random


class Player():
    def __init__(self, name, balance):
        self.name = name
        self.balance = balance

    def bet(self, amount: int):  # mostly for testing

        if self.balance >= amount:
            odds = random.choice(range(1, 101))
            if odds % 2 == 0:
                # even number, win
                print("You win!")
                self.balance += amount
            else:
                # odd number, lose
                print("You suck.")
                self.balance -= amount
        else:
            print("Insufficient funds.")

        print("Balance: ", self.balance)

    def pay(self, amount: int):
        if self.balance >= amount:
            self.balance -= amount
            return amount
        else:
            print("Insufficient funds.")

    def get(self, amount: int):
        self.balance += amount
        return self.balance

    def check(self):
        print("Your balance is: ", self.balance)
