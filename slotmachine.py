import random

MAX_LINES = 3
MAX_BET = 100
MIN_BET = 1

ROWS = 3

COLS = 3

symbol_count = {
    "@" : 5,
    "£" : 10,
    "$" : 20,
    "€" : 40,
    "§" : 25,
}

symbol_values = {
    "@" : 50,
    "£" : 10,
    "$" : 5,
    "€" : 2,
    "§" : 0,
}

# Define a list of quotes
quotes = [
    "I know you are thinking about quitting, but don't you want to double that number tho?",
    "You are on a roll! Keep going!",
    "You are so close to the jackpot, keep going!",
    "You are doing great! Keep going!",

]



def check_winnings(columns, lines, bet, values):
    winnings = 0
    winning_lines = []

    # Check horizontal winning lines
    for line in range(lines):
        symbol = columns[0][line]
        for column in columns:
            symbol_to_check = column[line]
            if symbol != symbol_to_check:
                break
        else:
            winnings += values[symbol] * bet
            winning_lines.append(line + 1)

    # Check vertical winning lines
    for column in columns:
        symbol = column[0]
        for symbol_to_check in column:
            if symbol != symbol_to_check:
                break
        else:
            winnings += values[symbol] * bet
            if winning_lines:
                winning_lines.append(winning_lines[-1] + 1)
            else:
                winning_lines.append(1)

    # Check diagonal winning lines
    if columns[0][0] == columns[1][1] == columns[2][2]:
        winnings += values[columns[0][0]] * bet
        winning_lines.append(4)
    if columns[0][2] == columns[1][1] == columns[2][0]:
        winnings += values[columns[0][2]] * bet
        winning_lines.append(5)

    return winnings, winning_lines

def multi_win(winnings, winning_lines):
    
    #Increase the winnings by 20% for each extra winning line beyond the first.
    
    if len(winning_lines) > 1:
        extra_lines = len(winning_lines) - 1
        extra_winnings = extra_lines * 0.2 * winnings
        return winnings + extra_winnings
    else:
        return winnings
    

def random_multi_winnings(winnings):
   
    #Apply a random multiplier to the winnings based on specified probabilities.
   
    # Define probabilities for each multiplier
    probabilities = {
        1000:   0.00001,     # 0.001% chance to multiply winnings by 1000
        100:    0.0001,      # 0.01% chance to multiply winnings by 100
        10:     0.001,       # 0.1% chance to multiply winnings by 10
        2:      0.01,        # 1% chance to double the winnings
        1.5:    0.05,        # 5% chance to add 50% of the winnings
        0:      0.82,        # 82% chance to lose the winnings
        -0.1:   0.10,        # 10% chance to lose 10% of the winnings
        -0.5:   0.04         # 4% chance to lose 50% of the winnings
    }

    # Choose a multiplier based on probabilities
    multiplier = random.choices(list(probabilities.keys()), list(probabilities.values()))[0]

    # Apply the multiplier to the winnings
    if multiplier == 10:
        return winnings * 10
    elif multiplier == 100:
        return winnings * 100
    elif multiplier == 2:
        return winnings * 2
    elif multiplier == 1.5:
        return winnings * 1.5
    elif multiplier == 1.3:
        return winnings * 1.3
    elif multiplier == -0.1:
        return winnings * 0.9
    elif multiplier == -0.5:
        return winnings * 0.5
    else:
        return 0  # If no multiplier is applied, user loses their winnings



def get_slot_machine_spin(rows, cols, symbols):
    all_symbols = []
    for symbol, symbol_count in symbols.items():
        for _ in range(symbol_count):
            all_symbols.append(symbol)

    columns = []    # define columns as an empty list
    for _ in range(cols):  # generte columns for the amount of COLS we have
        column = []
        current_symbols = all_symbols[:]  #copy the list with [:]
        for row in range(rows): #generate rows for the amount of ROWS we have
            value = random.choice(current_symbols)  #randomly choose a symbol from the current_symbols list
            current_symbols.remove(value)   #remove the symbol from the current_symbols list
            column.append(value)    #append the symbol to the column list
            
        columns.append(column)   
    return columns



slot_machine_part_1 = """                .-------.
            oO{-(\033[33m\033[5mMACHINE\033[0m)-}Oo
            .==============. """

slot_machine_part_2 = """            |--------------| __
            | €€€ :::::::: |(  )
            | £££ :::::::: | ||
            | $$$ :::::::: |_||"""
            
slot_machine_part_4 = """            |      __  === |
            |_____[__]_____|
           /################
          /##################
         |####################|"""

