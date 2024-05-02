import mysql.connector

class Database:
    def __init__(self):
        self.mydb = mysql.connector.connect(
            host="localhost",
            user="elwalid",
            password="VIOLON1999",
            database="mydatabase"
        )
        self.mycursor = self.mydb.cursor()

    def create_table(self):
        try:
            sql_guest = """
                CREATE TABLE IF NOT EXISTS guests (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    email VARCHAR(255) UNIQUE NOT NULL,
                    password VARCHAR(255) NOT NULL,
                    firstName VARCHAR(255) DEFAULT NULL,
                    lastName VARCHAR(255) DEFAULT NULL,
                    CIN VARCHAR(255) UNIQUE DEFAULT NULL,
                    license VARCHAR(255) UNIQUE DEFAULT NULL,
                    licenseDateOfDelivery DATE DEFAULT NULL,
                    DayOfBirth DATE DEFAULT NULL,
                    address VARCHAR(255) DEFAULT NULL
                )
            """
            self.mycursor.execute(sql_guest)
            self.mydb.commit()
            print("\033[92mTable 'guests' created successfully!\033[0m")  # Green text indicating success
        except mysql.connector.Error as err:
            print("\033[91mError creating table: {}\033[0m".format(err))  # Red text indicating error
