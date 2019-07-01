import os
import json
from django.shortcuts import render 
from django.http import JsonResponse, HttpResponse
from bot.chatterbotBot import Bot


chatbot = Bot()

chatbot.trainBot()

def index(request):
    return render(request, 'index.html')

def bot(request):
    input_data = json.loads(request.body.decode('utf-8'))

    response = chatbot.get_answer(input_data["text"])

    return HttpResponse(response, status=200)

def goodAnswer(request):
    input_data = json.loads(request.body.decode('utf-8'))

    message = input_data["message"]
    in_response_to = input_data["in_response_to"]

    answer = chatbot.learn_answer(message, in_response_to)

    if message and in_response_to:
        return HttpResponse(answer, status=200)
    else:
        return HttpResponse(status=400)
