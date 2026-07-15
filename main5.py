"""
main5.py — RAG (Retrieval Augmented Generation)
Loads a text file, splits it into chunks, embeds those chunks,
stores them in a FAISS vector store, and retrieves relevant chunks
to answer questions using only the content of the document.
"""

from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.messages import HumanMessage, SystemMessage

load_dotenv()

# 1. Load the document
with open("notes.txt", "r", encoding="utf-8") as f:
    text = f.read()

# 2. Split it into smaller chunks (so retrieval is more precise)
splitter = RecursiveCharacterTextSplitter(chunk_size=300, chunk_overlap=50)
chunks = splitter.split_text(text)
print(f"Split document into {len(chunks)} chunks.\n")

# 3. Embed the chunks and store them in a FAISS vector store
embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
vector_store = FAISS.from_texts(chunks, embeddings)

# 4. Set up the LLM
llm = ChatGroq(model="llama-3.1-8b-instant")

print("RAG system ready. Ask a question about notes.txt (type 'exit' to quit).\n")

while True:
    question = input("You: ").strip()
    if question.lower() in ["exit", "quit"]:
        break

    # Retrieve the most relevant chunks for this question
    relevant_docs = vector_store.similarity_search(question, k=2)
    context = "\n\n".join(doc.page_content for doc in relevant_docs)

    # Build a prompt that includes the retrieved context
    system_prompt = SystemMessage(content=(
        "Answer the user's question using ONLY the following context. "
        "If the answer isn't in the context, say you don't know.\n\n"
        f"Context:\n{context}"
    ))

    response = llm.invoke([system_prompt, HumanMessage(content=question)])
    print("AI:", response.content, "\n")
