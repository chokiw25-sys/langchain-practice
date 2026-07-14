from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, AIMessage
 
load_dotenv()

llm = ChatGroq(model= "llama-3.1-8b-instant")
#this holds all the converstations
conversation = []

while True:
	user_input = input("You: ")
	if user_input.lower() in ["exit", "quit"]:
		break
	#add the user's message to history
	conversation.append(HumanMessage(content=user_input))

	#send the whole coverstation so for, not jst the latest message 
	response = llm.invoke(conversation )
	print("AI:", response.content)

	#add the AI's reply to history too so it remembers what it said
	conversation.append(AIMessage(content=response.content))
