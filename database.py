import sqlite3
import os
import JsonFileManager
json_fm = JsonFileManager.JsonFileManager("PLAYER_DATA")

class DataBase:
    """
    This class is responsible for the database connection and the cursor.

    the data base is called database.db
    and will consist 1 table with only 1 row and 7 column\
    
    the columns are:
    1. balance INTEGER
    2. highscore INTEGER
    3. spin_count INTEGER
    4. multiplier_count INTEGER
    5. broke_counter INTEGER
    6. best_spin INTEGER
    7. jackpot_multiplier_counter INTEGER
    """
    def __init__(self,):
        self.open()

    def open(self):
        self.conn = sqlite3.connect("database.db")
        self.cursor = self.conn.cursor()
        self.__create_table()

    def __create_table(self):
        self.cursor.execute("CREATE TABLE IF NOT EXISTS data(balance INTEGER, highscore INTEGER, spin_count INTEGER, multiplier_count INTEGER, broke_counter INTEGER, best_spin INTEGER, jackpot_multiplier_counter INTEGER)")
        self.conn.commit()

    def insert_data(self, balence, highscore, spin_count, multiplier_count, broke_counter, best_spin, jackpot_multiplier_counter):
        self.cursor.execute("INSERT INTO data VALUES(?, ?, ?, ?, ?, ?, ?)", (balence, highscore, spin_count, multiplier_count, broke_counter, best_spin, jackpot_multiplier_counter))
        self.conn.commit()

# show all data
    def get_data(self): 
        self.cursor.execute("SELECT * FROM data")
        return self.cursor.fetchall()
    
# print the column data
    def get_column(self, column): # show specific column
        self.cursor.execute(f"SELECT {column} FROM data")
        return self.cursor.fetchone()[0]
    
    def add_column(self, column, data): # add a new column
        self.cursor.execute(f"ALTER TABLE data ADD COLUMN {column} {data}")
        self.conn.commit()
    
# update all data at once
    def update_data(self, balance, highscore, spin_count, multiplier_count, broke_counter, best_spin, jackpot_multiplier_counter):
        if not self.get_data():
            self.insert_data(balance, highscore, spin_count, multiplier_count, broke_counter, best_spin, jackpot_multiplier_counter)
            return
        self.cursor.execute("UPDATE data SET balance = ?, highscore = ?, spin_count = ?, multiplier_count = ?, broke_counter = ?, best_spin = ?, jackpot_multiplier_counter = ?", (balance, highscore, spin_count, multiplier_count, broke_counter, best_spin, jackpot_multiplier_counter))
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


# how to use the class / test
db = DataBase()

db.update_column("balance", json_fm.load_balance())
db.update_column("highscore", json_fm.load_highscore())
db.update_column("spin_count", json_fm.load_spin_count())
db.update_column("multiplier_count", json_fm.load_multiplier_count())
db.update_column("broke_counter", json_fm.load_broke_counter())
db.update_column("best_spin", json_fm.load_best_spin())
db.update_column("jackpot_multiplier_counter", json_fm.load_jackpot_multiplier_counter())


print( db.get_data() )
print( db.get_column("balance") )


