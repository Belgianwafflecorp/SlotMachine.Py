
MAX_LINES = 3
MIN_BET = 1

ROWS = 3
COLS = 3

# symbol_count = {
#     "🤑": 1,
#     ":apple:": 5,
#     ":banana:": 10,
#     ":watermelon:": 20,
#     ":cherries:": 40,
#     ":potato:": 25,
# }
symbol_count = { # debugging making the cherries more common
    "🤑" : 1,
    ":apple:" : 5,
    ":banana:" : 10,
    ":watermelon:" : 20,
    ":cherries:" : 100000,
    ":potato:" : 25,
}


symbol_values = {
    "🤑": 1000,
    ":apple:": 10,
    ":banana:": 5,
    ":watermelon:": 3,
    ":cherries:": 2,
    ":potato:": 0,
}

# Define the directory for JSON files
JSON_DIR = "PLAYER_DATA"


slot_machine_part_1 = """               .---------.
            oO{-([yellow]MACHINE[/yellow])-}Oo
            .===============. """

# part2 is in the slotmachine.py file

slot_machine_part_3 = """            |---------------| __
            | [purple]€€€[/purple] ::::::::: |(  )
            | [red]£££[/red] ::::::::: | ||
            | [green]$$$[/green] ::::::::: |_||"""

slot_machine_part_4 = """            |      ___  === |
            |_____[___]_____|
           [white]/[/white]#################\\
          [white]/[white]###################\\
         |#####################|"""

# Define probabilities for each multiplier
probabilities = {
    1000: 0.00001,  # 0.001% chance to multiply winnings by 1000
    100: 0.0001,  # 0.01% chance to multiply winnings by 100
    10: 0.001,  # 0.1% chance to multiply winnings by 10
    2: 0.01,  # 1% chance to double the winnings
    1.5: 0.05,  # 5% chance to add 50% of the winnings
    1.3: 0.10,  # 10% chance to add 30% of the winnings
    1.1: 0.22,  # 22% chance to add 10% of the winnings
    0: 0.50,  # 50% chance to lose the winnings
    0.9: 0.10,  # 10% chance to lose 10% of the winnings
    0.5: 0.04,  # 4% chance to lose 50% of the winnings
}


