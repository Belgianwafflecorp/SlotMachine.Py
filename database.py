import sqlite3
import os


class DataBase:
    """
    This class is responsible for the database connection and the cursor.

    the data base is called database.db
    and will consist 1 table with only 1 row and 9 column\
    
    the columns are:
    1. balance INTEGER
    2. highscore INTEGER
    3. spin_count INTEGER
    4. multiplier_count INTEGER
    5. broke_counter INTEGER
    6. best_spin INTEGER
    7. jackpot_multiplier_counter INTEGER
    8. previous_bet INTEGER
    9. max_bet INTEGER
    """

    def __init__(
        self,
    ):
        self.open()

    def open(self):
        self.conn = sqlite3.connect("database.db")
        self.cursor = self.conn.cursor()
        self.__create_table()

    # with default values
    def __create_table(self):
        self.cursor.execute(
            "CREATE TABLE IF NOT EXISTS data(balance INTEGER, highscore INTEGER, spin_count INTEGER, multiplier_count INTEGER, broke_counter INTEGER, best_spin INTEGER, jackpot_multiplier_counter INTEGER, previous_bet INTEGER, max_bet INTEGER default 100)"
        )
        self.conn.commit()

    def insert_data(
        self,
        balence,
        highscore,
        spin_count,
        multiplier_count,
        broke_counter,
        best_spin,
        jackpot_multiplier_counter,
        previous_bet,
        max_bet,
    ):
        self.cursor.execute(
            "INSERT INTO data VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (
                balence,
                highscore,
                spin_count,
                multiplier_count,
                broke_counter,
                best_spin,
                jackpot_multiplier_counter,
                previous_bet,
                max_bet,
            ),
        )
        self.conn.commit()

    # show all data
    def get_data(self):
        self.cursor.execute("SELECT * FROM data")
        return self.cursor.fetchall()

    # print the column data
    def get_column(self, column):  # show specific column
        self.cursor.execute(f"SELECT {column} FROM data")
        return self.cursor.fetchone()[0]

    def add_column(self, column, data):  # add a new column
        self.cursor.execute(f"ALTER TABLE data ADD COLUMN {column} {data}")
        self.conn.commit()

    # update all data at once
    def update_data(
        self,
        balance,
        highscore,
        spin_count,
        multiplier_count,
        broke_counter,
        best_spin,
        jackpot_multiplier_counter,
        previous_bet,
        max_bet,
    ):
        if not self.get_data():
            self.insert_data(
                balance,
                highscore,
                spin_count,
                multiplier_count,
                broke_counter,
                best_spin,
                jackpot_multiplier_counter,
                previous_bet,
                max_bet,
            )
            return
        self.cursor.execute(
            "UPDATE data SET balance = ?, highscore = ?, spin_count = ?, multiplier_count = ?,"
            + " broke_counter = ?, best_spin = ?, jackpot_multiplier_counter = ?, previous_bet = ?, max_bet = ?",
            (
                balance,
                highscore,
                spin_count,
                multiplier_count,
                broke_counter,
                best_spin,
                jackpot_multiplier_counter,
                previous_bet,
                max_bet,
            ),
        )
        self.conn.commit()

    def insert_column(self, column, value):
        self.cursor.execute(f"INSERT INTO data({column}) VALUES(?)", (value,))
        self.conn.commit()

    def get_column_names(self):
        self.cursor.execute("PRAGMA table_info(data)")
        return self.cursor.fetchall()

    # update a specific column or create a new one if not exist
    def update_column(self, column, value):
        if column not in [i[1] for i in self.get_column_names()]:
            # alter
            self.cursor.execute(f"ALTER TABLE data ADD COLUMN {column} INTEGER")
            self.conn.commit()
        if not self.get_data():
            self.insert_column(column, value)
            return

        self.cursor.execute(f"UPDATE data SET {column} = ?", (value,))
        self.conn.commit()

    # increment a specific column
    def increment_column(self, column):
        if not self.get_data():
            self.insert_column(column, 1)
            return
        self.cursor.execute(f"UPDATE data SET {column} = {column} + 1")
        self.conn.commit()

    # decrement a specific column
    def decrement_column(self, column):
        if not self.get_data():
            self.insert_column(column, 0)
            return
        self.cursor.execute(f"UPDATE data SET {column} = {column} - 1")
        self.conn.commit()

    def close(self):
        self.conn.close()

    def __del__(self):
        self.close()

    # delete all data
    def delete_all_player_data(self):
        self.cursor.execute("DELETE FROM data")
        self.conn.commit()

    # delete the old jsons
    def delete_player_data_folder():
        if os.path.exists("PLAYER_DATA"):
            os.rmdir("PLAYER_DATA")
