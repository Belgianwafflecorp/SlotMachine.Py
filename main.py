from slotmachine import SlotMachine
from controls import PlayerControls

# winget install --id Microsoft.WindowsTerminal -e
# Windows Terminal is not required to run the game, but it is recommended for a better experience.
import os
os.system("winget install --id Microsoft.WindowsTerminal -e")


def main():
    slot_machine = SlotMachine()
    slot_machine.clear_screen()
    slot_machine.welcome()
    controls = PlayerControls(slot_machine)
    while True:
        controls.get_input()


if __name__ == "__main__":
    main()