def slot_machine_part_3(winnings):
    # Convert winnings to a string
    winnings_str = str(winnings)
    # Calculate the length of the winnings string
    winnings_length = len(winnings_str)
    # Calculate the number of spaces needed to fill the remaining length
    spaces_needed = 15 - winnings_length - 1  # Subtract 1 for the space between winnings and the padding
    # If the winnings string is longer than 15 characters, truncate it
    if winnings_length > 15:
        return winnings_str[:15]
    # If the winnings string is shorter than 15 characters, pad it with spaces
    else:
        asci_winnings = " " * 12 +"|" + (spaces_needed - 1) * " " + "\033[33m" + winnings_str + "\033[0m" +" |--'"
        print(asci_winnings)
        return asci_winnings


def print_slot_machine(columns):
    print(slot_machine_part_1)
    slots = get_slot_machine_spin(ROWS, COLS, symbol_count)  # Generate slot machine spin
    winnings, winning_lines = check_winnings(slots, MAX_LINES, MAX_BET, symbol_values)  # Calculate winnings
    for row in range(len(columns[0])):  # For each row in the first column
        print(" " * 12, end="| ")  # Print 12 spaces and "|" at the beginning of each row
        for i, column in enumerate(columns):  # For each column in the columns list
            if i != len(columns) - 1:  # If the column is not the last column
                print(" " + column[row], end=" | ")  # Check if it's not the last index to print "|"
            else:
                print(column[row] + " ", end=" | ")  # If it's the last index, print "|" at the end of the row with additional space
        print()  # Print a new line
      




    
def deposit():
    while True:
        amount = input("Enter the amount you want to deposit: $")
        if amount.isdigit():
            amount = int(amount)
            if amount > 1000:
                print("Don't get over your head.")
                amount = 1000
                break
                
            elif amount <= 0:
                print("Please enter a positive amount.")

            else:
                break

        else:
            print("Please enter a valid amount.")
    return amount


def get_number_of_lines():
   # while True:
   #     lines = input("How many lines do you want to bet on? (1-" + str(MAX_LINES) + "? ")
    #    if lines.isdigit():
   #         lines = int(lines)
   #         if 1 <= lines <= MAX_LINES:
   #             break
   #         else:
    #            print("Please enter a number between 1 and 3.")
   #     else:
   #         print("Please enter a valid number.")
    lines = MAX_LINES
    return lines


def get_bet():
    while True:
        bet = input(f"How much do you want to bet? (${MIN_BET} and ${MAX_BET})? $")
        if bet.isdigit():
            bet = int(bet)
            if MIN_BET <= bet <= MAX_BET:
                break
            else:
                print(f"Please enter a bet between ${MIN_BET} and ${MAX_BET}.")
        else:
            print("Please enter a valid bet.")
    return bet


def spin(balance):
    lines = get_number_of_lines()
    while True:
        bet = get_bet()
        if bet > balance:
            print(f"You don't have enough money to make that bet. Your balance is ${balance}.")
        else:
            break

    print(f"You are betting ${bet} ")

    slots = get_slot_machine_spin(ROWS, COLS, symbol_count)

    winnings, winning_lines = check_winnings(slots, lines, bet, symbol_values)

    print_slot_machine(slots)
    print(slot_machine_part_2)  
    slot_machine_part_3(winnings)
    print(slot_machine_part_4)
    print()
    
    print("You won \033[33m$" + str(winnings) + "\033[0m")
    print("You won on line(s):", *winning_lines) 

    # Check if there are winnings
    if winnings > 0:
        # Ask the user if they want to apply a random multiplier
        choice = input("Do you want to use a random multiplier on your winnings? (Y/N): ").upper()
        if choice == "Y":
            new_winnings = random_multi_winnings(winnings)
            if new_winnings > 0:
                print("Adjusted winnings: \033[33m$" + str(new_winnings) + "\033[0m")
            else:
                print("Adjusted winnings: \033[33m$" + str(new_winnings) + "\033[0m")
        else:
            new_winnings = winnings
    else:
        new_winnings = 0

    return new_winnings - bet



def broke(balance):
    if balance == 0:
        print("\033[33mTime to go home fren\033[0m")
        print("We'll get that money anyway somehow")
        return True



def main():
    print("Welcome to the slot machine!")
    balance = deposit()
    while True:
        print("Your balance is \033[32m$" + str(balance) + "\033[0m")
        if broke(balance):  
            break
        answer = input("Press enter to play (Q to quit): ")
        if answer.lower() == "q":
            print(f"You checked out with ${balance}. Thanks for playing!")
            break
        balance += spin(balance)


main()

