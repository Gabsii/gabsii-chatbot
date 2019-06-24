from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
import sqlite3
import pickle

class Bot(object):
    def __init__(self):
        super().__init__()

        self.bot = ChatBot('Niklas')
        self.conn = sqlite3.connect('chatbot.db')

    def trainBot(self):
        trainer = ListTrainer(self.bot)
        #Training Bot with existing comments from db
        try:
            cursor = self.conn.cursor()
            
            cursor.execute('SELECT message FROM chatdata WHERE media IS NULL')
            results = cursor.fetchall()
            res = [''.join(i) for i in results]
            trainer.train(res)
        except sqlite3.Error as e:
            print('Error occured: ', e.args[0])
        except KeyboardInterrupt as e:
            return

    def testBot(self): 
        #Testing bot
        print()
        while True:
            request = input("You: ")
            response = self.get_answer(request)
            print('Bot:', response)

    def get_answer(self, question):
        return self.bot.get_response(question)

def main():
    Niklas = Bot()
    Niklas.trainBot()
    Niklas.testBot()

if __name__ == '__main__':
    main()