from slotmachine import SlotMachine
from controls import PlayerControls

# winget install --id Microsoft.WindowsTerminal -e
# enter the following command in the terminal to install the windows terminal
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
