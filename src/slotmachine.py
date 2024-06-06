import os
import time
import random
from quotes import quotes_win, quotes_loss
from database import DataBase
from ascii_art import Ascii
from settings import (
    ROWS,
    COLS,
    MIN_BET,
    symbol_count,
    symbol_values,
    slot_machine_part_1,
    slot_machine_part_3,
    slot_machine_part_4,
    probabilities,
)
from rich import print
from rich.table import Table
from dealer import Dealer


class SlotMachine:
    def __init__(self) -> None:
        self.player_db = DataBase() #instance of the database class
        self.ascii = Ascii()
        self.rows = ROWS
        self.cols = COLS
        self.sessie_spins = 0
        self.symbol_count = symbol_count  # number of each symbol per slot machine
        self.symbol_values = symbol_values  # value of each symbol
        self.slot_machine_part_1 = slot_machine_part_1
        self.slot_machine_part_3 = slot_machine_part_3
        self.slot_machine_part_4 = slot_machine_part_4
        self.min_bet = MIN_BET
        self.dealer = Dealer(self) #instance of slotmachine to dealer class 
        try:
            self.load_database()
        except:
            self.default_values()
            self.save_database()
            self.load_database()

    def default_values(self):
        self.balance = 0
        self.highscore = 0
        self.spin_counter = 0
        self.multiplier_counter = 0
        self.broke_counter = 0
        self.best_spin = 0
        self.jackpot_multiplier_counter = 0
        self.previous_bet = 1
        self.player_db.update_column("max_bet", 100)

    def delete_player(self):
        print("\nAre you sure you want to delete your player stats? (y/n):", end=' ')
        choice = input().lower()
        if choice == "y":
            self.default_values()
            self.save_database()
            self.clear_screen()
        else:
            self.clear_screen()
            print("\nPlayer stats were not deleted.\n")

    def load_database(self):
        self.balance = self.player_db.get_column('balance')
        self.highscore = self.player_db.get_column('highscore')
        self.spin_counter = self.player_db.get_column('spin_count')
        self.multiplier_counter = self.player_db.get_column('multiplier_count')
        self.broke_counter = self.player_db.get_column('broke_counter')
        self.best_spin = self.player_db.get_column('best_spin')
        self.jackpot_multiplier_counter = self.player_db.get_column(
            'jackpot_multiplier_counter'
        )
        self.previous_bet = self.player_db.get_column('previous_bet')
        self.max_bet = self.player_db.get_column('max_bet')

    def save_database(self):
        self.player_db.update_column("balance", self.balance)
        self.player_db.update_column("highscore", self.highscore)
        self.player_db.update_column("spin_count", self.spin_counter)
        self.player_db.update_column("multiplier_count", self.multiplier_counter)
        self.player_db.update_column("broke_counter", self.broke_counter)
        self.player_db.update_column("best_spin", self.best_spin)
        self.player_db.update_column("jackpot_multiplier_counter", self.jackpot_multiplier_counter)
        self.player_db.update_column("previous_bet", self.previous_bet)

    def update_spin_counter(self):
        self.spin_counter += 1
        self.player_db.update_column("spin_count", self.spin_counter)

    def update_multiplier_counter(self):
        self.multiplier_counter += 1
        self.player_db.update_column("multiplier_count", self.multiplier_counter)

    def check_highscore(self):
        self.highscore = max(self.highscore, self.balance)
        self.save_database()

    def update_broke_counter(self):
        self.broke_counter += 1
        self.player_db.update_column("broke_counter", self.broke_counter)

    def check_player_broke(self):
        if self.balance < 1:
            self.update_broke_counter()
            self.dealer.default_max_bet()
            self.clear_screen()
            print("\nsorry, you are out of chips")
            print("Make a new deposit to continue playing")
            self.deposit()

    def deposit(self):
        while True:
            amount = input("Enter the amount you want to deposit: $")
            if amount.isdigit():
                amount = int(amount)
                match amount:
                    case 1069:
                        self.clear_screen()
                        print("\nCheeky basterd. I'll let that one slide.\n")
                        amount = 1069
                        break
                    case _ if amount > 1000:
                        self.clear_screen()
                        print("Don't get over your head. You get $1000 to start with.")
                        amount = 1000
                        break
                    case _ if amount <= 0:
                        self.clear_screen()
                        print("Please enter a positive amount.")
                        break
                    case _:
                        break
            else:
                self.clear_screen()
                print("Please enter a valid amount.")
        self.balance += amount
        self.save_database()

    def check_best_spin(self):
        self.best_spin = max(self.best_spin, self.winnings)
        self.save_database()

    def slot_machine_part_2(self):
        # display the row of self.slots vertically so row 1 is column 1
        # double
        s = ""
        for i in range(self.rows):
            s += " " * 12 + "|" + " ║"
            for j in range(self.cols):
                s += (
                    self.slots[j][i] + " ║"
                    if j != self.cols - 1
                    else self.slots[j][i] + " ║"
                )

            s += " |\n" if i != self.rows - 1 else " |"
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
        self.slots = [
            random.choices(
                list(self.symbol_count.keys()),
                k=self.rows,
                weights=self.symbol_count.values(),
            )
            for _ in range(self.cols)
        ]

    def ask_for_command_or_new_bet(self):
        print(
            f"Balance: ${self.balance}\n"
            f"Enter a command (-help)\n"
            f"Press enter to bet ({self.previous_bet})\n"
            f"Place a bet between {self.min_bet} and {self.player_db.get_column('max_bet')}:",
            end=" ",
            )
        
    def get_bet(self):
        bet = None
        while bet is None:
            # show balance
            self.ask_for_command_or_new_bet()
            bet = input()
            if bet.isdigit():
                bet = int(bet)
                if bet < self.min_bet or bet > self.player_db.get_column('max_bet'):
                    print(f"Please enter a bet between ${self.min_bet} and ${self.player_db.get_column('max_bet')}.")
                    bet = None
                    continue
                break
            elif bet == "":
                bet = self.previous_bet
                break
            else:
                print("Please enter a valid number.")
                bet = None
                continue

        self.previous_bet = bet
        self.player_db.update_column("previous_bet", bet)
        return bet

    def clear_screen(self):
        # For Windows
        if os.name == "nt":
            os.system("cls")
        # For Mac and Linux (os.name is 'posix')
        else:
            os.system("clear")

    def spin_time(self):
        print("\n\n\n\n\n\n\t   [bold yellow]Spinning the wheels...[/bold yellow]")
        time.sleep(0.75)
        self.clear_screen()

    def spin(self, bet=None):
        self.check_player_broke()
        if bet is None:
            bet = self.get_bet()
        elif bet < self.min_bet or bet > self.max_bet:
            print(f"Please enter a bet between ${self.min_bet} and ${self.player_db.get_column('max_bet')}.")
            return
        else:
            self.previous_bet = bet
            self.player_db.update_column('previous_bet', bet)
        self.clear_screen()  # clear the screen (nicer experience for the player)
        if bet > self.balance:
            print("You don't have enough balance")
            return
        self.balance -= bet
        self.spin_time()
        self.get_slot_machine_spin()
        self.get_winnings(bet)
        self.display_slot_machine()
        self.check_best_spin()
        self.update_spin_counter()

        # ask if the player wants to use the multiplier
        if self.winnings > 0:
            print("Would you like to use the multiplier? (n to SKIP):", end=' ')
            use_multiplier = input()
            if use_multiplier.lower() != "n":
                self.use_multiplier()

            else:
                print("You chose not to use the multiplier")
        self.balance += self.winnings
        if self.balance <= 0:
            self.check_player_broke()
            print(f"[bold yellow]{random.choice(quotes_loss)}[/bold yellow]")
        elif self.winnings == 0:
            print(f"[bold yellow]{random.choice(quotes_loss)}[/bold yellow]")
        else:
            print(f"[bold yellow]{random.choice(quotes_win)}[/bold yellow]")
        self.check_highscore()
        self.save_database()
        return bet

    def use_multiplier(self):
        # get the multiplier
        multiplier = self.get_multiplier()
        self.update_multiplier_counter()
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
        match multiplier:
            case 1000:
                print(
                    "[bold magenta]You hit the jackpot! Your winnings are multiplied by 1000![/bold magenta]"
                )
                self.ascii.jackpot()
                self.player_db.increment_column('jackpot_multiplier_counter')
            case 100:
                print(
                    "[bold magenta]You got a huge win! Your winnings are multiplied by 100![/bold magenta]"
                )
            case 10:
                print(
                    "[bold magenta]You got a massive win! Your winnings are multiplied by 10![/bold magenta]"
                )
            case 2:
                print(
                    "[bold magenta]You doubled your winnings with the multiplier![/bold magenta]"
                )
            case 1.5:
                print(
                    "[bold magenta]You increased your winnings by 50% with the multiplier![/bold magenta]"
                )
            case _ if multiplier > 1:
                print("[bold magenta]Profits on top of profits![/bold magenta]")
            case _:
                print(
                    "[bold magenta]Better luck next time![/bold magenta]",
                )

    def get_winnings(self, bet):
        winnings = 0
        # check each line if the symbols are the same
        winnings = sum(
            self.symbol_values[line[0]] * bet for line in self.get_wining_lines()
        )
        for _ in range(1, len(self.get_wining_lines())):
            winnings *= 1.2

        self.winnings = int(winnings)

    def get_wining_lines(self):
        return [
            line
            for line in self.get_lines()
            if all(symbol == line[0] for symbol in line)
        ]

    def get_lines(self):
        lines = (
            [[self.slots[j][i] for j in range(self.cols)] for i in range(self.rows)]
            + [[self.slots[j][i] for i in range(self.rows)] for j in range(self.cols)]
            + [[self.slots[i][i] for i in range(self.rows)]]
            + [[self.slots[i][self.rows - i - 1] for i in range(self.rows)]]
        )
        return lines

    def print_stats(self):
        table = Table(title="Slot Machine Stats")
        # Add columns with the appropriate styles
        table.add_column("Statistic", justify="left", style="yellow", no_wrap=True)
        table.add_column("Value", justify="right", style="blue")
        # Add rows with the statistics and values
        table.add_row("Total spins", f"[blue]{self.spin_counter}[/blue]")
        table.add_row("Best spin", f"[blue]{self.best_spin}[/blue]")
        table.add_row(
            "Total multiplier uses", f"[blue]{self.multiplier_counter}[/blue]"
        )
        table.add_row(
            "Multiplier jackpots", f"[blue]{self.jackpot_multiplier_counter}[/blue]"
        )
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

    def allin_shout(self):
        self.clear_screen()
        print("\n\n\n\n\n\n\t   [bold yellow]LETS[/bold yellow]")
        time.sleep(1)
        self.clear_screen()
        print("\n\n\n\n\n\n\t   [bold yellow]GET[/bold yellow]")
        time.sleep(1)
        self.clear_screen()
        print("\n\n\n\n\n\n\t   [bold yellow]READY[/bold yellow]")
        time.sleep(1)
        self.clear_screen()
        print("\n\n\n\n\n\n\t   [bold yellow]TOO[/bold yellow]")
        time.sleep(1)
        self.clear_screen()
        print("\n\n\n\n\n\n\t   [bold yellow]RUMBLEEEEE !!![/bold yellow]")
        time.sleep(1)
        self.clear_screen()

    def allin(self, bet): 
        self.allin_shout()
        self.clear_screen()  
        self.balance -= bet
        self.get_slot_machine_spin()
        self.get_winnings(bet)
        self.display_slot_machine()
        self.check_best_spin()
        self.update_spin_counter()

        # ask if the player wants to use the multiplier
        if self.winnings > 0:
            print("Would you like to use the multiplier? (n to SKIP):", end=' ')
            use_multiplier = input()
            if use_multiplier.lower() != "n":
                self.use_multiplier()

            else:
                print("You chose not to use the multiplier")
        self.balance += self.winnings
        if self.balance > 0:
            print(f"[bold yellow]{random.choice(quotes_win)}[/bold yellow]")
        else :
            print("[bold yellow]Please don't tell use you borrowed that money.[/bold yellow]\n")
            print("You can get that back if you continue playing.")
        
        self.check_highscore()
        self.save_database()
        return bet
