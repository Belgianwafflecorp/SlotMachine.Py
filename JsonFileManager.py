import os
import json

class JsonFileManager:
    def __init__(self, directory):
        self.directory = directory
        self.balance_file = os.path.join(directory, "balance.json")
        self.highscore_file = os.path.join(directory, "highscore.json")
        self.spin_count_file = os.path.join(directory, "spin_count.json")
        self.multiplier_count_file = os.path.join(directory, "multiplier_count.json")
        self.spin_counter = self.load_spin_count()
        self.multiplier_counter = self.load_multiplier_count()


# BALANCE
    def load_data(self, filename):
        filepath = os.path.join(self.directory, filename)
        if os.path.exists(filepath):
            with open(filepath, "r") as f:
                return json.load(f)
        else:
            return None

    def save_data(self, filename, data):
        filepath = os.path.join(self.directory, filename)
        with open(filepath, "w") as f:
            json.dump(data, f)

    def load_balance(self):
        return self.load_data("balance.json")

    def save_balance(self, balance):
        self.save_data("balance.json", balance)


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


# Define the directory for JSON files
JSON_DIR = ".gitignore"

# Ensure that the directory exists
os.makedirs(JSON_DIR, exist_ok=True)

# Initialize the JsonFileManager instance
jsonFileManager = JsonFileManager(JSON_DIR)
