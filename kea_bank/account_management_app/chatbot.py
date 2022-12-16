from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
from chatterbot.trainers import ChatterBotCorpusTrainer
import json
from . models import Conversation


# Creating ChatBot Instance
chatbot = ChatBot('Bank')

 # Training with Personal Ques & Ans 
conversation = [
    "Hello",
    "Hi there!What can I help you with?",
    "Hi",
    "Hello, what can I help you with?"
    "I need help!",
    "What do you need help with?",
    "How do I transfer money?",
    "Got to dashboard open your account ",
    "How do I make a loan?",
    "Open account click on .."
]

trainer = ListTrainer(chatbot)
trainer.train(conversation)

# Training with English Corpus Data 
trainer_corpus = ChatterBotCorpusTrainer(chatbot)
trainer_corpus.train(
    'chatterbot.corpus.english',
    'chatterbot.corpus.english.conversations'

) 

json_array = []

def get_chatbot_response(self):
    response = chatbot.get_response(self)
    print(response)
    text_json = {
        'question': self,
        'response': str(response)
    }
    json_array.append(text_json)
    return response

def get_conversation(user):
    print(json_array)
    json_str = json.dumps(json_array)
    json_load = json.loads(json_str)
    conversation = Conversation(json_array=json_str, user = user)
    conversation.save()
    return json_load



