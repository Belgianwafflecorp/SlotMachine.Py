import os
import json
import sqlite3

# Define the directory for JSON files
JSON_DIR = "PLAYER_DATA"

# Ensure that the directory exists

class JsonFileManager:
    def __init__(self, directory):
        self.directory = directory
        os.makedirs(JSON_DIR, exist_ok=True)

        self.balance_file = os.path.join(directory, "balance.json")
        self.highscore_file = os.path.join(directory, "highscore.json")
        self.spin_count_file = os.path.join(directory, "spin_count.json")
        self.multiplier_count_file = os.path.join(directory, "multiplier_count.json")
        self.broke_counter_file = os.path.join(directory, "broke_counter.json")
        self.best_spin_file = os.path.join(directory, "best_spin.json")
        self.jackpot_multiplier_counter_file = os.path.join(directory, "jackpot_multiplier_counter.json")

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

    def save_spin_count(self, spin_counter):
        self.save_data("spin_count.json", spin_counter)

    def update_spin_count(self):
        self.spin_counter += 1
        self.save_spin_count()


# MULTIPLIER COUNT
    def load_multiplier_count(self):
        return self.load_data("multiplier_count.json") or 0

    def save_multiplier_count(self, multiplier_counter):
        self.save_data("multiplier_count.json", multiplier_counter)

    def update_multiplier_count(self):
        self.multiplier_counter += 1
        self.save_multiplier_count()


# BROKE COUNTER
    def load_broke_counter(self):
        return self.load_data("broke_counter.json") or 0
    
    def save_broke_counter(self, broke_counter):
        self.save_data("broke_counter.json", broke_counter)

    def update_broke_counter(self):
        broke_counter = self.load_broke_counter()
        broke_counter += 1
        self.save_broke_counter(broke_counter)


# BEST SPIN 
    def load_best_spin(self):
        return self.load_data("best_spin.json") or 0

    def save_best_spin(self, best_spin):
        self.save_data("best_spin.json", best_spin)

# JACKPOT MULTIPLIER COUNTER
    def load_jackpot_multiplier_counter(self):
        return self.load_data("jackpot_multiplier_counter.json") or 0

    def save_jackpot_multiplier_counter(self, jackpot_multiplier_counter):
        self.save_data("jackpot_multiplier_counter.json", jackpot_multiplier_counter)

    def update_jackpot_multiplier_counter(self):
        self.jackpot_multiplier_counter += 1
        self.save_jackpot_multiplier_counter()