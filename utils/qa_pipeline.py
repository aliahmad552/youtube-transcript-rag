import os
import pickle
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings, ChatHuggingFace, HuggingFaceEndpoint
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableParallel, RunnableLambda
from operator import itemgetter
from dotenv import load_dotenv
from utils.prompts import qa_prompt

load_dotenv()

# 🔹 Global embedding + model load once (for speed)
embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
llm = HuggingFaceEndpoint(repo_id="meta-llama/Meta-Llama-3-8B-Instruct", task="text-generation")
chat_model = ChatHuggingFace(llm=llm)

# Vector Store
def get_vector_store(video_id: str, transcript: str):
    """Cache & reuse FAISS vector store for each video."""
    os.makedirs("cache", exist_ok=True)
    cache_path = f"cache/{video_id}_faiss.pkl"

    if os.path.exists(cache_path):
        with open(cache_path, "rb") as f:
            print("🔁 Loaded cached FAISS store")
            return pickle.load(f)

    splitter = RecursiveCharacterTextSplitter(chunk_size=1500, chunk_overlap=200)
    docs = splitter.create_documents([transcript])
    vector_store = FAISS.from_documents(docs, embedding=embedding_model)

    with open(cache_path, "wb") as f:
        pickle.dump(vector_store, f)
    print("✅ New FAISS store saved")
    return vector_store


def get_answer(transcript: str, question: str, video_id: str = "default") -> str:
    """Runs the optimized RAG pipeline with caching."""
    
    # 1️⃣ Reuse / create FAISS store
    vector_store = get_vector_store(video_id, transcript)
    retriever = vector_store.as_retriever(search_type="similarity", search_kwargs={"k": 5})

    def format_docs(retrieved_docs):
        return "\n\n".join(doc.page_content for doc in retrieved_docs)

    # 2️⃣ Build chain
    chain = (
        RunnableParallel({
            "context": itemgetter("question") | retriever | RunnableLambda(format_docs),
            "question": itemgetter("question")
        })
        | qa_prompt
        | chat_model
        | StrOutputParser()
    )

    result = chain.invoke({"question": question})
    return result
