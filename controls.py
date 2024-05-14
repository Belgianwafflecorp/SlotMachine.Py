import sys
import JsonFileManager as json_fm  


class PlayerControls:
    def __init__(self, balance, json_fm_instance: json_fm.JsonFileManager, spin_counter):
        self.balance = balance
        self.json_fm_instance = json_fm_instance
        self.spin_counter = spin_counter
        

    def print_help(self):
        print("\n\t Available controls:\n")
        print(" -help   : Show available controls and their descriptions.")
        print(" -quit   : Quit the game.")
        print(" -stats  : Show your statistics.")
        print(" -dealer : To ask the dealer for higher max bets.")
        print(" -allin  : Exactly what you think, going all in!\n")

    def control_check(self, user_input, start_spin_count):
        if user_input == "-help": 
            self.print_help()
        elif user_input == "-quit": 
            self.quit(start_spin_count, self.spin_counter, self.balance)
        elif user_input == "-stats":
            self.print_stats()
        elif user_input == "-dealer":
            self.dealer()
        elif user_input == "-allin":
            self.allin()
        else:
            return 

    def dealer(self):
        dealer_level = self.json_fm_instance.load_dealer_lv()

        if self.balance < 10000:
            print("\nYou need at least 10k balance to increase your maximum bets.\n")
        elif self.balance >= 10000 and dealer_level == 0:
            print("\nYour maximum bets are now increased to 1000.\n")
            self.json_fm_instance.update_dealer_lv_up()
        elif self.balance >= 50000 and dealer_level == 1:
            print("\nYour maximum bets are now increased to 5000.\n")
            self.json_fm_instance.update_dealer_lv_up()
        elif self.balance >= 100000 and dealer_level == 2:
            print("\nYour maximum bets are now increased to 10000.\n")
            self.json_fm_instance.update_dealer_lv_up()
        else:
            print("\nYou've reached the maximum dealer level. \n")
            

        

    def quit(self, balance, spin_counter, start_spin_count):
        session_spins = spin_counter - start_spin_count
        print(f"\nYou made \033[34m{session_spins}\033[0m spins this session.")
        #check_session_spins(session_spins) # personal message
        print(f"You checked out with \033[32m${balance}\033[0m. Thanks for playing!\n")
        self.json_fm_instance.save_balance(balance)
        sys.exit() 

    def print_stats(self):
        print("Player statistics:")
        print(f"Balance: ${self.balance}")
        

    def allin(self):
        print("Betting all your balance!")
        return self.balance



