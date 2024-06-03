import sys
import os
from rich import print
from rich.table import Table
from slotmachine import DataBase
import slotmachine
import settings

class Dealer:

    def __init__(self):
        self.db = slotmachine.DataBase()
        self.settings = settings
        self.slotmachine = slotmachine

    def lv_up_max_bet(self, amount):
        self.db.update_column('max_bet', amount)

    def default_max_bet(self):
        self.db.update_column('max_bet', 100)

    def player_ask_dealer(self):
        self.clear_screen()
        choice = input("\nWould you like to increase your max bet? (y/n): ")
        
        if choice.lower() != 'n':
            print("\nlet me check your balance.\n")
            balance = self.db.get_column('balance')
            max_bet = self.db.get_column('max_bet')
            
            if balance >= 10000000 and max_bet <= 100000:
                self.lv_up_max_bet(1000000)
                print(f"The maximum bet we can let you place now is 1.000.000")
            elif balance >= 1000000 and max_bet <= 10000:
                self.lv_up_max_bet(100000)
                print(f"The maximum bet we can let you place now is 100.000")
            elif balance >= 100000 and max_bet <= 1000:
                self.lv_up_max_bet(10000)
                print(f"The maximum bet we can let you place now is 10.000")
            elif balance >= 10000 and max_bet == 100:
                self.lv_up_max_bet(1000)
                print(f"The maximum bet we can let you place now is 1000")
            else:
                print("You do not meet the requirements to increase your max bet.\n")

        
    def clear_screen(self):
        # For Windows
        if os.name == "nt":
            os.system("cls")
        # For Mac and Linux (os.name is 'posix')
        else:
            os.system("clear")

