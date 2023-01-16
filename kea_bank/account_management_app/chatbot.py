from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
import json
from .models import Customer

chatbot = ChatBot('Bank')


def chatterbot_setup():
    # Creating ChatBot Instance

    # Training with Personal Ques & Ans
    conversation = [
        "Hello", "Hi there! What can I help you with?", "Hey",
        "Hi there! What can I help you with?", "Hi",
        "Hello, what can I help you with?", "I need help!",
        "What do you need help with?", "How do I transfer money?",
        "Got to dashboard open account you want to transfer money from. Inser the amount, the account number and click on send. ",
        "How do I make a loan?",
        "Open account you want to take loan for. Enter the amount and click on Take loan",
        "How do I return money?",
        "Open the account you want to return money from, insert the amount and click on Pay back.",
        "How do I add money to my transfer account?",
        "Go to my savings, if you dont have an account create one. Once account is created insert the amount, and chose the account you want to transfer money from."
    ]

    trainer = ListTrainer(chatbot)
    trainer.train(conversation)


def get_chatbot_response(self):
    json_array = []
    response = chatbot.get_response(self)
    print(response)
    text_json = {'question': self, 'response': str(response)}
    json_array.append(text_json)
    return json_array


def save_conversation(user, self):
    conv_array = []
    chatbot_conv = get_chatbot_response(self)
    json_str = json.dumps(chatbot_conv)
    json_load = json.loads(json_str)

    existing_conv = Customer.objects.filter(user=user)
    if existing_conv.exists():
        existing_conv_obj = Customer.objects.get(user=user)
        conv = existing_conv_obj.json_array

        if conv == {}:
            conv_array.append(json_load)
            existing_conv_obj.json_array = conv_array
        else:
            conv.append(json_load)

        existing_conv_obj.save()
    return conv


def get_all_conv(user):
    existing_conv_obj = Customer.objects.get(user=user)
    whole_conversation = existing_conv_obj.json_array
    return whole_conversation
