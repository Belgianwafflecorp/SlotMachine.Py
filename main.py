from slotmachine import SlotMachine
from controls import PlayerControls

# winget install --id Microsoft.WindowsTerminal -e
# Windows Terminal is not required to run the game, but it is recommended for a better experience.
import os
os.system("winget install --id Microsoft.WindowsTerminal -e")


def main():
    slotmachine = SlotMachine()
    slotmachine.load_database()
    slotmachine.clear_screen()
    slotmachine.welcome()
    if slotmachine.balance == 0:
        slotmachine.deposit()
    controls = PlayerControls(slotmachine)
    while True:
        slotmachine.check_player_broke()
        controls.get_input()
        slotmachine.save_database()

if __name__ == "__main__":
    main()
