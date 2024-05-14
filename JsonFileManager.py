import os
import json

# Define the directory for JSON files
JSON_DIR = "PLAYER_DATA"

# Ensure that the directory exists
os.makedirs(JSON_DIR, exist_ok=True)

class JsonFileManager:
    def __init__(self, directory):
        self.directory = directory
        self.balance_file = os.path.join(directory, "balance.json")
        self.highscore_file = os.path.join(directory, "highscore.json")
        self.spin_count_file = os.path.join(directory, "spin_count.json")
        self.multiplier_count_file = os.path.join(directory, "multiplier_count.json")
        self.spin_counter = self.load_spin_count()
        self.multiplier_counter = self.load_multiplier_count()

# SAVE DATA
    def save_data(self, filename, data):
        filepath = os.path.join(self.directory, filename)
        with open(filepath, "w") as f:
            json.dump(data, f)

# LOAD DATA
    def load_data(self, filename):
        filepath = os.path.join(self.directory, filename)
        if os.path.exists(filepath):
            with open(filepath, "r") as f:
                return json.load(f)
        else:
            return None

# BALANCE
    def load_balance(self):
        return self.load_data("balance.json") or 0

    def save_balance(self, balance):
        self.save_data("balance.json", balance)

    def print_balance(self, balance):
        print(f"Your balance is: \033[32m${balance}\033[0m \n")


# HIGHSCORE
    def load_highscore(self):
        return self.load_data("highscore.json") or 0

    def save_highscore(self, highscore):
        self.save_data("highscore.json", highscore)

    def print_highscore(self, highscore):
        if highscore != 0:
            print("Remember the time you had " + "\033[32m" + "$" + str(highscore) + "\033[0m" + "?")
            print("\033[36m" + "Time to double that!" + "\033[0m \n")
            

# SPIN COUNT
    def load_spin_count(self):
        return self.load_data("spin_count.json") or 0

    def save_spin_count(self):
        self.save_data("spin_count.json", self.spin_counter)

    def update_spin_count(self):
        self.spin_counter += 1
        self.save_spin_count()


# MULTIPLIER COUNT
    def load_multiplier_count(self):
        return self.load_data("multiplier_count.json") or 0

    def save_multiplier_count(self):
        self.save_data("multiplier_count.json", self.multiplier_counter)

    def update_multiplier_count(self):
        self.multiplier_counter += 1
        self.save_multiplier_count()

    def print_multiplier_count(self, multiplier_count):
        print("You've used the multiplier " + "\033[32m" + str(multiplier_count) + "\033[0m" + " times. \n")


# BROKE COUNTER
    def load_broke_counter(self):
        return self.load_data("broke_counter.json") or 0
    
    def save_broke_counter(self, broke_counter):
        self.save_data("broke_counter.json", broke_counter)

    def update_broke_counter(self):
        broke_counter = self.load_broke_counter()
        broke_counter += 1
        self.save_broke_counter(broke_counter)

    def print_broke_counter(self, broke_counter):
        if broke_counter != 0:
            print("You've gone broke " + "\033[31m" + str(broke_counter) + "\033[0m" + " times. \n")
        else:
             print("Do you know you never went broke with us? \n")


# DEALER
    def load_dealer_lv(self):
        return self.load_data("dealer_lv.json") or 0

    def save_dealer_lv(self):
        self.save_data("dealer_lv.json", self.dealer_lv)

    def update_dealer_lv_up(self, lv):
        self.dealer_lv =+ lv
        self.save_dealer_lv()

    def update_dealer_lv_down(self, lv):
        self.dealer_lv =- lv
        self.save_dealer_lv()

    def print_maximum_bets(self, dealer_lv):
        if dealer_lv == 0:
            print(f"Your maximum bets are \033[32m100\033[0m. \n")
        elif dealer_lv == 1:
            print(f"Your maximum bets are \033[32m1000\033[0m. \n")
        elif dealer_lv == 2:
            print(f"Your maximum bets are \033[32m5000\033[0m. \n")
        elif dealer_lv == 3:
            print(f"Your maximum bets are \033[32m10000\033[0m. \n")

    # define the max bet
    def load_max_bet(load_dealer_lv):
        if load_dealer_lv() is 0:
            max_bet = 100
        elif load_dealer_lv() is 1:
            max_bet = 1000
        elif load_dealer_lv() is 2:
            max_bet = 5000
        elif load_dealer_lv() is 3:
            max_bet = 10000
        

# Initialize the JsonFileManager instance
jsonFileManager = JsonFileManager(JSON_DIR)