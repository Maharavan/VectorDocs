import os
import pickle
import streamlit as st
from rank_bm25 import BM25Okapi
from langchain_community.vectorstores import FAISS
from langchain_openai import ChatOpenAI,OpenAIEmbeddings
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from sentence_transformers import CrossEncoder
from openai import AuthenticationError,RateLimitError
RERANKER = None

def load_rerank_model():
    """Load CrossEncoder model for reranking."""
    global RERANKER
    if RERANKER is None:
        RERANKER = CrossEncoder("cross-encoder/ms-marco-MiniLM-L-6-v2",device='cpu')
    return RERANKER

model = load_rerank_model()

def rerank_encoder(query, documents, top_k=3):
    """Rerank documents using CrossEncoder model."""
    scores = model.predict([(query,doc.page_content) for doc in documents])
    rank_docs = sorted(zip(documents,scores), key=lambda x :x[1],reverse=True)
    top_docs = [doc for doc,score in rank_docs[:top_k]]
    return top_docs


def check_hallcuinated_content(context, question, answer ,llm): 
    """Check if the answer is supported by the context using LLM."""
    prompt = ("""
    You are HallucinationChecker, an expert in verifying the accuracy of answers based on provided context.
    Your task is to determine whether the given answer is supported by the context.

    Context:
    {context}

    Question:
    {question}

    Answer:
    {answer}

    Respond with STRICTLY one word: "supported" or "unsupported".
    """)
    prompt_template = PromptTemplate.from_template(prompt)

    chain = prompt_template| llm | StrOutputParser()

    result = chain.invoke({"context":context,"question":question,"answer":answer})

    if result.strip().lower() == "supported":
        return True

    return False

def embed_vector(query,index_path='faiss_index'):
    """Perform hybrid search using FAISS and BM25, then rerank and generate answer."""
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        return
    try :
        embeddings = OpenAIEmbeddings()
        llm = ChatOpenAI(model="gpt-4o-mini",temperature=0)

        vector_store = FAISS.load_local(index_path,embeddings,allow_dangerous_deserialization=True)
        docs_vector = vector_store.similarity_search(query, k=10)

        print(f"FAISS hits: {len(docs_vector)}")

        try:
            with open("bm25_store.pkl","rb") as f:
                data = pickle.load(f)
            chunks = data["chunks"]
            bm25:BM25Okapi = data["bm25"]
            docs_bm25_raw = bm25.get_top_n(query.split(), chunks, n=10)
            print(f"BM25 hits: {len(docs_bm25_raw)}")
        except FileNotFoundError:
            print("BM25 store not found — run embedding first.")
            docs_bm25_raw = []

        combined_docs = docs_vector + docs_bm25_raw

        if not combined_docs:
            return "No results from FAISS or BM25 — reprocess documents."
        combined_docs = list({doc.page_content: doc for doc in combined_docs}.values())
        reranked_docs = rerank_encoder(query, combined_docs, top_k=3)
        context = "\n\n---\n\n".join([doc.page_content for doc in reranked_docs])

        system_prompt = ("""
        You are VectorDocs, a document-based reasoning assistant.

        You must:
        - Read the context carefully.
        - Understand the user's question.
        - Know the content format is text/pdf/json documents.
        - Extract information relevant to the user's question.
        - If related information exists, answer using it in your own words.
        -----------------
        Context:
        {context}
        -----------------

        Question:
        {question}

        Final Answer:
        """)


        prompt = PromptTemplate.from_template(system_prompt)
        chain = prompt | llm | StrOutputParser()

        answer = chain.invoke({"context":context,"question":query})

        result = check_hallcuinated_content(context, query, answer, llm)
        if not result:
            return f"Possible hallucination — answer not fully found in docs.\n\nAnswer: {answer}"
        return answer
    except AuthenticationError:
        st.error("❌ Invalid OpenAI API key. Please check and try again.")
    except RateLimitError:
        st.error("⚠️ OpenAI rate limit reached. Please try again later.")

    except Exception as e:
        st.error("❌ Failed to process query")
