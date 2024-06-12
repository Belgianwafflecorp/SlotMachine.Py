import sys
from rich import print
from rich.table import Table
from slotmachine import DataBase
import settings


class PlayerControls:
    def __init__(self, slotmachine=None | object):
        self.slotmachine = slotmachine  # Assuming you have a slot machine object
        self.first_time = True
        self.db = DataBase()
        self.settings = settings
        self.dealer = slotmachine.dealer

    def print_help(self):
        self.slotmachine.clear_screen()
        t = Table(title="Controls")
        t.add_column("Control", style='cyan')
        t.add_column("Description", style='cyan')
        t.add_row("-allin", "Exactly what you think, going all in!")
        t.add_row("-dealer", 'Ask the dealer to increase your max bet.')
        t.add_row("-delete", 'Delete player stats.')
        t.add_row("-help", 'Show available controls and their descriptions.')
        t.add_row("-quit", 'Quit the game.')
        t.add_row("-stats", 'Show your statistics.')
        t.add_row("-win", 'Show possible winnings.')
        print(t)
        input("Press enter to continue...")
        self.slotmachine.clear_screen()

    def quit(self):
        self.slotmachine.clear_screen()
        self.slotmachine.save_database()
        print(f"\nYou checked out with ${self.db.get_column('balance')}")
        print("\nDon't forget to come back and try your luck again!\n")
        sys.exit()  # Quit the application

    def stats(self):
        self.slotmachine.clear_screen()
        self.slotmachine.print_stats()
        input("Press enter to continue...")
        self.slotmachine.clear_screen()

    def allin(self):
        choice = input("Are you sure you want to go all in? (y/n): ")
        if choice.lower() != "n":
            allin_bet = self.db.get_column('balance')
            real_max_bet = self.db.get_column('max_bet')
            self.db.update_column('max_bet', allin_bet)
            self.slotmachine.allin(allin_bet)
            self.db.update_column('max_bet', real_max_bet)


    def spin(self):
        print("Spinning the slot machine!")
        self.slotmachine.spin()

    def possible_winnings(self):
        self.slotmachine.clear_screen()
        t = Table(title="Possible Winnings")
        t.add_column("Symbol", style='cyan')
        t.add_column("Multiplier", style='cyan')

        for symbol, multiplier in self.settings.symbol_values.items():
            t.add_row(symbol*3, str(multiplier))

        print(t)
        print("\n[bold yellow]Having more than one winning line will give combo bonuses![/bold yellow]")
        print("[bold yellow]For each combo, you will get an extra 20% of the total winnings![/bold yellow]\n")
        print(":potato: lines will add to the bonus combo lines.\n")
        input("Press enter to continue...")
        self.slotmachine.clear_screen()

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
            case "-win":
                self.possible_winnings()
            case "-dealer":
                self.dealer.player_ask_dealer()
            case "-delete":
                self.slotmachine.delete_player()
            case "":
                self.slotmachine.spin(self.db.get_column("previous_bet"))
            case _:
                # check if the command is a number
                try:
                    bet = int(command)
                    if bet < 0:
                        self.slotmachine.clear_screen() 
                        print("Invalid command. Please try again.\n")
                        return
                    # check if the bet is higher than the max or lower than the min
                    if (
                        bet > self.db.get_column("max_bet")
                        or bet < self.slotmachine.min_bet
                    ):
                        self.slotmachine.clear_screen()
                        print("Invalid bet. Please try again.\n")
                        return
                    self.slotmachine.spin(bet)
                except ValueError:
                    self.slotmachine.clear_screen()
                    print("Invalid command. Please try again.\n")

    def get_input(self):
        if self.first_time:
            #self.print_help()
            self.first_time = False
        self.slotmachine.ask_for_command_or_new_bet()
        command = input().strip().lower()
        self.get_command(command)
