from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer


def ai_talk(question):
    chatbot = ChatBot('Ron Obvious', logic_adapters=[
        {
            'import_path': 'chatterbot.logic.BestMatch',
            'threshold': 0.65,
            'default_response': 'I\'d love to chat with you some more, but better use the buttons!'
        }
    ])

    # Create a new trainer for the chatbot
    trainer = ChatterBotCorpusTrainer(chatbot)

    # Train the chatbot based on the english corpus
    trainer.train("chatterbot.corpus.english.conversations")

    # Get a response to an input statement
    response = chatbot.get_response(question)
    return response
