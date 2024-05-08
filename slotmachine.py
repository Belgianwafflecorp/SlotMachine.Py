import random

MAX_LINES = 3
MAX_BET = 100
MIN_BET = 1

ROWS = 3

COLS = 3

symbol_count = {
    "A" : 5,
    "B" : 10,
    "C" : 20,
    "D" : 40,
}

symbol_values = {
    "A" : 100,
    "B" : 10,
    "C" : 5,
    "D" : 2,
}

def check_winnings(columns, lines, bet, values):
    winnings = 0
    winning_lines = []
    for line in range(lines):
        symbol = columns[0][line]
        for column in columns:
            symbol_to_check = column[line]
            if symbol != symbol_to_check:
                break
        else:
            winnings += values[symbol] * bet
            winning_lines.append(line + 1)

    return winnings, winning_lines


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


def print_slot_machine(columns):
    for row in range(len(columns[0])): #for each row in the first column
        for i, column in enumerate(columns): #for each column in the columns list
            if i != len(columns) - 1:   #if the column is not the last column
                print(column[row],end=" | ") # check if its not the last index to print "|"
            else:
                print(column[row],end="") #if its the last index, print nothing

        print() #print a new line


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
        #total_bet = bet * lines
        if bet > balance:
            print(f"You don't have enough money to make that bet. Your balance is ${balance}.")
        else:
            break

    print(f"You are betting ${bet} on {lines} lines. Total bet: ${bet}")

    slots = get_slot_machine_spin(ROWS, COLS, symbol_count)
    print_slot_machine(slots)
    winnings, winning_lines = check_winnings(slots, lines, bet, symbol_values)
    print(f"You won ${winnings}")
    print(f"You won on line(s):", *winning_lines) 
    return winnings - bet


def broke(balance):
    if balance == 0:
        print("Time to go home fren.")
        return True


def main():
    print("Welcome to the slot machine!")
    balance = deposit()
    while True:
        print(f"Your balance is ${balance}.")
        if broke(balance):
            break
        answer = input("Press enter to play (Q to quit): ")
        if answer.lower() == "q":
            print(f"You checked out with ${balance}. Thanks for playing!")
            break
        balance += spin(balance)
    

main()

