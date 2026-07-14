#streaming means getting response word-by-word instead of waiting for the whole thing to pront at once more like chatgot interface, this part shows that
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
	print("AI:", end="", flush=True)

	full_response = ""
	#.stream() instead of .invoke() gives us chunks as they arrive
	for chunk in llm.stream(conversation):
		print(chunk.content, end="", flush=True)
		full_response += chunk.content
	print() #move to a new line after the response finishes

	#add the AI's reply to history too so it remembers what it said
	conversation.append(AIMessage(content=full_response))
