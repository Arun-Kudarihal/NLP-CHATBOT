from gtts import gTTS
import speech_recognition as sr
import os
import re
import webbrowser
import smtplib
import requests
#from chatbot import Chat,MultiFunctionCall
import wikipedia
import re

from chatterbot import ChatBot
chatbot = ChatBot('Adam')

#from weather import Weather

import tkinter as tk
from tkinter import ttk

output = open('output/Session_data','w')
output.write('')
output.close()

class Main_Class():
	def __init__(self):
		self.begin = True


	def file_output(self,text):
		output_object = open('output/Session_data','a')
		output_object.write(text + '\n')
		output_object.close()

	def gtts_speech(self,audio):
		text_to_speech = gTTS(text=str(audio),lang='en')
		text_to_speech.save('audio.mp3')
		os.system('afplay audio.mp3')
	
	def system_speech(self,audio):
		os.system("say " + str(audio))


	def clean(self,text):
		#text.replace('(\w+)','')
		text = re.sub("[()''\[\];:\"\"]",'',text)
		return text

	def initial_screen(self):
		text = '******** WELCOME ********\n\n'
		text = text + '1. To interact with the chatbot using text type the QUERY and click on Get Answer\n\n'
		text = text + '2. To interact with the chatbot through voice click on the Voice Conversation\n\n'
		self.file_output(text)
		textbox.insert(tk.END,text)


	def talkToMe(self,audio):
		"speaks audio passed as argument"
		audio = self.clean(str(audio))
		to_print = 'Chatbot: ' + audio + '\n'
		self.file_output(to_print)
		print(to_print)
		textbox.insert(tk.END,to_print)
    
		try:
			self.system_speech(audio)
			#for line in audio.splitlines():
			#os.system("say " + audio)
			#break
		except:
			self.gtts_speech(audio)
			#use the system's inbuilt say command instead of mpg123
		


	def myCommand(self):
		"listens for commands"

		r = sr.Recognizer()

		with sr.Microphone() as source:
			print('Ready...')
			r.pause_threshold = 1
			r.adjust_for_ambient_noise(source, duration=1)
			audio = r.listen(source)

		try:
			command = r.recognize_google(audio).lower()
			print('You said: ' + command + '\n')

		#loop back to continue to listen for commands if unrecognizable speech is received
		except sr.UnknownValueError:
			print('Your last command couldn\'t be heard')
			command = self.myCommand()

		return command

	def who_is(self,query,session_id="general"):
		try:
			return wikipedia.summary(query,sentences=2)
		except:
			try:
				for new_query in wikipedia.search(query):
					text = wikipedia.summary(new_query,sentences=2)
					#text = text.split('\n')
					#return text[0]
					return text
			except:
				return "No Internet connection! Please try again"
				pass
	#return "I don't know about "+ query
	


	def assistant(self):
		"if statements for executing commands"
		self.talkToMe('I am ready for your command')
		query = self.myCommand()
		to_print = 'User Said : ' + query + '\n'
		self.file_output(to_print)
		textbox.insert(tk.END,to_print)
		self.reply(query)

	def assistant_text(self):
		query = query_var.get()
		to_print = 'User Query : ' + query + '\n'
		print(to_print)
		self.file_output(to_print)
		textbox.insert(tk.END,to_print)
		self.reply(query)

	def intent_handler(self,command):
		if 'open reddit' in command:
			reg_ex = re.search('open reddit (.*)', command)
			url = 'https://www.reddit.com/'
			if reg_ex:
				subreddit = reg_ex.group(1)
				url = url + 'r/' + subreddit
			webbrowser.open(url)
			print('Done!')

		elif 'open website' in command:
			reg_ex = re.search('open website (.+)', command)
			if reg_ex:
				domain = reg_ex.group(1)
				url = 'https://www.' + domain
				webbrowser.open(url)
				print('Done!')
			else:
				pass

		elif 'what\'s up' in command:
			self.talkToMe('Just doing my thing')
		elif 'joke' in command:
			res = requests.get('https://icanhazdadjoke.com/',headers={"Accept":"application/json"})

			if res.status_code == requests.codes.ok:
				self.talkToMe(str(res.json()['joke']))
			else:
				self.talkToMe('oops!I ran out of jokes')
		elif 'email' in command:
			self.talkToMe('Who is the recipient?')
			recipient = self.myCommand()

			if 'John' in recipient:
				self.talkToMe('What should I say?')
				content = self.myCommand()

				#init gmail SMTP
				mail = smtplib.SMTP('smtp.gmail.com', 587)

				#identify to server
				mail.ehlo()

				#encrypt session
				mail.starttls()

				#login
				mail.login('username', 'password')

				#send message
				mail.sendmail('John Fisher', 'JARVIS2.0@protonmail.com', content)

				#end mail connection
				mail.close()

				self.talkToMe('Email sent.')
		elif 'what is your name' in command:
			self.talkToMe('My name is Major Project')
		elif 'tell me about' in command:
			#call = MultiFunctionCall({"whoIs":who_is})
			command = re.sub('tell me ','',command)
			call = self.who_is(command)
			self.talkToMe(call)
		elif 'who is' in command:
			#command = re.sub('who is ','',command)
			call = self.who_is(command)
			self.talkToMe(call)
		elif 'when was' in command:
			#command = re.sub('when was ','',command)
			call = self.who_is(command)
			self.talkToMe(call)
		elif 'when is' in command:
			#command = re.sub('when is ','',command)
			call = self.who_is(command)
			self.talkToMe(call)
		elif 'what is' in command:
			call = self.who_is(command)
			self.talkToMe(call)
		else:
			response = chatbot.get_response(command)
			self.talkToMe(response)
		
	def reply(self,command):
		self.intent_handler(command)

	def saveSession(self):
		self.talkToMe('Successfully saved')	
		self.begin = False
		exit()

main = Main_Class()

win = tk.Tk()
win.title('CHATBOT USING NLP')


query_label = ttk.Label(win,text='Enter Query')
query_var = tk.StringVar()
query_label.grid(row=0,column=0,sticky=tk.W)
query_entrybox = ttk.Entry(win,width = 40,textvariable = query_var)
query_entrybox.grid(row=0,column=1)

choose_btn = ttk.Button(win,text='Get Answer',command=main.assistant_text)
choose_btn.grid(row=0,column=2,sticky=tk.W)
choose_btn.config(width=15)

textbox = tk.Text(win, height=30, width=60)
S = tk.Scrollbar(win)
S.grid(row=4,column=2,rowspan=8,sticky=tk.W)
S.config(command=textbox.yview)
textbox.config(yscrollcommand=S.set)
textbox.grid(row=5,column=1)


start_btn = ttk.Button(win,text='Voice Conversation',command=main.assistant)
start_btn.grid(row=1,column=2,sticky=tk.W)
start_btn.config(width=15)

save_btn = ttk.Button(win,text='Save Session',command=main.saveSession)
save_btn.grid(row=2,column=2,sticky=tk.W)
save_btn.config(width=15)


main.initial_screen()

win.mainloop()

