from chatbot import chatbot
from chatterbot.trainers import ChatterBotCorpusTrainer

trainer = ChatterBotCorpusTrainer(chatbot)

trainer.train(
    "chatterbot.corpus.english",
     "chatterbot.corpus.english.greetings",
    "chatterbot.corpus.english.conversations"
)


#while(1):
	#q = input('enter query')
	#response = chatbot.get_response(q)
	#print(response)
