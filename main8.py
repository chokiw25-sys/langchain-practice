"""
main8.py - custom agent Middleware
Demonstrates wrapping the LLM call with custom "middleware" functions
that run before and after each response - e.g. loffing, timing, and a simple content guardrail.
"""

import time
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, AIMessage

load_dotenv()

llm = ChatGroq(model="llama-3.1-8b-instant")

conversation = []

# --- MIDDLEWARE FUNCTIONS ---

def log_input(user_input: str):
	"""Run BEFORE the model call - logs what the user asked."""
	print(f"[LOG] User asked: {user_input}")

def check_guardrail(user_input: str) -> bool:
	"""Runs BEFORE the model call - blocks certain inputs."""
	blocked_words = ["hack", "password", "exploit"]
	for word in blocked_words:
		if word in user_input.lower():
			print(f"[GUARDRAIL] Blocked input containing '{word}'")
			return False
	return True

def log_output(response_text: str, duration: float):
	"""Runs AFTER the model call - log timing and respnse length."""
	print(f"[LOG] respnse tool {duration: .2f}s, {len(response_text)} characters")

# --- MAIN LOOP WITH MIDDLEWARE APPLIED ---

while True:
	user_input = input("You: ").strip()
	if user_input.lower() in ["exit", "quit"]:
		break

	# Middleware step 1: logging
	log_input(user_input)

	# Middleware step 2: guardrail check
	if not check_guardrail(user_input) :
		print("AI: sorry, i cant help with that request. \n")
		continue
	conversation.append(HumanMessage(content=user_input))

	#time the actual model call
	start_time = time.time()
	response = llm.invoke(conversation)
	duration =time.time() -start_time

	#Middleware step 3: post-respone logging
	log_output(response.content, duration)

	print("AI: ", response.content, "\n")
	conversation.append(AIMessage(content=response.content))
