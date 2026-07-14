"""
Advance agent example demo:
1. context: a systemMessage to set the AI's role/behavior
2. structured output: using pydantic + with_structured_output() to get clean python objects back instead of free text
3. Memory: keeping a running conversation list
"""
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage
from pydantic import BaseModel, Field

load_dotenv()

llm = ChatGroq(model="llama-3.1-8b-instant")

system_prompt = SystemMessage(content=(
	"You are a helpful assistant that extracts structured task information "
	"from what the user tells you about something they need to do."
))

class TaskInfo(BaseModel):
	task: str = Field(description="A short summary of the task")
	priority: str = Field(description="low, medium, or high")
	deadline: str = Field(description= "Deadline mentioned, or 'none' if not stated")

structured_llm= llm.with_structured_output(TaskInfo)

conversation = [system_prompt]

while True:
	user_input= input("You: ")
	if user_input.lower() in ["exit", "quit"]:
		break

	conversation.append(HumanMessage(content=user_input))
	result = structured_llm.invoke(conversation)

	print("AI extracted:")
	print(f" task: {result.task}")
	print(f"Priority: {result.priority}")
	print(f"deadline: {result.deadline}")

	conversation.append(AIMessage(content=str(result)))
