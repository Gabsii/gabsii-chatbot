from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
from chatterbot.conversation import Statement
import sqlite3

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
            
            cursor.execute('SELECT message, quotedMessage FROM chatdata WHERE media IS NULL')
            results = cursor.fetchall()
            for r in results:
                if (r[1] == None):
                    trainer.train(r)
                else:
                    self.bot.learn_answer(r[0], r[1])
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

    def learn_answer(self, message, in_reply_to):
        return self.bot.learn_response(Statement(text=message), Statement(text=in_reply_to))

def main():
    Niklas = Bot()
    Niklas.trainBot()
    Niklas.testBot()

if __name__ == '__main__':
    main()