from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer, ListTrainer
import config_files.config as config


def ai_talk(question):
    chatbot = ChatBot('Mr. Butler',
                      database=f'{config.db_path}CB_talk.db',
                      logic_adapters=[
        {
            'import_path': 'chatterbot.logic.BestMatch',
            'threshold': 0.65,
            'default_response': 'I\'d love to chat with you some more, but better use the buttons!',
        }
    ])

    # trainer = ListTrainer(chatbot)
    #
    # with open('../lib/dialogues.txt', 'r', encoding='utf-8') as f:
    #     content = f.readlines()
    #     # you may also want to remove whitespace characters like '\n' at the end of each line
    # content = [x.strip() for x in content]
    #
    # train_data = []
    # p = 0
    # for i in content:
    #     if p == 0 and i != '':
    #         train_data.append(i)
    #         p += 1
    #         continue
    #     elif p == 1 and i != '':
    #         train_data.append(i)
    #         p += 1
    #         continue
    #     elif p == 2 and i != '':
    #         continue
    #     elif p == 2 and i == '':
    #         p = 0
    #         continue
    #
    # trainer.train(train_data)


    # Create a new trainer for the chatbot
    trainer = ChatterBotCorpusTrainer(chatbot)
    # Train the chatbot based on the english corpus
    trainer.train("chatterbot.corpus.english.conversations")
    # Get a response to an input statement
    response = chatbot.get_response(question)
    return response


