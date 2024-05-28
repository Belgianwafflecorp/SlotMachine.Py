import os
import random
import JsonFileManager as json_fm
from controls import PlayerControls
from quotes import quotes_win, quotes_loss
from settings import (
    ROWS,
    COLS,
    MAX_LINES,
    MAX_BET,
    MIN_BET,
    symbol_count,
    symbol_values,
    JSON_DIR,
    slot_machine_part_1,
    slot_machine_part_3,
    slot_machine_part_4,
    probabilities,
)
from rich import print
from rich.table import Table

class SlotMachine:
    def __init__(self) -> None:
        self.json_fm = json_fm.JsonFileManager(JSON_DIR)
        self.load_player()
        self.rows = ROWS
        self.cols = COLS
        self.sessie_spins = 0
        self.symbol_count = symbol_count  # number of each symbol per slot machine
        self.symbol_values = symbol_values  # value of each symbol
        self.slot_machine_part_1 = slot_machine_part_1
        self.slot_machine_part_3 = slot_machine_part_3
        self.slot_machine_part_4 = slot_machine_part_4
        self.min_bet = MIN_BET
        self.max_bet = MAX_BET

    def load_player(self):
        self.balance = self.json_fm.load_balance()
        self.highscore = self.json_fm.load_highscore()
        self.spin_counter = self.json_fm.load_spin_count()
        self.multiplier_counter = self.json_fm.load_multiplier_count()
        self.broke_counter = self.json_fm.load_broke_counter()

    def save_player(self):
        self.json_fm.save_balance(self.balance)
        self.json_fm.save_highscore(self.highscore)
        self.json_fm.save_spin_count(self.spin_counter)
        self.json_fm.save_multiplier_count(self.multiplier_counter)
        self.json_fm.save_broke_counter(self.broke_counter)

    def update_multiplier_counter(self):
        self.multiplier_counter += 1
        self.save_player()

    def update_broke_counter(self):
        self.broke_counter += 1
        self.save_player()

    def update_spin_counter(self):
        self.spin_counter += 1
        self.save_player()

    def update_highscore(self):
        self.highscore = max(self.highscore, self.balance)
        self.save_player()

    def player_broke(self):
        if self.balance < 1:
            self.update_broke_counter()
            print("Your out of chips, make a new deposit to continue playing")
            s.deposit()

    def deposit(self):
        while True:
            amount = input("Enter the amount you want to deposit: $")
            if amount.isdigit():
             amount = int(amount)
             if amount == 1069:
                 print("\nCheeky basterd. I'll let that one slide.\n")
             elif amount > 1000 and amount != 1069:
                 print("Don't get over your head. You get $1000 to start with.")
                 amount = 1000
             elif amount <= 0:
                 print("Please enter a positive amount.")
             break
            else:
             print("Please enter a valid amount.")
             return amount
        self.balance += amount

    def slot_machine_part_2(self):
        # display the row of self.slots vertically so row 1 is column 1
        # double
        s = ""
        for i in range(self.rows):
            s += " " * 12 + "|[red]" + " ║"
            for j in range(self.cols):
                s += (
                    self.slots[j][i] + " ║"
                    if j != self.cols - 1
                    else self.slots[j][i] + " ║"
                )

            s += "[/red] |\n" if i != self.rows - 1 else "[/red] |"
        return s

    def display_slot_machine(self):
        print(self.slot_machine_part_1)
        print(self.slot_machine_part_2())
        print(self.slot_machine_part_3)
        print(self.show_winnings())
        print(self.slot_machine_part_4)

    def show_winnings(self):
        winning_len = len(str(self.winnings))
        spaces_needed = 15 - winning_len - 2

        s = " " * 12 + "|" + " " * spaces_needed
        remaining = 15 - spaces_needed - winning_len

        if self.winnings > 0:
            s += f"[bold yellow]{self.winnings}[/bold yellow]"
        else:
            s += f"[red]{self.winnings}[/red]"

        s += " " * remaining + "|--'"
        return s

    def get_slot_machine_spin(self):
        # set self.slots to a random selection of symbols keep in mind the amount of each symbol
        # random.sample( list(self.symbol_count.keys()), 1, counts=self.symbol_count.values() )
        self.slots = [
            random.choices(
                list(self.symbol_count.keys()),
                k=self.rows,
                weights=self.symbol_count.values(),
            )
            for _ in range(self.cols)
        ]

    def get_min_max_bet(self):
        return self.min_bet, self.max_bet

    def get_bet(self):
        self.min_bet, self.max_bet = self.get_min_max_bet()
        bet = None
        while not bet:
            # show balance
            print(
                f"Your balance is: {self.balance}. \n"
                f"how much would you like to bet? between {self.min_bet} and {self.max_bet}:",
                end=" ",
            )
            bet = input()
            try:
                bet = int(bet)
            except ValueError:
                bet = None
                print("Bet must be a number")
                continue
            if MIN_BET <= bet <= MAX_BET:
                break
            elif bet >= MAX_BET:
                bet = MAX_BET
                break
            else:
                print(f"Please enter a bet between ${MIN_BET} and ${MAX_BET}.")
        return bet

    def clear_screen(self):
    # For Windows
         if os.name == 'nt':
             os.system('cls')
         # For Mac and Linux (os.name is 'posix')
         else:
              os.system('clear')

    def spin(self):
        s.player_broke()
        bet = self.get_bet()
        self.clear_screen() # clear the screen (nicer experience for the player)
        self.sessie_spins += 1
        if bet > self.balance:
            print("You don't have enough balance")
            return
        self.balance -= bet
        self.get_slot_machine_spin()
        self.get_winnings(bet)
        self.display_slot_machine()

        # ask if the player wants to use the multiplier
        if self.winnings > 0:
            print("Would you like to use the multiplier? (n to SKIP):", end=" ")
            use_multiplier = input()
            if use_multiplier.lower() != "n":
                self.use_multiplier()
                self.update_multiplier_counter()

            else:
                print("You chose not to use the multiplier")
        self.balance += self.winnings
        if self.balance <= 0:
            self.update_broke_counter()
            print(random.choice(quotes_loss))
        else:
            print(random.choice(quotes_win))
        self.update_spin_counter()
        self.update_highscore()
        self.save_player()
    

    def use_multiplier(self):
        # get the multiplier
        multiplier = self.get_multiplier()
        # multiply the winnings

        self.winnings *= multiplier
        self.winnings = int(self.winnings)
        self.print_multiplier_message(multiplier)
        print(f"Your winnings are now: {self.winnings}")

    def get_multiplier(self):
        # get the multiplier
        multiplier = random.choices(
            list(probabilities.keys()), weights=probabilities.values(), k=1
        )[0]
        return multiplier
    
    def print_multiplier_message(self, multiplier):
        if multiplier == 100:
            print("[bold magenta]You hit the jackpot! Your winnings are multiplied by 100![/bold magenta]")
        elif multiplier == 10:
            print("[bold magenta]You got a massive win! Your winnings are multiplied by 10![/bold magenta]")
        elif multiplier == 2:
            print("[bold magenta]You doubled your winnings with the multiplier![/bold magenta]")
        elif multiplier == 1.5:
            print("[bold magenta]You increased your winnings by 50% with the multiplier![/bold magenta]")
        elif multiplier > 1:
            print("[bold magenta]Profits on top of profits![/bold magenta]")
        else:
            print("[bold magenta]Better luck next time![/bold magenta]")

    def get_winnings(self, bet):
        wlines = self.get_wining_lines()
        winnings = 0
        # check each line if the symbols are the same
        for line in wlines:
            # get the symbol
            symbol = line[0]
            # get the value of the symbol
            value = self.symbol_values[symbol]
            winnings += value * bet

        for i in range(1, len(wlines)):
            winnings *= 1.2

        self.winnings = int(winnings)

    def get_wining_lines(self):
        lines = self.get_lines()
        l = []
        for line in lines:
            # get the symbol
            symbol = line[0]
            # check if all symbols are the same
            if all(symbol == s for s in line):
                l.append(line)

        return l

    def get_lines(self):
        lines = []
        # horizontal lines
        for i in range(self.rows):
            lines.append([self.slots[j][i] for j in range(self.cols)])
        # vertical lines
        for j in range(self.cols):
            lines.append([self.slots[j][i] for i in range(self.rows)])
        # diagonal lines
        lines.append([self.slots[i][i] for i in range(self.rows)])
        lines.append([self.slots[i][self.rows - i - 1] for i in range(self.rows)])
        return lines

    def print_stats(self):
        table = Table(title="Slot Machine Stats")

        # Add columns with the appropriate styles
        table.add_column("Statistic", justify="left", style="yellow", no_wrap=True)
        table.add_column("Value", justify="right", style="blue")

        # Add rows with the statistics and values
        table.add_row("Total spins", f"[blue]{self.spin_counter}[/blue]")
        table.add_row("Total multiplier uses", f"[blue]{self.multiplier_counter}[/blue]")
        table.add_row("Total times broke", f"[blue]{self.broke_counter}[/blue]")
        table.add_row("Highscore", f"[blue]{self.highscore}[/blue]")
        table.add_row("", "")  # Add an empty row for spacing
        table.add_row("Your balance", f"[bold green]{self.balance}[/bold green]")

        print(table)

    def welcome(self):
        print("\n   Welcome to the Slot Machine\n")
        self.print_stats()
        input("\n      Press enter to start")
        self.clear_screen()

# Main loop
s = SlotMachine()
s.welcome()
while 1:
    s.spin()
