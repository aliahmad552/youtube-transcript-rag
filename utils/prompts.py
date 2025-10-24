from langchain_core.prompts import PromptTemplate

qa_prompt = PromptTemplate(
    template="""
    You are a helpful AI assistant.
    Answer only using the provided context.
    If the context is insufficient, say "I don't know based on this video."

    Context:
    {context}

    Question: {question}
    """,
    input_variables=["context", "question"]
)
