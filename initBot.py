############################################
#                                          #
#        I exported my data from a         #
#      WhatsApp chat using an extension    #
#          from the Chrome Store           #
#         (Backup WhatsApp Chats)          #
#                                          #
#    But it's broken since csv's don't     #
#     handle line breaks (\n) well         #
#                                          #
############################################

import csv
import sqlite3

class InitBotData(object):
    def __init__(self):
        super().__init__()

        self.csv = 'data.csv'
        self.conn = sqlite3.connect('chatbot.db')

    def testCSV(self): 
        with open(self.csv, newline='',  encoding="utf-8") as csvfile:
            reader = csv.reader(csvfile, delimiter=';', quotechar='"',
                            quoting=csv.QUOTE_ALL, skipinitialspace=True)
            counter = 1 
            wrongLen = 0
            maxCheck = 60000
            next(reader)
            for row in reader:
                if counter < maxCheck:
                    if len(row) != 10:
                        print("_____")
                        print('row: ' + str(counter) + ', len: ' + str(len(row)))
                        print(row)
                        print("_____")
                        wrongLen += 1
                else: 
                    break
                counter += 1        
            print('len. ' + str(wrongLen))

    def createTables(self):
        # datetime TEXT NOT NULL
        # sender TEXT NOT NULL
        # message TEXT NOT NULL
        # media TEXT 
        # quotedMessage TEXT
        # quotedMessageDatetime TEXT
        try:
            cursor = self.conn.cursor()
            cursor.execute('''CREATE TABLE IF NOT EXISTS chatdata
                                (datetime TEXT, 
                                sender TEXT NOT NULL, 
                                message TEXT NOT NULL,
                                media TEXT,
                                quotedMessage TEXT,
                                quotedMessageDatetime TEXT)''')
            self.conn.commit()
            return True
        except sqlite3.Error as e:
            print("An error occurred:", e.args[0])

    def insertData(self):
        try:
            cursor = self.conn.cursor()

            with open(self.csv, newline='',  encoding="utf-8") as csvfile:
                reader = csv.reader(csvfile, delimiter=';', quotechar='"',
                                quoting=csv.QUOTE_ALL, skipinitialspace=True)
                next(reader)
                data = []
                for row in reader:
                    datetime = row[1] + " " + row[2]
                    sender = row[4]
                    message = row[5]
                    media = row[6] if row[6] != 'null' else None
                    quotedMessage = row[7] if row[7] != 'null' else None
                    quotedMessageDatetime = row[8] + " " + row[9] if row[8] != 'null' else None
                    rowData = (datetime, sender, message, media, quotedMessage, quotedMessageDatetime)
                    data.append(rowData)
                    if reader.line_num % 10000:
                        cursor.executemany('INSERT INTO chatdata VALUES (?, ?, ?, ?, ?, ?)', data)
                        data = []
                if len(data) >= 1:
                        cursor.executemany('INSERT INTO chatdata VALUES (?, ?, ?, ?, ?, ?)', data)
            self.conn.commit()
        except sqlite3.Error as e:
            print("An error occurred:", e.args[0])

    def closeConnection(self):
        return self.conn.close()

def main():
    
    init = InitBotData()

    init.createTables()
    print("start insert")
    init.insertData()
    init.closeConnection()
    print("insert done")
if __name__ == '__main__':
    main()