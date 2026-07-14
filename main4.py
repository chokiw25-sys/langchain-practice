"""
Multimodel Input:
sends both text and an image to the model in a single message, 
so it can describe or answer questions about the image.
"""

import base64
import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, AIMessage
 
load_dotenv()

llm = ChatGroq(model= "qwen/qwen3.6-27b")


#this holds all the converstations
conversation = []

print("Chat started. Type 'exit' to quit.")
print("When asked for an image, press Enter to skip it. \n")

while True:

	# ask the user for the image path
	image_path = input("Enter the path to your image(e.g. phot0.jpg): ")

	image_content = None
	if image_path:
		if not os.path.exists(image_path):
        		print(f"file not found: {image_path} - sending text only. \n")
        		content=user_input
		else:
			ext = os.path.splitext(image_path)[1].lower().replace(".", "")
			if ext == "jpg":
				ext -"jpeg"
			with open(image_path, 'rb') as f:
				image_data= base64.b64encode(f.read()).decode('utf-8')
			image_content = f"data:image/{ext};base64,{image_data}"

	user_input = input("You: ")
	if user_input.lower() in ["exit", "quit"]:
		break

	#in here the ai decide if it is suppose to give answer for text only or for the picture and text together
	if image_content:
		content = [
			{"type": "text", "text": user_input},
			{"type": "image_url","image_url":{"url":image_content}},
		]
	else:
		content = user_input

	conversation.append(HumanMessage(content=content))

	response = llm.invoke(conversation)
	print("AI:", response.content, "\n")

	#add the AI's reply to history too so it remembers what it said
	conversation.append(AIMessage(content=response.content))
