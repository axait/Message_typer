database_file_location = "C:/Program Files/messagetyper/save_msg.db"
folder_path = "C:/Program Files/messagetyper"

import os
import sqlite3

class database_editing_class(sqlite3.Connection):
    def __init__(self ):
        try:
            os.makedirs(folder_path)
        except FileExistsError:
            ...
        # Call the constructor of the parent class (sqlite3.Connection)
        super().__init__( database_file_location )
        self.cursor = self.cursor()
        try:
            # Create the save_msg_table with id (auto-increment) and msgs (text)
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS save_msg_table (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    msgs TEXT
                )
            ''')
            self.commit()
        except:
            ...

    def create_table(self):
        # Create the save_msg_table with id (auto-increment) and msgs (text)
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS save_msg_table (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                msgs TEXT
            )
        ''')
        self.commit()

    def add_msg(self, message : str ):
        # Add a new message to the msgs column
        self.cursor.execute("INSERT INTO save_msg_table (msgs) VALUES (?)", (message,))
        self.commit()

    def update_msg(self, old_message : str , new_message : str ):
        # Update messages without knowing the ID
        self.cursor.execute("UPDATE save_msg_table SET msgs = ? WHERE msgs = ?", (new_message, old_message))
        self.commit()

    def delete_msg(self, old_message : str ):
        try:
            # Use the DELETE FROM statement to delete rows from the table
            self.cursor.execute("DELETE FROM save_msg_table WHERE msgs = ?", (old_message,))
            self.commit()
            return (f"Deleted message: {old_message}")
        except Exception as e:
            return (f"Error deleting message: {e}")

    def fetch_all_data(self):
        # Fetch all data from the table
        self.cursor.execute("SELECT * FROM save_msg_table")
        return self.cursor.fetchall()

    def clear_database(self):
        # Delete all data from the database
        self.cursor.execute("DELETE FROM save_msg_table")
        self.commit()

    def close_connection(self):
        # Close the database connection
        self.close()


# if __name__ == '__main__' :
#     # Usage example:
#     db = database_editing_class('save_msg.db')
#     # db.create_table()
#     for i in range(50):
#         db.add_msg(i)
#     # db.add_msg("Hello, world!")
#     # db.update_msg("ALI", "Updated message")
#     # data = db.fetch_all_data()
#     # data = db.clear_database()
#     # print("All data:")
#     # for row in data:
#     #     print(row)
#     # # db.clear_database()
#     db.close_connection()


# class database_editing_class(sqlite3.Connection):
#     def __init__(self, db_file_name):
#         # Call the constructor of the parent class (sqlite3.Connection)
#         super().__init__(db_file_name)
#         self.cursor = self.cursor()
#         # 
#     def add_msg(self , message:str ):
#         """This function add new data mean new message in database"""
#         self.cursor.execute("INSERT INTO save_msg_table (msgs) VALUES (?)", (message))


#         # Commit the changes and close the connection
#         self.commit()
#     def fetch_all_messages(self):
#         # Retrieve all messages from the table
#         self.cursor.execute("SELECT msgs FROM save_msg_table")
#         return [row[0] for row in self.cursor.fetchall()]
#     def close_connection(self):
#         # Close the database connection
#         self.close()

# import sqlite3

# # Connect to the SQLite database (or create it if it doesn't exist)
# conn = sqlite3.connect('save_msg.db')

# # Create a cursor object to interact with the database
# cursor = conn.cursor()
# message = "d"
# cursor.execute("INSERT INTO save_msg_table (msgs) VALUES (?)", (message))


# # Commit the changes and close the connection
# conn.commit()
# conn.close()




# # Create the save_msg_table with id (auto-increment) and msgs (text)
# cursor.execute('''
#     CREATE TABLE IF NOT EXISTS save_msg_table (
#         id INTEGER PRIMARY KEY AUTOINCREMENT,
#         msgs TEXT
#     )
# ''')
# print("Table 'save_msg_table' has been created in 'save_msg.db'")
