#!/usr/bin/python3
import telebot
from engine.utility import *
from telebot import types
from random import shuffle
from html import unescape
from os import getenv
from dotenv import load_dotenv

load_dotenv()

bot = telebot.TeleBot(getenv("API_KEY"))

users_progress = {'status': '0'}

ans_list = [] # Handles all the answers


@bot.message_handler(commands=["start"])
def start_bot(message):
	"""Starts the bot"""
	continue_btn = types.InlineKeyboardButton(text="🟢 Continue", callback_data="continue")
	markup1 = types.InlineKeyboardMarkup().add(continue_btn)
	bot.send_message(message.chat.id, start_reply, reply_markup=markup1)
	if users_progress.get("user_id"):
		del users_progress["user_id"]


@bot.callback_query_handler(func=lambda callback: callback.data == "continue")
def continue_task(callback):
	"""After continue"""
	bot.answer_callback_query(callback.id)
	bot.send_message(callback.message.chat.id, categories)


@bot.message_handler(func=lambda message: message.text.isdigit())
def check_message(message):
	"""Checks each messages parsed"""
	global response
	response = int(message.text)
	if users_progress["status"] == '1':
		receive_answer(message)
	elif response in range(cat1, catN) and users_progress["status"] == '0':
		bot.send_message(message.chat.id, "Getting Your Questions Ready In A Bit")
		question_answer(response, message)
	else:
		bot.send_message(message.chat.id, "Number not in range of listed categories")


def question_answer(category, message):
	"""Handles questions"""
	global users_progress
	user_id = message.chat.id
	if user_id not in users_progress:
		users_progress["status"] = '1'
		users_progress[user_id] = {'correct_answers': 0}
	global questions
	questions = ask_question_group(category)
	if "num" not in users_progress[user_id]:
		users_progress[user_id]["num"] = 0
	loop_questions(user_id, users_progress[user_id]["num"])


def loop_questions(user_id, num=0):
	"""dummy function for looping questions"""
	if num < 10:
		question_text = questions["results"][num]["question"]
		question_text = unescape(question_text)
		correct_answer = questions["results"][num]["correct_answer"]
		ans_list.append((num + 1, unescape(correct_answer)))
		# Prepare the list of answers and shuffle them.
		answers = questions["results"][num]["incorrect_answers"] + [correct_answer]

		shuffle(answers)

		markup2 = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
		for answer in answers:
			markup2.add(types.KeyboardButton(text=unescape(answer)))
		
		# Send the question with answer buttons.
		bot.send_message(user_id, question_text, reply_markup=markup2)
		
		# Store the current question and correct answer for the user.
		users_progress[user_id]['correct_answer'] = correct_answer
	else:
		# No more questions left to answer in this category.
		bot.send_message(user_id, "You have answered all the questions in this category.")
		bot.send_message(user_id, users_score(user_id, users_progress) + "\n" + end_reply)
		ans_string = "Answers to the questions:\n"
		ans_string += "\n".join([str(item) for item in ans_list])
		bot.send_message(user_id, ans_string)
		del users_progress[user_id]
		users_progress["status"] = '0'


@bot.message_handler(func=lambda message: True)
def receive_answer(message):
	"""Check if the message corresponds to an ongoing question."""
	if message.chat.id in users_progress:
		user_id = message.chat.id
		correct_answer = users_progress[user_id]['correct_answer']
		if message.text == correct_answer:
			bot.send_message(message.chat.id, "Correct! 🎉")
			users_progress[user_id]['correct_answers'] += 1
		else:
			bot.send_message(message.chat.id, "Oops! That's not correct. 😢")
		users_progress[user_id]["num"] += 1
		loop_questions(user_id, users_progress[user_id]["num"])



bot.polling()
