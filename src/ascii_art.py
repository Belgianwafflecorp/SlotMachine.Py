from rich import print

class Ascii:

    ascii_jackpot = """[bold magenta]
   _    __    __    _     ___   ___  _____
  | |  / /\\  / /`  | |_/ | |_) / / \\  | | 
\\_|_| /_/--\\ \\_\\_, |_| \\ |_|   \\_\\_/  |_| 
[/bold magenta]
"""


    def jackpot(self):
        print(self.ascii_jackpot)
        print("[bold magenta]Congratulations! You hit the JACKPOT![/bold magenta]") 

    
