"""
main7.py - Dynamic Model Choice
Lets the user pick which model to use at runtime, so the same code
can switch between a fast/cheap model and slower/more capable one.
"""
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, AIMessage

load_dotenv()

# A dictionary of available models - swap freely without changing logic
models = {
	"1": ("Fast & light", "llama-3.1-8b-instant"),
	"2": ("Balanced", "llama-3.3-70b-versatile"),
	"3": ("Reasoning", "openai/gpt-oss-120b"),
}

print("Choose a model: ")
for key, (name, model_id) in models.items():
	print(f" {key}. {name} ({model_id})")

choice = input("Enter choice (1-3): ").strip()
model_name, model_id = models.get(choice, models["1"])

print(f"\nUsing model: {model_name} ({model_id})\n")

# The model is chosen dynamically based on user input
llm = ChatGroq(model=model_id)

conversation = []

while True:
	user_input = input("You: ").strip()
	if user_input.lower() in ["exit", "quit"]:
		break

	conversation.append(HumanMessage(content=user_input))
	response = llm.invoke(conversation)
	print("AI:", response.content, "\n")
	conversation.append(AIMessage(content=response.content))
