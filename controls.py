import sys
import JsonFileManager as json_fm  


class PlayerControls:
    def __init__(self, balance, spin_counter, start_spin_count):
        self.balance = balance
        self.spin_counter = spin_counter
        self.start_spin_count = start_spin_count

    def print_help(self):
        print("\n\tAvailable controls:")
        print(" -help   : Show available controls and their descriptions.")
        print(" -quit   : Quit the game.")
        print(" -stats  : Show your statistics.")
        print(" -dealer : To ask the dealer for higher max bets.")
        print(" -allin  : Exactly what you think, going all in!")

    def quit(self):
            sys.exit()  # Quit the application

    def stats(self):
        print("Player statistics:")
        print(f"Balance: ${self.balance}")

    def allin(self):
        print("Betting all your balance!")
        # Assuming you have a betting function where you can specify the bet
        # Here, we're setting the bet as the current balance
        # You may need to adapt this based on your actual betting function
        return self.balance


def main():
    # Initialize player with some initial balance (you can load this from JsonFileManager)
    balance = json_fm.load_balance() or 1000  # Default to $1000 if balance file doesn't exist
    player = PlayerControls(balance)

    while True:
        command = input("Enter a command: ").strip().lower()

        if command == "-help":
            player.help()
        elif command == "-quit":
            player.quit()
        elif command == "-stats":
            player.stats()
        elif command == "-allin":
            bet = player.allin()
            # Now you can use the returned bet value for your betting logic
            # For example:
            # perform_bet(bet)
        else:
            print("Invalid command. Type '-help' for available controls.")

if __name__ == "__main__":
    main()
