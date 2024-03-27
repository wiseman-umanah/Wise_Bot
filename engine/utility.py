#!/usr/bin/python3
import requests


r = requests.get("https://opentdb.com/api_category.php").json()
categories = """Please choose a category by sending its number(Id).
Id\t\tCategory\n"""
catlen = len(r["trivia_categories"])

for i in r["trivia_categories"]:
	categories += f"{i['id']}\t\t{i['name']}\n"
cat1 = r["trivia_categories"][0]["id"]
catN = r["trivia_categories"][catlen - 1]["id"]


def ask_question_group(response=cat1):
	"""
	This function returns the questions and answer set
	based on the response of the user or the first category by default

	Arguments:
		response (int): The id or first category id by default
	"""
	questions = requests.get(f"https://opentdb.com/api.php?amount=10&category={response}").json()
	return questions




start_reply = """
🎉 Welcome to Wise_bot! 🤖✨

👋 Hey there! I'm Wise_bot, your go-to trivia partner. Get ready to dive into a sea of questions from various categories. Whether you're in the mood for a brain workout or just looking for some fun facts, I've got you covered.
"""


end_reply = """
Thank You For Using My Bot

If you feel a need to play around try the /start command 😊

Don't Forget to follow the Developer

𝕏 Follow My Official Twitter (https://www.twitter.com/wisemanjoearts)

💬 Comment on the lastest post on Twitter

🔵 Follow Me On LinkedIn (https://www.linkedin.com/in/wisemanumanah)
"""


def users_score(user_id, users_progress={}):
	"""
	This returns the score of the user to be printed
	to user

	Arguments:
		user_id (id): The current user id
		users_progress (dict): The users progress
	"""
	details = "Your ScoreLine: "
	if users_progress[user_id]:
		user = users_progress[user_id]
		details += f'Your Score is {user["correct_answers"]}/10\n'
		if user["correct_answers"] < 5:
			details += "😢 Try Harder next Time"
		elif user["correct_answers"] == 5:
			details += "😆 Oh Boy, You are So lucky!"
		else:
			details += "🎆🎇🎉🥳WOW!, Let's Celebrate"
		return details

