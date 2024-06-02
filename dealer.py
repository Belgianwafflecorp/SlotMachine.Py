import sys
import os
from rich import print
from rich.table import Table
from slotmachine import DataBase
import slotmachine
import settings

class Dealer:

    def __init__(self):
        self.db = DataBase()
        self.settings = settings
        self.slotmachine = slotmachine

    def lv_up_max_bet(self, max_bet):
        self.new_max_bet = max_bet * 10
        self.db.update_column('max_bet', self.new_max_bet)

    def default_max_bet(self):
        self.db.update_column('max_bet', 100)

    def player_ask_dealer(self):
        self.clear_screen()
        choice = input("\nWould you like to increase your max bet? (y/n): ")
        
        if choice.lower() != 'n':
            print("\nlet me check your balance.\n")
            balance = self.db.get_column('balance')
            max_bet = self.db.get_column('max_bet')
            
            if balance >= 10000 and max_bet == 100:
                self.lv_up_max_bet(max_bet)
                print(f"Your max bet is now {self.new_max_bet}")
            elif balance >= 100000 and max_bet == 1000:
                self.lv_up_max_bet(max_bet)
                print(f"Your max bet is now {self.new_max_bet}")
            elif balance >= 1000000 and max_bet == 10000:
                self.lv_up_max_bet(max_bet)
                print(f"Your max bet is now {self.new_max_bet}")
            elif balance >= 10000000 and max_bet == 100000:
                self.lv_up_max_bet(max_bet)
                print(f"Your max bet is now {self.new_max_bet}")
            elif balance >= 100000000 and max_bet == 1000000:
                self.lv_up_max_bet(max_bet)
                print(f"Your max bet is now {self.new_max_bet}")
            else:
                print("You do not meet the requirements to increase your max bet.\n")

        
    def clear_screen(self):
        # For Windows
        if os.name == "nt":
            os.system("cls")
        # For Mac and Linux (os.name is 'posix')
        else:
            os.system("clear")

