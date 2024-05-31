import sys
from rich import print
from rich.table import Table
from slotmachine import DataBase


class PlayerControls:
    def __init__(self, slotmachine=None | object):
        self.slotmachine = slotmachine  # Assuming you have a slot machine object
        self.first_time = True
        self.db = DataBase()

    def print_help(self):
        self.slotmachine.clear_screen()
        t = Table(title="Controls")
        t.add_column("Control", style="cyan")
        t.add_column("Description", style="cyan")
        t.add_row("-help", "Show available controls and their descriptions.")
        t.add_row("-quit", "Quit the game.")
        t.add_row("-stats", "Show your statistics.")
        # t.add_row("-allin", "Exactly what you think, going all in!")
        print(t)

    def quit(self):
        self.slotmachine.clear_screen()
        self.slotmachine.save_database()
        print(f"\nYou checked out with ${self.db.get_column('balance')}")
        print("\nDon't forget to come back and try your luck again!\n")
        sys.exit()  # Quit the application

    def stats(self):
        self.slotmachine.clear_screen()
        self.slotmachine.print_stats()

    def allin(self):
        # print("Betting all your balance!")
        # self.slotmachine.allin()
        ...

    def spin(self):
        print("Spinning the slot machine!")
        self.slotmachine.spin()

    def get_command(self, command):
        match command:
            case "-help":
                self.print_help()
            case "-quit":
                self.quit()
            case "-stats":
                self.stats()
            case "-allin":
                self.allin()
            case "":
                self.slotmachine.spin(self.slotmachine.db.get_column("previous_bet"))
            case _:
                # check if the command is a number
                try:
                    bet = int(command)
                    if bet < 0:
                        print("Invalid command. Please try again.")
                        return
                    # check if the bet is higher than the max or lower than the min
                    if (
                        bet > self.slotmachine.db.get_column("max_bet")
                        or bet < self.slotmachine.min_bet
                    ):
                        print("Invalid bet. Please try again.")
                        return
                    self.slotmachine.spin(bet)
                except ValueError:
                    print("Invalid command. Please try again.")

    def get_input(self):
        if self.first_time:
            self.print_help()
            self.first_time = False
        self.slotmachine.ask_for_command_or_new_bet()
        command = input().strip().lower()
        self.get_command(command)
